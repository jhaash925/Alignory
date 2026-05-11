import ollama
import json
import logging
import re
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)


SECTION_ALIASES = {
    "summary": {
        "summary",
        "career objective",
        "objective",
        "professional summary",
        "profile",
    },
    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "key skills",
        "technologies",
        "tech stack",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "internship",
        "internships",
    },
    "projects": {
        "projects",
        "project",
        "project work",
        "personal projects",
        "academic projects",
    },
    "education": {
        "education",
        "educaon",
        "educaton",
        "educa ion",
        "academic background",
        "qualification",
        "qualifications",
        "academics",
    },
}

NON_RENDERED_SECTION_ALIASES = {
    "achievement",
    "achievements",
    "languages",
    "language",
    "certification",
    "certifications",
    "awards",
    "interests",
    "hobbies",
}


def _normalize_heading(line):
    text = line.lower().replace("^", "ti")
    text = re.sub(r"[^a-z\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _compact_heading(line):
    return re.sub(r"[^a-z]", "", line.lower().replace("^", "ti"))


def _looks_like_heading(line):
    if len(line) > 48:
        return False

    if re.search(r"[@|:/\\]|\d{3,}", line):
        return False

    return len(re.findall(r"[A-Za-z]", line)) >= 4


def _match_section_heading(line):
    normalized = _normalize_heading(line)
    compact = _compact_heading(line)

    for section_name, aliases in SECTION_ALIASES.items():
        for alias in aliases:
            alias_normalized = _normalize_heading(alias)
            alias_compact = _compact_heading(alias)

            if normalized == alias_normalized or compact == alias_compact:
                return section_name

            if _looks_like_heading(line):
                similarity = SequenceMatcher(None, compact, alias_compact).ratio()

                if len(compact) >= 6 and similarity >= 0.84:
                    return section_name

    return None


def _looks_like_education_entry(line):
    normalized = line.lower()
    return bool(
        re.search(r"\b(b\.?\s?tech|bachelor|master|m\.?\s?tech|b\.?\s?e\.?|m\.?\s?e\.?|b\.?\s?sc|m\.?\s?sc|mba|degree|diploma|12th|10th|high school|senior secondary|university|college|school)\b", normalized)
        or re.search(r"\b(computer science|engineering|pcm|cgpa|gpa|coursework)\b", normalized)
    )


def _recover_education_section(sections, resume_text):
    if sections.get("education"):
        return sections

    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    recovered = []
    collecting = False

    for line in lines:
        if _match_section_heading(line) == "education" or _compact_heading(line) in {"educaon", "education"}:
            collecting = True
            continue

        if collecting:
            next_section = _match_section_heading(line)

            if next_section and next_section != "education":
                break

            recovered.append(line)
            continue

        if _looks_like_education_entry(line):
            recovered.append(line)

    if recovered:
        sections["education"] = recovered[:8]

    return sections


def _empty_sections():
    return {
        "summary": [],
        "skills": [],
        "experience": [],
        "projects": [],
        "education": []
    }


def _rule_based_parse(resume_text):

    sections = _empty_sections()
    current_section = None

    for raw_line in resume_text.splitlines():

        line = raw_line.strip()

        if not line:
            continue

        normalized = _normalize_heading(line)

        matched_section = _match_section_heading(line)

        if normalized in NON_RENDERED_SECTION_ALIASES:
            current_section = None
            continue

        if matched_section:
            current_section = matched_section
            continue

        if current_section:
            sections[current_section].append(line)

    return _recover_education_section(sections, resume_text)


def parse_resume_to_json(resume_text):
    rule_based = _rule_based_parse(resume_text)

    populated_sections = sum(1 for items in rule_based.values() if items)

    if populated_sections >= 2:
        return rule_based

    prompt = f"""
You are a resume parser.

Extract structured data from this resume.

Return ONLY valid JSON.

Format:

{{
 "summary": [],
 "skills": [],
 "experience": [],
 "projects": [],
 "education": []
}}

Resume:
{resume_text}
"""

    try:

        response = ollama.chat(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            options={"temperature": 0}
        )

        content = response["message"]["content"]

        start = content.find("{")
        end = content.rfind("}") + 1

        content = content[start:end]

        parsed = json.loads(content)

        if not isinstance(parsed, dict):
            raise ValueError("Parsed resume is not a dictionary")

        normalized = _empty_sections()

        for key in normalized:
            value = parsed.get(key, [])

            if isinstance(value, list):
                normalized[key] = value
            elif isinstance(value, str) and value.strip():
                normalized[key] = [value.strip()]

        if any(normalized.values()):
            return normalized

        return rule_based

    except Exception as e:

        logger.error(f"Resume parsing failed: {e}")

        return rule_based
