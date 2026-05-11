import ollama
import numpy as np
import logging
import re
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.skill_graph import expand_skill_graph
from app.services.skill_dictionary import detect_skills_from_text
from app.services.skill_weights import get_skill_weight
from app.services.skill_utils import canonicalize_list

from app.services.resume_parser import parse_resume_to_json

from app.services.skill_extractor import extract_skills_llm
from app.services.skill_normalizer import normalize_skill_list
from app.services.section_scorer import compute_section_scores
from app.services.ats_engine import build_ats_breakdown, build_general_ats_breakdown

from app.services.keyword_engine import (
    extract_important_keywords,
    keyword_match_score
)

# --------------------------------
# LOGGER
# --------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

LLM_TIMEOUT_SECONDS = 45

# --------------------------------
# EMBEDDING MODEL
# --------------------------------

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# --------------------------------
# SKILL DEFINITIONS
# --------------------------------

TECH_SKILLS = [
    "javascript","react","node","express",
    "html","css","tailwind","bootstrap",
    "mongodb","mysql","postgresql","sql","nosql",
    "git","rest","api",
    "python","java","typescript",
    "docker","aws","azure","gcp"
]

SOFT_SKILLS = [
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
    "time management",
    "adaptability",
    "critical thinking",
    "collaboration"
]


# --------------------------------
# LLM CALL
# --------------------------------

def call_llm(prompt):

    try:

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": 0.3,
                "num_predict": 800
            }
        )

        return response["message"]["content"]

    except Exception as e:

        logger.error(f"Ollama error: {e}")
        return "LLM generation failed."


def call_llm_json(prompt):

    executor = None

    try:

        def _request():
            return ollama.chat(
                model="llama3",
                messages=[{"role": "user", "content": prompt}],
                options={
                    "temperature": 0.1,
                    "num_predict": 1400
                }
            )

        executor = ThreadPoolExecutor(max_workers=1)
        future = executor.submit(_request)
        response = future.result(timeout=LLM_TIMEOUT_SECONDS)
        executor.shutdown(wait=False, cancel_futures=True)
        executor = None

        content = response["message"]["content"]
        start = content.find("{")
        end = content.rfind("}") + 1

        if start == -1 or end <= start:
            raise ValueError("No JSON object found in response")

        return json.loads(content[start:end])

    except FuturesTimeoutError:

        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=True)
        logger.error("Ollama JSON request timed out")
        return None

    except Exception as e:

        if executor is not None:
            executor.shutdown(wait=False, cancel_futures=True)
        logger.error(f"Ollama JSON error: {e}")
        return None


# --------------------------------
# NORMALIZE PARSED JSON SECTIONS
# --------------------------------

def normalize_section(section):

    cleaned = []

    for item in section:

        if isinstance(item, str):
            cleaned.append(item)

        elif isinstance(item, dict):

            values = [str(v) for v in item.values()]
            cleaned.append(" ".join(values))

        else:

            cleaned.append(str(item))

    return cleaned


# --------------------------------
# SKILL CLASSIFICATION
# --------------------------------

def classify_skills(skills):

    tech = []
    soft = []
    other = []

    for skill in skills:

        s = skill.lower().strip()

        if s in TECH_SKILLS:

            tech.append(s)

        elif s in SOFT_SKILLS:

            soft.append(s)

        else:

            other.append(s)

    return tech, soft, other

# --------------------------------
# SEMANTIC SKILL MATCH
# --------------------------------

def semantic_skill_match(job_skills, resume_skills):

    if not job_skills or not resume_skills:
        return [], job_skills

    resume_skills = normalize_skill_list(resume_skills)

    job_embeddings = model.encode(job_skills)
    resume_embeddings = model.encode(resume_skills)

    matched = []
    missing = []

    for i, job_skill in enumerate(job_skills):

        job_skill_norm = normalize_skill_list([job_skill])[0]

        # direct match
        if job_skill_norm in resume_skills:

            matched.append(job_skill)
            continue

        # semantic similarity
        similarity = cosine_similarity(
            [job_embeddings[i]],
            resume_embeddings
        )[0]

        if np.max(similarity) > 0.7:

            matched.append(job_skill)
            continue

        # ontology expansion
        equivalents = expand_skill_graph(job_skill_norm)

        equivalents = normalize_skill_list(equivalents)

        if any(eq in resume_skills for eq in equivalents):

            matched.append(job_skill)

        else:

            missing.append(job_skill)

    return matched, missing


# --------------------------------
# FINAL SCORE
# --------------------------------

def compute_final_score(skill_score, exp_score, keyword_score):

    skill_weight = 0.5
    exp_weight = 0.3
    keyword_weight = 0.2

    final = (
        skill_score * skill_weight +
        exp_score * exp_weight +
        keyword_score * keyword_weight
    )

    return int(final * 100)


def compute_relevance_score(skill_score, keyword_score, ats_breakdown, section_score):

    requirements = ats_breakdown.get("requirements", [])
    core_categories = {"technical", "framework", "tooling", "engineering"}

    core_items = [
        item for item in requirements
        if item.get("category") in core_categories
    ]

    if core_items:
        core_total = sum(item.get("weight", 0) for item in core_items) or 1
        core_matched = sum(
            item.get("weight", 0) * max(item.get("confidence", 0), 0.72)
            for item in core_items
            if item.get("matched")
        )
        core_requirement_score = core_matched / core_total
    else:
        core_requirement_score = skill_score

    final = (
        skill_score * 0.45 +
        keyword_score * 0.30 +
        core_requirement_score * 0.20 +
        section_score * 0.05
    )

    return int(final * 100)


# --------------------------------
# RESUME VALIDATION
# --------------------------------

def validate_resume(improved_resume, original_resume):
    cleaned = improved_resume.strip()
    return cleaned if cleaned else original_resume


def normalize_generated_resume(text):

    cleaned = text.replace("\r", "\n").strip()

    cleaned = re.sub(r"\*\*(SUMMARY|SKILLS|EXPERIENCE|PROJECTS|EDUCATION)\*\*", r"\n\1\n", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"(?i)\b(SUMMARY|SKILLS|EXPERIENCE|PROJECTS|EDUCATION)\s*[:\-]\s*", r"\n\1\n", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    sections = ["SUMMARY", "SKILLS", "EXPERIENCE", "PROJECTS", "EDUCATION"]

    for section in sections:
        cleaned = re.sub(
            rf"(?<!\n){section}(?![A-Z])",
            f"\n{section}\n",
            cleaned,
            flags=re.IGNORECASE
        )

    lines = []

    for raw_line in cleaned.split("\n"):
        line = raw_line.strip()

        if not line:
            continue

        upper_line = line.upper().rstrip(":")
        if upper_line in sections:
            lines.append(upper_line)
            continue

        if line.startswith("Here is the edited ATS-friendly resume"):
            continue

        line = re.sub(r"\s{2,}", " ", line)
        line = re.sub(r"\s+-\s+", "\n- ", line)

        for split_line in line.split("\n"):
            split_line = split_line.strip()
            if split_line:
                lines.append(split_line)

    normalized = []

    for line in lines:
        if line in sections:
            normalized.append("")
            normalized.append(line)
            continue

        normalized.append(line)

    cleaned = "\n".join(normalized)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)

    return cleaned.strip()


def extract_header_from_resume_text(raw_resume_text):

    lines = [line.strip() for line in raw_resume_text.splitlines() if line.strip()]

    if not lines:
        return {
            "name": "Candidate Name",
            "contact": [],
            "headline": ""
        }

    name = lines[0]
    contact = []
    headline = ""

    for line in lines[1:6]:
        if (
            "@" in line or
            re.search(r"\b\d{10}\b", re.sub(r"\D", "", line)) or
            re.search(r"linkedin|github|portfolio|www\.|https?://", line, re.IGNORECASE)
        ):
            contact.append(line)
        elif not headline:
            headline = line

    return {
        "name": name,
        "contact": contact,
        "headline": headline
    }


def extract_summary_from_resume_text(raw_resume_text, parsed_resume=None):

    if parsed_resume and parsed_resume.get("summary"):
        summary_lines = normalize_section(parsed_resume.get("summary", []))
        cleaned_lines = [
            line for line in summary_lines
            if _normalize_summary_line(line)
        ]
        if cleaned_lines:
            return " ".join(cleaned_lines).strip()

    lines = [line.strip() for line in raw_resume_text.splitlines() if line.strip()]
    summary_markers = {"career objective", "objective", "summary", "professional summary", "profile"}
    stop_markers = {
        "skills",
        "technical skills",
        "projects",
        "project",
        "education",
        "internships",
        "internship",
        "experience",
        "work experience",
        "achievement",
        "achievements",
        "languages",
        "language",
    }

    collecting = False
    collected = []

    for line in lines:
        normalized = re.sub(r"[^a-z\s]", "", line.lower()).strip()

        if normalized in summary_markers:
            collecting = True
            continue

        if collecting and normalized in stop_markers:
            break

        if collecting and _normalize_summary_line(line):
            collected.append(line)

    return " ".join(collected).strip()


def _normalize_summary_line(line):

    cleaned = str(line).strip()
    if not cleaned:
        return ""

    normalized = re.sub(r"[^a-z\s]", "", cleaned.lower()).strip()
    if normalized in {"career objective", "objective", "summary", "professional summary", "profile"}:
        return ""

    return cleaned


def strip_bullet_prefix(text):

    return re.sub(r"^\s*[-*•]+\s*", "", str(text)).strip()


def merge_wrapped_lines(lines):

    merged = []

    for raw_line in lines:
        line = str(raw_line).strip()
        if not line:
            continue

        if re.match(r"^[-*•]\s*", line):
            merged.append(strip_bullet_prefix(line))
            continue

        if not merged:
            merged.append(line)
            continue

        previous = merged[-1]
        if previous.endswith((".", "!", "?", ":")):
            merged.append(line)
        else:
            merged[-1] = f"{previous} {line}".strip()

    return merged


def merge_wrapped_skill_lines(lines):

    merged = []

    def starts_new_skill_group(text):
        return bool(re.match(r"^[A-Za-z][A-Za-z &/()+-]{0,40}:\s*", text))

    for raw_line in lines:
        line = str(raw_line).strip()
        if not line:
            continue

        if not merged:
            merged.append(line)
            continue

        if starts_new_skill_group(line):
            merged.append(line)
            continue

        previous = merged[-1]
        if previous.endswith((".", "!", "?")):
            merged.append(line)
        else:
            merged[-1] = f"{previous} {line}".strip()

    return merged


def build_entries_from_lines(lines, entry_type):

    merged_lines = merge_wrapped_lines(lines)
    entries = []
    current = None

    def is_action_line(text):
        return text.startswith((
            "Built ", "Developed ", "Designed ", "Optimized ", "Collaborated ",
            "Created ", "Implemented ", "Led ", "Managed ", "Worked ", "Provided "
        ))

    def is_project_title_line(text):
        return (
            not is_action_line(text)
            and ("—" in text or " – " in text or " - " in text)
            and not text.endswith(".")
        )

    for line in merged_lines:
        is_title_line = not is_action_line(line) and "•" not in line[:2]

        if entry_type == "experience":
            if current is None or ("," in line and "(" in line and ")" in line and is_title_line):
                if current:
                    entries.append(current)
                title_part, _, date_part = line.rpartition("(")
                title_company = title_part.strip(" ,")
                dates = f"({date_part}" if date_part else ""
                title = title_company
                company = ""
                if "," in title_company:
                    title, company = [part.strip() for part in title_company.split(",", 1)]
                current = {
                    "title": title,
                    "company": company,
                    "dates": dates.strip(),
                    "brief": "",
                    "bullets": []
                }
                continue
        else:
            if current is None or is_project_title_line(line):
                if current:
                    entries.append(current)
                if "—" in line:
                    name, subtitle = [part.strip() for part in line.split("—", 1)]
                elif " – " in line:
                    name, subtitle = [part.strip() for part in line.split(" – ", 1)]
                elif " - " in line:
                    name, subtitle = [part.strip() for part in line.split(" - ", 1)]
                else:
                    name, subtitle = [line.strip(), ""]
                current = {
                    "name": name,
                    "subtitle": subtitle,
                    "brief": "",
                    "bullets": []
                }
                continue

        if current is None:
            continue

        if not current["brief"]:
            current["brief"] = line
        else:
            current["bullets"].append(strip_bullet_prefix(line))

    if current:
        entries.append(current)

    return [
        entry for entry in entries
        if any(entry.get(field) for field in ["title", "company", "name", "brief"]) or entry.get("bullets")
    ]


def build_structured_resume_fallback(raw_resume_text, parsed_resume):

    header = extract_header_from_resume_text(raw_resume_text)
    summary_text = extract_summary_from_resume_text(raw_resume_text, parsed_resume)
    skills_lines = merge_wrapped_skill_lines(normalize_section(parsed_resume.get("skills", [])))
    experience_lines = normalize_section(parsed_resume.get("experience", []))
    project_lines = normalize_section(parsed_resume.get("projects", []))
    education_lines = normalize_section(parsed_resume.get("education", []))

    return {
        "header": header,
        "summary": summary_text or header.get("headline", ""),
        "skills": normalize_skill_groups([], skills_lines),
        "experience": build_entries_from_lines(experience_lines, "experience"),
        "projects": build_entries_from_lines(project_lines, "projects"),
        "education": education_lines[:4]
    }


def normalize_string_list(value):

    if isinstance(value, str):
        items = [strip_bullet_prefix(item) for item in re.split(r"[,\n|]+", value) if item.strip()]
        return items

    if isinstance(value, list):
        items = []
        for entry in value:
            if isinstance(entry, str) and entry.strip():
                items.append(strip_bullet_prefix(entry))
        return items

    return []


def looks_like_skill_noise(text):

    lowered = text.lower()

    if any(marker in lowered for marker in [
        "certificate",
        "awarded",
        "recognized",
        "presentation",
        "nptel",
        "course"
    ]):
        return True

    if "." in text and len(text.split()) > 8:
        return True

    return False


def clean_skill_label(label):

    cleaned = re.sub(r"\s+", " ", str(label)).strip(" :-")
    cleaned = cleaned.replace("&", " & ")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    lowered = cleaned.lower()
    label_map = {
        "technical skills": "Technical Skills",
        "tech skills": "Technical Skills",
        "soft skills": "Soft Skills",
        "core skills": "Core Skills",
        "tools": "Tools",
        "technologies": "Technical Skills",
        "github, database management system": "Tools & Databases",
        "github database management system": "Tools & Databases",
        "database management system": "Databases",
    }

    if lowered in label_map:
        return label_map[lowered]

    if "," in cleaned:
        parts = [part.strip() for part in cleaned.split(",") if part.strip()]
        if 1 < len(parts) <= 3:
            cleaned = " & ".join(parts)

    words = cleaned.split()
    if len(words) > 4:
        cleaned = " ".join(words[:4])

    return cleaned.title() or "Skills"


def split_skill_items(text):

    text = re.sub(r"^(technical skills|soft skills)\s*:\s*", "", text, flags=re.IGNORECASE).strip()

    if "(" in text and ")" in text:
        prefix = text.split("(", 1)[0].strip(" :-")
        nested = text.split("(", 1)[1].rsplit(")", 1)[0]
        nested_items = [item.strip() for item in nested.split(",") if item.strip()]
        if prefix and nested_items:
            category_like_prefixes = {
                "frontend development",
                "backend development",
                "technical skills",
                "soft skills",
                "programming languages",
                "languages",
                "tools",
                "tooling",
            }

            if prefix.lower() in category_like_prefixes:
                return clean_skill_label(prefix), nested_items

            return None, [prefix, *nested_items]

    items = [
        item.strip(" -•")
        for item in re.split(r",|\||;", text)
        if item.strip(" -•")
    ]
    return None, items


def split_top_level_segments(text):

    segments = []
    current = []
    depth = 0

    for char in str(text):
        if char == "(":
            depth += 1
        elif char == ")" and depth > 0:
            depth -= 1

        if char == "," and depth == 0:
            segment = "".join(current).strip()
            if segment:
                segments.append(segment)
            current = []
            continue

        current.append(char)

    final_segment = "".join(current).strip()
    if final_segment:
        segments.append(final_segment)

    return segments


def extract_source_skill_groups(parsed_resume):

    skills_lines = merge_wrapped_skill_lines(normalize_section(parsed_resume.get("skills", [])))
    return normalize_skill_groups([], skills_lines)


def flatten_skill_groups(skill_groups):

    inventory = []

    for group in skill_groups or []:
        if not isinstance(group, dict):
            continue
        for item in group.get("items", []):
            cleaned = re.sub(r"\s+", " ", str(item)).strip(" -•")
            if cleaned:
                inventory.append(cleaned)

    return canonicalize_list(inventory)


def ensure_all_source_skills_present(skill_groups, source_skill_groups):

    groups_by_category = {}

    for group in skill_groups or []:
        if not isinstance(group, dict):
            continue
        category = group.get("category", "Technical Skills")
        groups_by_category[category] = canonicalize_list(group.get("items", []))

    for source_group in source_skill_groups or []:
        if not isinstance(source_group, dict):
            continue
        category = source_group.get("category", "Technical Skills")
        existing = groups_by_category.get(category, [])
        groups_by_category[category] = canonicalize_list(existing + source_group.get("items", []))

    preferred_order = [
        "Technical Skills",
        "Frontend Development",
        "Backend Development",
        "Programming Languages",
        "Databases",
        "Tools",
        "Core CS",
        "Soft Skills",
    ]

    merged_groups = [
        {"category": category, "items": items[:24]}
        for category, items in groups_by_category.items()
        if items
    ]
    merged_groups.sort(
        key=lambda group: (
            preferred_order.index(group["category"])
            if group["category"] in preferred_order
            else len(preferred_order),
            group["category"]
        )
    )

    return merged_groups[:8]


def normalize_project_entries(projects):

    normalized_projects = []

    for item in projects or []:
        if not isinstance(item, dict):
            continue

        brief = str(item.get("brief", "")).strip()
        bullets = [strip_bullet_prefix(b) for b in item.get("bullets", []) if str(b).strip()]

        # A single leftover bullet reads awkwardly in the template; fold it into the body.
        if len(bullets) == 1:
            brief = f"{brief} {bullets[0]}".strip() if brief else bullets[0]
            bullets = []

        normalized_projects.append({
            **item,
            "brief": brief,
            "bullets": bullets,
        })

    return normalized_projects


def categorize_skill_item(item, category_hint=""):

    cleaned_item = re.sub(r"\s+", " ", str(item)).strip(" -•&")
    lowered_item = cleaned_item.lower()
    lowered_hint = clean_skill_label(category_hint).lower() if category_hint else ""

    ignored_skill_labels = {
        "backend development",
        "frontend development",
        "technical skills",
        "soft skills",
        "database management system",
    }

    if lowered_item in ignored_skill_labels:
        return ""

    soft_skill_terms = {
        "communication",
        "problem solving ability",
        "problem solving",
        "teamwork & collaboration",
        "teamwork",
        "collaboration",
        "adaptability & learning agility",
        "adaptability",
        "learning agility",
        "critical thinking",
        "creativity & innovation",
        "creativity",
        "innovation",
        "time management",
        "attention to detail",
        "leadership",
    }

    if lowered_item in soft_skill_terms or lowered_hint == "soft skills":
        return "Soft Skills"

    if any(term in lowered_item for term in [
        "sql",
        "mongodb",
        "mysql",
        "postgres",
        "database",
        "nosql",
    ]):
        return "Databases"

    if any(term in lowered_item for term in [
        "operating system",
        "computer networks",
        "data structures",
        "algorithms",
        "oops",
        "dbms",
    ]):
        return "Core CS"

    if any(term in lowered_item for term in [
        "git",
        "github",
        "postman",
        "docker",
        "jira",
    ]):
        return "Tools"

    if lowered_hint in {
        "frontend development",
        "backend development",
        "programming languages",
        "technical skills",
        "databases",
        "soft skills",
        "tools",
        "core cs",
    }:
        hint_map = {
            "technical skills": "Technical Skills",
            "frontend development": "Frontend Development",
            "backend development": "Backend Development",
            "programming languages": "Programming Languages",
            "databases": "Databases",
            "soft skills": "Soft Skills",
            "tools": "Tools",
            "core cs": "Core CS",
        }
        return hint_map[lowered_hint]

    if lowered_hint in {"skills", "core skills", ""}:
        return "Technical Skills"

    return clean_skill_label(category_hint)


def normalize_skill_groups(raw_groups, fallback_lines):

    groups = []
    grouped_items = {}

    def normalize_skill_category(category):
        cleaned = clean_skill_label(category)
        lowered = cleaned.lower()

        if lowered in {"skills", "core skills"}:
            return "Technical Skills"

        return cleaned

    def push_group(category, items):
        for item in items:
            candidate = re.sub(r"\s+", " ", item).strip(" -•&")
            if not candidate or looks_like_skill_noise(candidate):
                continue
            normalized_category = categorize_skill_item(
                candidate,
                normalize_skill_category(category)
            )
            if not normalized_category:
                continue
            existing = grouped_items.get(normalized_category, [])
            merged = canonicalize_list(existing + [candidate])
            grouped_items[normalized_category] = merged[:24]

    if isinstance(raw_groups, list):
        for group in raw_groups:
            if not isinstance(group, dict):
                continue

            category = clean_skill_label(group.get("category", "Skills"))
            source_items = normalize_string_list(group.get("items"))
            flat_items = []

            for item in source_items:
                if looks_like_skill_noise(item):
                    continue

                segments = split_top_level_segments(item)

                for segment in segments:
                    if ":" in segment and len(segment.split(":", 1)[0].split()) <= 4:
                        label, rest = segment.split(":", 1)
                        _, nested_items = split_skill_items(rest)
                        push_group(label, nested_items)
                    else:
                        nested_category, nested_items = split_skill_items(segment)
                        if nested_category:
                            push_group(nested_category, nested_items)
                        else:
                            flat_items.extend(nested_items)

            push_group(category, flat_items)

    for line in fallback_lines:
        if looks_like_skill_noise(line):
            continue

        segments = split_top_level_segments(line)

        for segment in segments:
            if ":" in segment and len(segment.split(":", 1)[0].split()) <= 4:
                label, rest = segment.split(":", 1)
                _, nested_items = split_skill_items(rest)
                push_group(label, nested_items)
            else:
                nested_category, nested_items = split_skill_items(segment)
                push_group(nested_category or "Core Skills", nested_items)

    for category, items in grouped_items.items():
        groups.append({
            "category": category,
            "items": items
        })

    preferred_order = [
        "Technical Skills",
        "Frontend Development",
        "Backend Development",
        "Programming Languages",
        "Databases",
        "Tools",
        "Core CS",
        "Soft Skills",
    ]
    groups.sort(
        key=lambda group: (
            preferred_order.index(group["category"])
            if group["category"] in preferred_order
            else len(preferred_order),
            group["category"]
        )
    )

    return groups[:8]


def normalize_structured_resume(data, fallback):

    if not isinstance(data, dict):
        return fallback

    header = data.get("header", {}) if isinstance(data.get("header"), dict) else {}

    normalized = {
        "header": {
            "name": str(header.get("name", fallback["header"]["name"])).strip() or fallback["header"]["name"],
            "contact": normalize_string_list(header.get("contact")) or fallback["header"]["contact"],
            "headline": str(header.get("headline", fallback["header"]["headline"])).strip()
        },
        "summary": str(data.get("summary", fallback["summary"])).strip(),
        "skills": [],
        "experience": [],
        "projects": [],
        "education": normalize_string_list(data.get("education")) or fallback["education"]
    }

    fallback_skill_lines = merge_wrapped_skill_lines(
        normalize_section(parse_resume_to_json(structured_resume_to_text(fallback)).get("skills", []))
    )
    source_skill_groups = []
    if isinstance(data.get("skills"), list):
        source_skill_groups.extend(data.get("skills", []))
    if isinstance(fallback.get("skills"), list):
        source_skill_groups.extend(fallback.get("skills", []))

    source_only_skill_groups = extract_source_skill_groups(parse_resume_to_json(structured_resume_to_text(fallback)))
    normalized["skills"] = source_only_skill_groups or normalize_skill_groups(source_skill_groups, fallback_skill_lines)
    if not normalized["skills"]:
        normalized["skills"] = normalize_skill_groups([], fallback_skill_lines)

    raw_experience = data.get("experience", [])
    if isinstance(raw_experience, list):
        for item in raw_experience:
            if isinstance(item, dict):
                bullets = normalize_string_list(item.get("bullets"))
                title = str(item.get("title", "")).strip()
                company = str(item.get("company", "")).strip()
                dates = str(item.get("dates", "")).strip()
                brief = str(item.get("brief", "")).strip()
                if title or company or bullets or brief:
                    normalized["experience"].append({
                        "title": title,
                        "company": company,
                        "dates": dates,
                        "brief": brief,
                        "bullets": bullets
                    })
    if not normalized["experience"]:
        normalized["experience"] = fallback["experience"]

    raw_projects = data.get("projects", [])
    if isinstance(raw_projects, list):
        for item in raw_projects:
            if isinstance(item, dict):
                bullets = normalize_string_list(item.get("bullets"))
                name = str(item.get("name", "")).strip()
                subtitle = str(item.get("subtitle", "")).strip()
                brief = str(item.get("brief", "")).strip()
                if name or bullets or brief:
                    normalized["projects"].append({
                        "name": name,
                        "subtitle": subtitle,
                        "brief": brief,
                        "bullets": bullets
                    })
    if not normalized["projects"]:
        normalized["projects"] = fallback["projects"]
    normalized["projects"] = normalize_project_entries(normalized["projects"])

    return normalized


def structured_resume_to_text(data):

    lines = []
    header = data.get("header", {})

    if header.get("name"):
        lines.append(header["name"])
    for contact_line in header.get("contact", []):
        lines.append(contact_line)
    if header.get("headline"):
        lines.append(header["headline"])

    if data.get("summary"):
        lines.extend(["", "SUMMARY", data["summary"]])

    if data.get("skills"):
        lines.extend(["", "SKILLS"])
        for group in data["skills"]:
            category = group.get("category", "Skills")
            items = ", ".join(group.get("items", []))
            if items:
                lines.append(f"{category}: {items}")

    if data.get("experience"):
        lines.extend(["", "EXPERIENCE"])
        for item in data["experience"]:
            title_line = " | ".join(
                part for part in [item.get("title", ""), item.get("company", ""), item.get("dates", "")]
                if part
            )
            if title_line:
                lines.append(title_line)
            if item.get("brief"):
                lines.append(item["brief"])
            for bullet in item.get("bullets", []):
                lines.append(f"- {bullet}")

    if data.get("projects"):
        lines.extend(["", "PROJECTS"])
        for item in data["projects"]:
            title_line = " | ".join(
                part for part in [item.get("name", ""), item.get("subtitle", "")]
                if part
            )
            if title_line:
                lines.append(title_line)
            if item.get("brief"):
                lines.append(item["brief"])
            for bullet in item.get("bullets", []):
                lines.append(f"- {bullet}")

    if data.get("education"):
        lines.extend(["", "EDUCATION"])
        for item in data["education"]:
            lines.append(item)

    return "\n".join(lines).strip()


def format_requirement_notes(items):

    lines = []

    for item in items:
        title = item.get("name") or item.get("title") or "Requirement"
        parts = []

        if item.get("severity"):
            parts.append(item["severity"])

        if item.get("proof_strength") and item["proof_strength"] != "missing":
            parts.append(f'{item["proof_strength"]} proof')

        if item.get("recent_evidence"):
            parts.append("recent evidence")

        suffix = f" ({', '.join(parts)})" if parts else ""
        lines.append(f"- {title}{suffix}")

    return "\n".join(lines)


def extract_resume_skill_inventory(raw_resume_text, parsed_resume):

    detected = detect_skills_from_text(raw_resume_text)
    detected = normalize_skill_list(detected)
    source_skill_groups = extract_source_skill_groups(parsed_resume)
    explicit_terms = flatten_skill_groups(source_skill_groups)

    return canonicalize_list(detected + explicit_terms)


def extract_verified_requirement_inventory(ats_breakdown):

    verified = []

    for item in ats_breakdown.get("matched_requirements", []):
        if item.get("matched"):
            verified.append(item.get("name", ""))

    return canonicalize_list([item for item in verified if item])


def prioritize_list_by_job_terms(items, priority_terms):

    normalized_terms = [term.lower() for term in priority_terms if term]

    def score_item(text):
        lowered = str(text).lower()
        return sum(
            1
            for term in normalized_terms
            if term in lowered
        )

    return sorted(
        items,
        key=lambda item: (-score_item(item), str(item).lower())
    )


def prioritize_structured_resume(structured_resume, ats_breakdown, job_description):

    if not isinstance(structured_resume, dict):
        return structured_resume

    requirement_terms = [
        item.get("name", "")
        for item in ats_breakdown.get("requirements", [])
        if item.get("name")
    ]
    job_skills = normalize_skill_list(detect_skills_from_text(job_description))
    priority_terms = canonicalize_list(requirement_terms + job_skills)

    prioritized = {
        **structured_resume,
        "skills": [],
        "experience": [],
        "projects": [],
    }

    for group in structured_resume.get("skills", []):
        if not isinstance(group, dict):
            continue

        prioritized["skills"].append({
            "category": group.get("category", "Skills"),
            "items": prioritize_list_by_job_terms(group.get("items", []), priority_terms)
        })

    def score_entry(item):
        fragments = []
        for field in ["title", "company", "brief", "name", "subtitle"]:
            value = item.get(field)
            if value:
                fragments.append(str(value))
        fragments.extend(item.get("bullets", []))
        combined = " ".join(fragments).lower()

        score = 0
        for term in priority_terms:
            lowered_term = term.lower()
            if lowered_term and lowered_term in combined:
                score += 1
        return score

    experience = list(structured_resume.get("experience", []))
    projects = normalize_project_entries(list(structured_resume.get("projects", [])))

    prioritized["experience"] = sorted(
        experience,
        key=lambda item: (-score_entry(item), str(item.get("title", "")).lower(), str(item.get("company", "")).lower())
    )
    prioritized["projects"] = sorted(
        projects,
        key=lambda item: (-score_entry(item), str(item.get("name", "")).lower())
    )

    return prioritized


def pick_best_structured_resume(job_description, original_resume_text, parsed_resume, candidate_structured, fallback_structured):

    original_breakdown = build_ats_breakdown(
        job_description,
        original_resume_text,
        parsed_resume
    )

    candidates = []
    for structured in [candidate_structured, fallback_structured]:
        if not structured:
            continue
        candidate_text = structured_resume_to_text(structured)
        candidate_parsed = parse_resume_to_json(candidate_text)
        candidate_breakdown = build_ats_breakdown(
            job_description,
            candidate_text,
            candidate_parsed
        )
        candidates.append((structured, candidate_breakdown))

    if not candidates:
        return fallback_structured

    best_structured, best_breakdown = max(
        candidates,
        key=lambda item: (
            item[1].get("overall_score", 0),
            item[1].get("subscores", {}).get("keyword_alignment", 0),
            item[1].get("subscores", {}).get("skills", 0)
        )
    )

    if best_breakdown.get("overall_score", 0) < original_breakdown.get("overall_score", 0):
        return fallback_structured

    return best_structured


def generate_improved_resume_draft(job_description, resume_text):

    raw_resume_text = resume_text.strip()
    parsed_resume = parse_resume_to_json(raw_resume_text)

    all_sections = []

    for section_content in parsed_resume.values():
        normalized = normalize_section(section_content)
        all_sections.extend(normalized)

    parsed_text = " ".join(all_sections)
    combined_resume_text = " ".join(
        part for part in [raw_resume_text, parsed_text] if part
    )
    ats_breakdown = build_ats_breakdown(
        job_description,
        combined_resume_text,
        parsed_resume
    )
    source_skill_groups = extract_source_skill_groups(parsed_resume)
    allowed_skills = extract_resume_skill_inventory(raw_resume_text, parsed_resume)
    verified_requirements = extract_verified_requirement_inventory(ats_breakdown)
    weak_proof_items = [
        card["title"]
        for card in ats_breakdown.get("explanation_cards", [])
        if card.get("type") == "weak_evidence"
    ]

    fallback_structured = build_structured_resume_fallback(raw_resume_text, parsed_resume)

    improve_prompt = f"""
You are an expert ATS resume editor.

Rewrite the resume as structured JSON.

RULES:
- Do NOT invent skills
- Do NOT add fake projects
- Only use information already present in the source resume
- You may strengthen wording, structure, and bullet quality, but you must not introduce new tools, frameworks, platforms, or certifications that are not already in the source
- If a job requirement is missing from the source resume, do not add it
- Keep the candidate's skill set truthful
- Preserve contact or header details if present in the source
- Preserve the Career Objective / Summary if present in the source, but rewrite it more professionally if needed
- Use concise ATS-friendly bullets
- In EXPERIENCE and PROJECTS, rewrite bullets to emphasize already-existing relevant skills and accomplishments
- Prefer 2 to 4 bullets per role or project
- Add a short 1-line brief under each experience item and each project that explains what it was or what the work focused on
- Keep technical/backend/foundational skills from the source resume if they are present, including areas like backend development, databases, operating systems, and computer networks
- Do not move non-skills such as achievements, awards, class projects, or certifications into the SKILLS section
- Order skills, experience, and projects so the most job-relevant verified material appears first
- Return ONLY valid JSON

Resume:
{combined_resume_text}

Job Description:
{job_description}

Allowed skills and technologies from the source resume:
{", ".join(allowed_skills) if allowed_skills else "Use only the exact skills already present in the source resume."}

Verified strengths already supported by the resume:
{", ".join(verified_requirements) if verified_requirements else "Use only what is clearly supported in the source resume."}

Areas that need stronger proof, not new skills:
{", ".join(weak_proof_items) if weak_proof_items else "Strengthen existing evidence where possible."}

JSON format:
{{
  "header": {{
    "name": "",
    "contact": [],
    "headline": ""
  }},
  "summary": "",
  "skills": [
    {{
      "category": "",
      "items": []
    }}
  ],
  "experience": [
    {{
      "title": "",
      "company": "",
      "dates": "",
      "brief": "",
      "bullets": []
    }}
  ],
  "projects": [
    {{
      "name": "",
      "subtitle": "",
      "brief": "",
      "bullets": []
    }}
  ],
  "education": []
}}
"""

    raw_structured = call_llm_json(improve_prompt)
    structured_resume = normalize_structured_resume(raw_structured, fallback_structured)
    structured_resume["skills"] = ensure_all_source_skills_present(
        source_skill_groups,
        source_skill_groups
    )
    structured_resume = prioritize_structured_resume(
        structured_resume,
        ats_breakdown,
        job_description
    )
    fallback_structured = prioritize_structured_resume(
        fallback_structured,
        ats_breakdown,
        job_description
    )
    fallback_structured["skills"] = ensure_all_source_skills_present(
        source_skill_groups,
        source_skill_groups
    )
    structured_resume = pick_best_structured_resume(
        job_description,
        combined_resume_text,
        parsed_resume,
        structured_resume,
        fallback_structured
    )
    normalized_resume = structured_resume_to_text(structured_resume)
    validated_resume = validate_resume(normalized_resume, combined_resume_text)

    return {
        "text": validated_resume,
        "structured": structured_resume
    }


# --------------------------------
# MAIN PIPELINE
# --------------------------------

def generate_general_ats_review(resume_text):

    logger.info("Starting general ATS review")

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is required to generate a general ATS review.")

    raw_resume_text = resume_text.strip()
    parsed_resume = parse_resume_to_json(raw_resume_text)

    all_sections = []

    for section_content in parsed_resume.values():
        all_sections.extend(normalize_section(section_content))

    normalized_resume_text = " ".join(all_sections)
    combined_resume_text = " ".join(
        part for part in [raw_resume_text, normalized_resume_text] if part
    )

    resume_skills = detect_skills_from_text(combined_resume_text)

    if not resume_skills:
        resume_skills = extract_skills_llm(combined_resume_text)

    resume_skills = canonicalize_list(normalize_skill_list(resume_skills))
    resume_tech, resume_soft, _ = classify_skills(resume_skills)
    ats_breakdown = build_general_ats_breakdown(raw_resume_text, parsed_resume)
    ats_score = ats_breakdown["overall_score"]
    subscores = ats_breakdown.get("subscores", {})
    enterprise_profile = ats_breakdown.get("enterprise_profile", {})
    diagnostics = enterprise_profile.get("diagnostics", {})
    risk_flags = enterprise_profile.get("risk_flags", [])
    missing_priorities = ats_breakdown.get("missing_requirements", [])
    matched_strengths = ats_breakdown.get("matched_requirements", [])

    resume_suggestions = [
        item["evidence"]
        for item in missing_priorities[:8]
    ]

    resume_suggestions.extend(
        flag["label"]
        for flag in risk_flags[:3]
        if flag.get("label")
    )

    if not resume_suggestions:
        resume_suggestions.append(
            "Your resume has the core ATS basics in place. Next, refine bullets for sharper impact and clearer outcomes."
        )

    analysis_lines = [
        f"ATS Score Explanation: This resume scores {ats_score}% in the enterprise-style general ATS model without using a job description.",
        f"Parser Readiness: {subscores.get('parser_readiness', 0)}% based on identity parsing, section taxonomy, and extraction-safe formatting.",
        f"Searchability: {subscores.get('searchability', 0)}% based on concrete skills, title signal, keyword density, and whether skills appear in experience context.",
        f"Evidence Strength: {subscores.get('impact', 0)}% based on action verbs, measurable achievements, metric density, and outcome language.",
        f"Chronology: {subscores.get('chronology', 0)}% based on dates, month/year precision, role structure, and timeline coverage.",
        f"Readability and Professionalism: {subscores.get('readability', 0)}% readability and {subscores.get('professionalism', 0)}% professionalism.",
        (
            "Enterprise Diagnostics: "
            f"{diagnostics.get('words', 0)} words, "
            f"{diagnostics.get('bullets', 0)} bullets, "
            f"{diagnostics.get('metrics', 0)} metrics, "
            f"{diagnostics.get('detected_skills', 0)} detected skills, "
            f"{diagnostics.get('contextualized_skills', 0)} skills backed in experience or projects."
        ),
        "Risk Flags: "
        + (
            ", ".join(flag["label"] for flag in risk_flags[:5])
            if risk_flags
            else "No major enterprise ATS risk flags detected."
        ),
        "Top Strengths: "
        + (
            ", ".join(item["name"] for item in matched_strengths[:5])
            if matched_strengths
            else "No major strengths detected yet."
        ),
        "Top Improvements: "
        + (
            ", ".join(item["name"] for item in missing_priorities[:5])
            if missing_priorities
            else "No major ATS basics are missing."
        ),
    ]

    logger.info("General ATS review complete")

    return {
        "mode": "general",
        "ats_score": ats_score,
        "relevance_score": ats_score,
        "ats_depth_score": ats_score,
        "matched_skills": resume_tech,
        "missing_skills": [],
        "soft_skills_detected": resume_soft,
        "important_keywords": ats_breakdown.get("keyword_matched", []),
        "keyword_matched": ats_breakdown.get("keyword_matched", []),
        "keyword_missing": ats_breakdown.get("keyword_missing", []),
        "analysis": "\n\n".join(analysis_lines),
        "improved_resume": "",
        "resume_suggestions": resume_suggestions,
        "ats_breakdown": ats_breakdown,
        "enterprise_profile": enterprise_profile,
        "matched_requirements": matched_strengths,
        "missing_requirements": missing_priorities,
    }

def generate_tailored_resume(job_description, resume_text=None, include_improved_resume=False):

    logger.info("Starting resume analysis")

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text is required to generate ATS analysis.")


    # --------------------------------
    # PARSE FULL RESUME
    # --------------------------------

    raw_resume_text = resume_text.strip()

    parsed_resume = parse_resume_to_json(raw_resume_text)


    # --------------------------------
    # BUILD RESUME TEXT FROM ALL PARSED SECTIONS
    # --------------------------------

    all_sections = []

    for section_name, section_content in parsed_resume.items():

        normalized = normalize_section(section_content)

        all_sections.extend(normalized)

    resume_text = " ".join(all_sections)

    combined_resume_text = " ".join(
        part for part in [raw_resume_text, resume_text] if part
    )

    logger.info(f"RESUME TEXT SAMPLE: {combined_resume_text[:500]}")


    # --------------------------------
    # SKILL EXTRACTION
    # --------------------------------

    job_skills = detect_skills_from_text(job_description)

    resume_skills = detect_skills_from_text(combined_resume_text)

    logger.info(f"RAW JOB SKILLS: {job_skills}")
    logger.info(f"RAW RESUME SKILLS: {resume_skills}")

    if not job_skills:

        job_skills = extract_skills_llm(job_description)

    if not resume_skills:

        resume_skills = extract_skills_llm(combined_resume_text)

    job_skills = normalize_skill_list(job_skills)
    resume_skills = normalize_skill_list(resume_skills)

    logger.info(f"NORMALIZED JOB SKILLS: {job_skills}")
    logger.info(f"NORMALIZED RESUME SKILLS: {resume_skills}")

    job_skills = canonicalize_list(job_skills)
    resume_skills = canonicalize_list(resume_skills)

    logger.info(f"JOB SKILLS DETECTED: {job_skills}")
    logger.info(f"RESUME SKILLS DETECTED: {resume_skills}")

    logger.info(f"Job Skills Detected: {job_skills}")
    logger.info(f"Resume Skills Detected: {resume_skills}")


    # --------------------------------
    # CLASSIFY SKILLS
    # --------------------------------

    job_tech, job_soft, _ = classify_skills(job_skills)

    resume_tech, resume_soft, _ = classify_skills(resume_skills)


    # --------------------------------
    # SECTION SCORE
    # --------------------------------

    section_score = compute_section_scores(parsed_resume, job_tech)


    # --------------------------------
    # SKILL MATCHING
    # --------------------------------

    matched_skills, missing_skills = semantic_skill_match(
        job_tech,
        resume_tech
    )


    # --------------------------------
    # WEIGHTED SKILL SCORE
    # --------------------------------

    total_weight = 0
    matched_weight = 0

    for skill in job_tech:

        weight = get_skill_weight(skill)

        total_weight += weight

        if skill in matched_skills:

            matched_weight += weight

    skill_score = matched_weight / total_weight if total_weight else 0


    # --------------------------------
    # EXPERIENCE SIMILARITY
    # --------------------------------

    job_emb = model.encode([job_description])[0]

    resume_emb = model.encode([combined_resume_text])[0]

    exp_score = cosine_similarity(
        [job_emb],
        [resume_emb]
    )[0][0]


    # --------------------------------
    # KEYWORD ANALYSIS
    # --------------------------------

    important_keywords = extract_important_keywords(job_description)

    keyword_score, keyword_matched, keyword_missing = keyword_match_score(
        important_keywords,
        combined_resume_text
    )

    ats_breakdown = build_ats_breakdown(
        job_description,
        combined_resume_text,
        parsed_resume
    )


    # --------------------------------
    # FINAL ATS SCORE
    # --------------------------------

    ats_score = max(
        compute_final_score(
            (skill_score + section_score) / 2,
            exp_score,
            keyword_score
        ),
        ats_breakdown["overall_score"]
    )

    relevance_score = max(
        compute_relevance_score(
            skill_score,
            keyword_score,
            ats_breakdown,
            section_score
        ),
        ats_breakdown["subscores"].get("keyword_alignment", 0)
    )


    # --------------------------------
    # RESUME SUGGESTIONS
    # --------------------------------

    resume_suggestions = []

    missing_requirement_names = [
        requirement["name"]
        for requirement in ats_breakdown["missing_requirements"][:6]
    ]

    for skill in missing_requirement_names or missing_skills:

        resume_suggestions.append(
            f'Consider adding or highlighting "{skill}" in your resume if you have experience with it.'
        )

    for card in ats_breakdown.get("explanation_cards", [])[:4]:
        resume_suggestions.append(card["message"])


    improved_resume = (
        generate_improved_resume_draft(job_description, raw_resume_text)
        if include_improved_resume
        else ""
    )


    # --------------------------------
    # ANALYSIS
    # --------------------------------

    analysis_prompt = f"""
You are an ATS resume analysis assistant.

IMPORTANT:
Only use the skills provided.

ATS Score: {ats_score}

Relevance Score: {relevance_score}

Matched Skills:
{matched_skills}

Missing Skills:
{missing_requirement_names or missing_skills}

Top ATS Insights:
{chr(10).join(f"- {card['message']}" for card in ats_breakdown.get("explanation_cards", [])[:5])}

Explain:

1. ATS Score Explanation
2. Matched Technical Skills
3. Missing Technical Skills
4. Resume Improvement Tips
5. Which skills are present but need stronger proof in projects or experience
"""

    analysis = call_llm(analysis_prompt)

    logger.info("Resume analysis complete")


    return {

        "ats_score": ats_score,

        "relevance_score": relevance_score,

        "ats_depth_score": ats_score,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "soft_skills_detected": resume_soft,

        "important_keywords": important_keywords,

        "keyword_matched": ats_breakdown["keyword_matched"] or keyword_matched,

        "keyword_missing": ats_breakdown["keyword_missing"] or keyword_missing,

        "analysis": analysis,

        "improved_resume": improved_resume,

        "resume_suggestions": resume_suggestions,

        "ats_breakdown": ats_breakdown,

        "matched_requirements": ats_breakdown["matched_requirements"],

        "missing_requirements": ats_breakdown["missing_requirements"]
    }
