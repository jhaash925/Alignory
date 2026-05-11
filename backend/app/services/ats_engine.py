import re
from datetime import datetime

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from app.services.keyword_engine import extract_important_keywords, keyword_match_score
from app.services.section_scorer import compute_section_scores
from app.services.skill_dictionary import detect_skills_from_text


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
CURRENT_YEAR = datetime.now().year


REQUIREMENT_LIBRARY = [
    {
        "name": "HTML",
        "category": "technical",
        "weight": 5,
        "aliases": ["html", "html5"],
    },
    {
        "name": "CSS",
        "category": "technical",
        "weight": 5,
        "aliases": ["css", "css3"],
    },
    {
        "name": "JavaScript",
        "category": "technical",
        "weight": 5,
        "aliases": ["javascript", "js"],
    },
    {
        "name": "TypeScript",
        "category": "technical",
        "weight": 4,
        "aliases": ["typescript"],
    },
    {
        "name": "React",
        "category": "framework",
        "weight": 4,
        "aliases": ["react", "react.js", "reactjs"],
    },
    {
        "name": "Node.js",
        "category": "framework",
        "weight": 4,
        "aliases": ["node", "node.js", "nodejs"],
    },
    {
        "name": "Express",
        "category": "framework",
        "weight": 3,
        "aliases": ["express", "express.js"],
    },
    {
        "name": "REST APIs",
        "category": "technical",
        "weight": 3,
        "aliases": ["rest api", "rest apis", "restful api", "api", "apis"],
    },
    {
        "name": "Git",
        "category": "tooling",
        "weight": 3,
        "aliases": ["git", "github", "gitlab"],
    },
    {
        "name": "Version Control",
        "category": "tooling",
        "weight": 3,
        "aliases": ["version control", "git", "github", "gitlab"],
    },
    {
        "name": "Agile",
        "category": "methodology",
        "weight": 3,
        "aliases": ["agile", "scrum", "kanban"],
    },
    {
        "name": "Responsive Design",
        "category": "design",
        "weight": 4,
        "aliases": ["responsive", "responsive design", "responsive websites"],
    },
    {
        "name": "Web Design Principles",
        "category": "design",
        "weight": 3,
        "aliases": ["web design", "design principles", "ui", "ux"],
    },
    {
        "name": "Human-Computer Interaction",
        "category": "design",
        "weight": 2,
        "aliases": ["human-computer interaction", "hci"],
    },
    {
        "name": "Code Reviews",
        "category": "engineering",
        "weight": 2,
        "aliases": ["code reviews", "code review"],
    },
    {
        "name": "Problem Solving",
        "category": "soft_skills",
        "weight": 3,
        "aliases": ["problem solving", "problem-solving"],
    },
    {
        "name": "Communication",
        "category": "soft_skills",
        "weight": 3,
        "aliases": ["communication", "interpersonal"],
    },
    {
        "name": "Collaboration",
        "category": "soft_skills",
        "weight": 3,
        "aliases": ["collaborate", "collaboration", "team", "teamwork"],
    },
    {
        "name": "Attention to Detail",
        "category": "soft_skills",
        "weight": 2,
        "aliases": ["attention to detail", "detail oriented", "detail-oriented"],
    },
    {
        "name": "Troubleshooting",
        "category": "engineering",
        "weight": 2,
        "aliases": ["troubleshoot", "troubleshooting", "troubleshot", "debug", "debugging", "fix bugs", "fixed bugs", "resolved issues", "issue resolution"],
    },
    {
        "name": "SQL",
        "category": "technical",
        "weight": 4,
        "aliases": ["sql"],
    },
    {
        "name": "Frameworks and Libraries",
        "category": "technical",
        "weight": 2,
        "aliases": ["frameworks", "libraries", "framework", "library", "react", "node.js", "nodejs", "express", "wordpress", "plugins"],
    },
    {
        "name": "Web Technologies",
        "category": "technical",
        "weight": 4,
        "aliases": ["web technologies", "web development", "frontend", "website"],
    },
    {
        "name": "Excel",
        "category": "analytics",
        "weight": 3,
        "aliases": ["excel", "microsoft excel", "spreadsheets"],
    },
    {
        "name": "Reporting",
        "category": "analytics",
        "weight": 3,
        "aliases": ["reporting", "reports", "dashboards"],
    },
    {
        "name": "Data Analysis",
        "category": "analytics",
        "weight": 3,
        "aliases": ["data analysis", "analyze data", "analytics", "analysis"],
    },
    {
        "name": "Documentation",
        "category": "operations",
        "weight": 3,
        "aliases": ["documentation", "records", "record keeping"],
    },
    {
        "name": "Process Improvement",
        "category": "operations",
        "weight": 3,
        "aliases": ["process improvement", "improve processes", "operational efficiency", "workflow improvement"],
    },
    {
        "name": "Project Coordination",
        "category": "operations",
        "weight": 3,
        "aliases": ["project coordination", "coordinated projects", "project support", "scheduling"],
    },
    {
        "name": "Stakeholder Management",
        "category": "business",
        "weight": 3,
        "aliases": ["stakeholder management", "stakeholders", "cross-functional stakeholders"],
    },
    {
        "name": "Customer Support",
        "category": "customer",
        "weight": 4,
        "aliases": ["customer support", "customer service", "support tickets", "ticket resolution"],
    },
    {
        "name": "CRM",
        "category": "customer",
        "weight": 3,
        "aliases": ["crm", "salesforce", "hubspot", "customer relationship management"],
    },
    {
        "name": "Escalation Management",
        "category": "customer",
        "weight": 3,
        "aliases": ["escalation management", "escalations", "issue escalation"],
    },
    {
        "name": "Sales",
        "category": "sales",
        "weight": 3,
        "aliases": ["sales", "business development", "lead generation"],
    },
    {
        "name": "Negotiation",
        "category": "sales",
        "weight": 3,
        "aliases": ["negotiation", "negotiated", "closing deals"],
    },
    {
        "name": "Marketing",
        "category": "marketing",
        "weight": 3,
        "aliases": ["marketing", "digital marketing", "brand marketing"],
    },
    {
        "name": "SEO",
        "category": "marketing",
        "weight": 3,
        "aliases": ["seo", "search engine optimization"],
    },
    {
        "name": "Content Creation",
        "category": "marketing",
        "weight": 3,
        "aliases": ["content creation", "content writing", "content strategy"],
    },
    {
        "name": "Campaign Management",
        "category": "marketing",
        "weight": 3,
        "aliases": ["campaign management", "campaigns", "campaign execution"],
    },
    {
        "name": "Recruitment",
        "category": "people",
        "weight": 3,
        "aliases": ["recruitment", "recruiting", "talent acquisition"],
    },
    {
        "name": "Interview Coordination",
        "category": "people",
        "weight": 2,
        "aliases": ["interview coordination", "interview scheduling", "scheduled interviews"],
    },
    {
        "name": "HR Operations",
        "category": "people",
        "weight": 3,
        "aliases": ["hr operations", "human resources", "employee records", "onboarding"],
    },
    {
        "name": "Microsoft Office",
        "category": "admin",
        "weight": 3,
        "aliases": ["microsoft office", "ms office", "office suite"],
    },
    {
        "name": "Scheduling",
        "category": "admin",
        "weight": 3,
        "aliases": ["scheduling", "calendar management", "calendar coordination", "appointments"],
    },
    {
        "name": "Data Entry",
        "category": "admin",
        "weight": 2,
        "aliases": ["data entry", "entered data", "database entry"],
    },
    {
        "name": "Vendor Management",
        "category": "business",
        "weight": 3,
        "aliases": ["vendor management", "vendors", "supplier coordination", "supplier management"],
    },
    {
        "name": "Bookkeeping",
        "category": "finance",
        "weight": 3,
        "aliases": ["bookkeeping", "ledger management", "general ledger"],
    },
    {
        "name": "Accounts Payable",
        "category": "finance",
        "weight": 3,
        "aliases": ["accounts payable", "ap processing", "invoice processing"],
    },
    {
        "name": "Accounts Receivable",
        "category": "finance",
        "weight": 3,
        "aliases": ["accounts receivable", "ar", "billing collections"],
    },
    {
        "name": "Financial Reporting",
        "category": "finance",
        "weight": 4,
        "aliases": ["financial reporting", "financial reports", "monthly closing", "financial statements"],
    },
    {
        "name": "Budgeting",
        "category": "finance",
        "weight": 3,
        "aliases": ["budgeting", "budgets", "budget planning"],
    },
    {
        "name": "Forecasting",
        "category": "finance",
        "weight": 3,
        "aliases": ["forecasting", "forecasts", "financial planning"],
    },
    {
        "name": "Business Analysis",
        "category": "analytics",
        "weight": 4,
        "aliases": ["business analysis", "business analyst", "analyzed business requirements"],
    },
    {
        "name": "Requirements Gathering",
        "category": "business",
        "weight": 3,
        "aliases": ["requirements gathering", "gathered requirements", "requirement elicitation"],
    },
    {
        "name": "Presentation Skills",
        "category": "soft_skills",
        "weight": 2,
        "aliases": ["presentations", "presentation skills", "presented findings"],
    },
    {
        "name": "Research",
        "category": "analytics",
        "weight": 2,
        "aliases": ["research", "researched", "market research"],
    },
    {
        "name": "Compliance",
        "category": "operations",
        "weight": 3,
        "aliases": ["compliance", "regulatory compliance", "policy compliance"],
    },
]

LIBRARY_BY_NAME = {item["name"]: item for item in REQUIREMENT_LIBRARY}


SECTION_LABELS = ["skills", "experience", "projects", "education"]

SECTION_EVIDENCE_WEIGHTS = {
    "Skills": 0.74,
    "Experience": 1.0,
    "Projects": 0.94,
    "Education": 0.7,
}

JOB_SECTION_HINTS = {
    "requirements": [
        "job requirements",
        "requirements",
        "required skills",
        "must have",
        "qualification",
        "qualifications",
        "key skills",
    ],
    "responsibilities": [
        "roles and responsibility",
        "roles and responsibilities",
        "responsibilities",
        "what you will do",
        "duties",
    ],
    "preferred": [
        "preferred",
        "good to have",
        "nice to have",
        "preferred qualifications",
    ],
}

PRIORITY_PATTERNS = {
    "must_have": [
        r"\bmust\b",
        r"\brequired\b",
        r"\bneed(?:ed)?\b",
        r"\bproficiency in\b",
        r"\bstrong understanding of\b",
        r"\bexpertise in\b",
    ],
    "core": [
        r"\bexperience with\b",
        r"\bfamiliarity with\b",
        r"\bability to\b",
        r"\bdevelop\b",
        r"\bdesign\b",
        r"\bbuild\b",
        r"\bwrite\b",
        r"\btroubleshoot\b",
        r"\bversion control\b",
    ],
    "preferred": [
        r"\bnice to have\b",
        r"\bpreferred\b",
        r"\bbonus\b",
        r"\bplus\b",
    ],
}

GENERIC_REQUIREMENT_PATTERNS = [
    r"(?:proficiency in|experience with|strong understanding of|familiarity with|knowledge of|expertise in)\s+([^\.:\n]+)",
    r"(?:ability to|responsible for|responsibilities include|roles and responsibility|roles and responsibilities)\s+([^\.:\n]+)",
]

GENERIC_CATEGORY_RULES = [
    ("methodology", ["agile", "scrum", "kanban", "workflow"]),
    ("design", ["design", "ux", "ui", "interaction"]),
    ("tooling", ["git", "github", "version control", "tool", "tools"]),
    ("soft_skills", ["communication", "collaboration", "team", "interpersonal", "detail", "problem solving"]),
    ("engineering", ["troubleshoot", "debug", "review", "testing", "code quality"]),
    ("analytics", ["excel", "report", "dashboard", "analytics", "analysis", "data"]),
    ("operations", ["documentation", "process", "operations", "workflow", "coordination", "scheduling"]),
    ("customer", ["customer", "support", "ticket", "crm", "escalation", "service"]),
    ("sales", ["sales", "lead", "pipeline", "negotiation", "client acquisition"]),
    ("marketing", ["marketing", "seo", "campaign", "content", "branding"]),
    ("people", ["recruitment", "hiring", "onboarding", "interview", "hr"]),
    ("business", ["stakeholder", "cross-functional", "business", "vendor"]),
    ("admin", ["office", "scheduling", "calendar", "data entry", "administrative", "appointments"]),
    ("finance", ["finance", "financial", "budget", "forecast", "payable", "receivable", "bookkeeping", "invoice"]),
]


DOMAIN_CATEGORY_MAP = {
    "tech": {"technical", "framework", "tooling", "engineering", "design", "methodology"},
    "operations": {"operations", "admin", "business", "analytics"},
    "customer": {"customer", "soft_skills", "business"},
    "marketing": {"marketing", "analytics", "business", "soft_skills"},
    "sales": {"sales", "business", "soft_skills", "analytics"},
    "finance": {"finance", "analytics", "business"},
    "people": {"people", "business", "soft_skills", "admin"},
}

STOP_PHRASES = {
    "other web technologies",
    "industry standards",
    "latest web development trends",
    "overall code quality",
    "official channels",
}

QUALITY_CHECKS = [
    {
        "id": "contact_email",
        "label": "Email present",
        "weight": 2,
    },
    {
        "id": "contact_phone",
        "label": "Phone number present",
        "weight": 2,
    },
    {
        "id": "skills_section",
        "label": "Skills section present",
        "weight": 3,
    },
    {
        "id": "experience_section",
        "label": "Experience section present",
        "weight": 4,
    },
    {
        "id": "projects_section",
        "label": "Projects section present",
        "weight": 2,
    },
    {
        "id": "education_section",
        "label": "Education section present",
        "weight": 2,
    },
    {
        "id": "bullets",
        "label": "Bullet points used",
        "weight": 2,
    },
    {
        "id": "dates",
        "label": "Dates detected",
        "weight": 2,
    },
    {
        "id": "metrics",
        "label": "Quantified achievements",
        "weight": 3,
    },
]

GENERAL_ATS_CHECKS = [
    {
        "id": "name_header",
        "label": "Name appears in header",
        "weight": 5,
        "category": "Identity",
    },
    {
        "id": "contact_email",
        "label": "Email present",
        "weight": 5,
        "category": "Identity",
    },
    {
        "id": "professional_email",
        "label": "Professional email format",
        "weight": 3,
        "category": "Identity",
    },
    {
        "id": "contact_phone",
        "label": "Phone number present",
        "weight": 5,
        "category": "Identity",
    },
    {
        "id": "profile_link",
        "label": "LinkedIn or portfolio link present",
        "weight": 4,
        "category": "Identity",
    },
    {
        "id": "summary_section",
        "label": "Professional summary present",
        "weight": 4,
        "category": "Structure",
    },
    {
        "id": "clear_section_headings",
        "label": "Clear section headings",
        "weight": 7,
        "category": "Structure",
    },
    {
        "id": "skills_section",
        "label": "Skills section present",
        "weight": 7,
        "category": "Structure",
    },
    {
        "id": "experience_section",
        "label": "Experience section present",
        "weight": 9,
        "category": "Structure",
    },
    {
        "id": "education_section",
        "label": "Education section present",
        "weight": 5,
        "category": "Structure",
    },
    {
        "id": "section_order",
        "label": "Standard section order",
        "weight": 4,
        "category": "Structure",
    },
    {
        "id": "ats_safe_characters",
        "label": "ATS-safe character usage",
        "weight": 5,
        "category": "Parseability",
    },
    {
        "id": "low_table_risk",
        "label": "Low table or column risk",
        "weight": 5,
        "category": "Parseability",
    },
    {
        "id": "text_extractable",
        "label": "Text extraction is healthy",
        "weight": 6,
        "category": "Parseability",
    },
    {
        "id": "no_repeated_headers",
        "label": "No repeated headers or footers",
        "weight": 3,
        "category": "Parseability",
    },
    {
        "id": "keyword_density",
        "label": "Meaningful skills and keywords",
        "weight": 8,
        "category": "Searchability",
    },
    {
        "id": "hard_skill_depth",
        "label": "Enough concrete hard skills",
        "weight": 7,
        "category": "Searchability",
    },
    {
        "id": "skill_context",
        "label": "Skills backed by experience",
        "weight": 7,
        "category": "Searchability",
    },
    {
        "id": "title_signal",
        "label": "Target role or title signal",
        "weight": 4,
        "category": "Searchability",
    },
    {
        "id": "dates",
        "label": "Dates detected",
        "weight": 6,
        "category": "Chronology",
    },
    {
        "id": "date_month_precision",
        "label": "Month and year date precision",
        "weight": 3,
        "category": "Chronology",
    },
    {
        "id": "role_structure",
        "label": "Role, company, and date structure",
        "weight": 7,
        "category": "Chronology",
    },
    {
        "id": "chronology_coverage",
        "label": "Career timeline coverage",
        "weight": 5,
        "category": "Chronology",
    },
    {
        "id": "action_verbs",
        "label": "Action verbs in bullets",
        "weight": 7,
        "category": "Evidence",
    },
    {
        "id": "metrics",
        "label": "Quantified achievements",
        "weight": 9,
        "category": "Evidence",
    },
    {
        "id": "metric_density",
        "label": "Metrics distributed across bullets",
        "weight": 6,
        "category": "Evidence",
    },
    {
        "id": "outcome_language",
        "label": "Outcome-focused language",
        "weight": 5,
        "category": "Evidence",
    },
    {
        "id": "bullet_points",
        "label": "Bullet points used",
        "weight": 7,
        "category": "Readability",
    },
    {
        "id": "concise_bullets",
        "label": "Bullets are concise",
        "weight": 4,
        "category": "Readability",
    },
    {
        "id": "reasonable_length",
        "label": "Resume length is scannable",
        "weight": 6,
        "category": "Readability",
    },
    {
        "id": "no_objective",
        "label": "No outdated objective section",
        "weight": 4,
        "category": "Professionalism",
    },
    {
        "id": "no_first_person",
        "label": "No first-person resume language",
        "weight": 3,
        "category": "Professionalism",
    },
    {
        "id": "low_buzzword_risk",
        "label": "Low generic buzzword risk",
        "weight": 4,
        "category": "Professionalism",
    },
    {
        "id": "low_duplicate_risk",
        "label": "Low duplicate bullet risk",
        "weight": 4,
        "category": "Professionalism",
    },
]

GENERAL_ACTION_VERBS = {
    "achieved",
    "analyzed",
    "automated",
    "built",
    "collaborated",
    "coordinated",
    "created",
    "delivered",
    "designed",
    "developed",
    "drove",
    "improved",
    "implemented",
    "increased",
    "launched",
    "led",
    "managed",
    "optimized",
    "reduced",
    "resolved",
    "streamlined",
}

GENERAL_OUTCOME_TERMS = {
    "accelerated",
    "decreased",
    "delivered",
    "grew",
    "improved",
    "increased",
    "lowered",
    "optimized",
    "reduced",
    "saved",
    "streamlined",
}

GENERAL_BUZZWORDS = {
    "detail oriented",
    "dynamic",
    "fast paced",
    "go getter",
    "hard worker",
    "motivated",
    "passionate",
    "proactive",
    "results driven",
    "self starter",
    "team player",
}

GENERAL_ROLE_TITLE_PATTERN = (
    r"\b("
    r"accountant|administrator|analyst|assistant|associate|consultant|coordinator|"
    r"developer|designer|director|engineer|executive|intern|lead|manager|"
    r"marketer|officer|product owner|program manager|project manager|"
    r"representative|researcher|specialist|supervisor"
    r")\b"
)


def _normalize_text(text):
    return re.sub(r"\s+", " ", text.lower()).strip()


def _normalize_phrase(text):
    text = re.sub(r"[^\w\s/&+-]", " ", text.lower())
    text = re.sub(r"\s+", " ", text).strip(" ,.-")
    return text


def _contains_alias(text, alias):
    pattern = r"(?<!\w)" + re.escape(alias.lower()) + r"(?!\w)"
    return re.search(pattern, text) is not None


def _split_evidence_units(text):
    if not text:
        return []

    chunks = re.split(r"[\n\r]+|(?<=[\.\!\?])\s+", text)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _find_best_evidence(aliases, text):
    for unit in _split_evidence_units(text):
        normalized_unit = _normalize_text(unit)

        for alias in aliases:
            if _contains_alias(normalized_unit, alias):
                return unit

    return ""


def _extract_competency_set(text):
    normalized_text = _normalize_text(text or "")
    competencies = set()

    for requirement in REQUIREMENT_LIBRARY:
        if any(_contains_alias(normalized_text, alias) for alias in requirement["aliases"]):
            competencies.add(requirement["name"])

    return competencies


def _jaccard_competency_coverage(requirements, resume_text):
    required_competencies = {item["name"] for item in requirements}
    resume_competencies = _extract_competency_set(resume_text)

    if not required_competencies:
        return {
            "score": 0,
            "coverage_score": 0,
            "intersection": [],
            "required_only": [],
            "resume_only": sorted(resume_competencies),
            "required_count": 0,
            "resume_count": len(resume_competencies),
            "intersection_count": 0,
            "union_count": len(resume_competencies),
        }

    intersection = required_competencies & resume_competencies
    union = required_competencies | resume_competencies
    jaccard_score = len(intersection) / len(union) if union else 0
    coverage_score = len(intersection) / len(required_competencies)

    return {
        "score": jaccard_score,
        "coverage_score": coverage_score,
        "intersection": sorted(intersection),
        "required_only": sorted(required_competencies - resume_competencies),
        "resume_only": sorted(resume_competencies - required_competencies),
        "required_count": len(required_competencies),
        "resume_count": len(resume_competencies),
        "intersection_count": len(intersection),
        "union_count": len(union),
    }


def _extract_years(text):
    return [int(year) for year in re.findall(r"\b(19\d{2}|20\d{2})\b", text)]


def _extract_recentness_score(text):
    normalized = _normalize_text(text)

    if re.search(r"\b(present|current|now)\b", normalized):
        return 1.0

    years = _extract_years(text)

    if not years:
        return 0.65

    latest_year = max(years)
    age = max(0, CURRENT_YEAR - latest_year)

    if age <= 1:
        return 1.0

    if age <= 3:
        return 0.88

    if age <= 5:
        return 0.72

    return 0.62


def _extract_duration_score(text):
    years = sorted(set(_extract_years(text)))
    normalized = _normalize_text(text)

    if re.search(r"\b(\d+)\+?\s+years?\b", normalized):
        explicit_years = max(int(value) for value in re.findall(r"\b(\d+)\+?\s+years?\b", normalized))

        if explicit_years >= 3:
            return 1.0

        if explicit_years == 2:
            return 0.82

        return 0.68

    if len(years) >= 2:
        span = max(years) - min(years)

        if span >= 3:
            return 0.95

        if span >= 1:
            return 0.8

    if years:
        return 0.72

    return 0.68


def _evidence_quality_score(evidence):
    if not evidence:
        return 0

    normalized = _normalize_text(evidence)
    score = 0.45

    if re.search(r"\b(built|developed|designed|implemented|led|created|optimized|delivered|improved|launched|deployed)\b", normalized):
        score += 0.2

    if re.search(r"(\d+%|\d+\+|\$\d+|\d+\s*(users|clients|projects|features|days|months|years))", normalized):
        score += 0.2

    if len(normalized.split()) >= 8:
        score += 0.1

    return min(score, 1.0)


def _evidence_signal_score(section_name, evidence):
    section_score = SECTION_EVIDENCE_WEIGHTS.get(section_name, 0.75)
    quality_score = _evidence_quality_score(evidence)
    recency_score = _extract_recentness_score(evidence)
    duration_score = _extract_duration_score(evidence)

    combined = (
        section_score * 0.4 +
        quality_score * 0.3 +
        recency_score * 0.18 +
        duration_score * 0.12
    )

    return max(0.66, min(combined, 1.0)), recency_score, duration_score


def _proof_strength(score):
    if score >= 0.92:
        return "strong"

    if score >= 0.78:
        return "good"

    if score >= 0.62:
        return "fair"

    return "weak"


def _collect_matching_evidence(aliases, parsed_resume, resume_text):
    hits = []

    for section_name in SECTION_LABELS:
        section_content = parsed_resume.get(section_name, [])

        for item in section_content:
            if isinstance(item, dict):
                candidate_parts = []

                for value in item.values():
                    if isinstance(value, list):
                        candidate_parts.append(", ".join(str(entry) for entry in value if str(entry).strip()))
                    else:
                        candidate_parts.append(str(value).strip())

                candidate = ". ".join(part for part in candidate_parts if part)
            elif isinstance(item, list):
                candidate = ". ".join(str(entry).strip() for entry in item if str(entry).strip())
            else:
                candidate = str(item).strip()

            if not candidate:
                continue

            normalized_candidate = _normalize_text(candidate)

            if any(_contains_alias(normalized_candidate, alias) for alias in aliases):
                display_name = section_name.title()
                score, recency_score, duration_score = _evidence_signal_score(display_name, candidate)
                hits.append(
                    {
                        "section": display_name,
                        "text": candidate,
                        "score": score,
                        "recency_score": recency_score,
                        "duration_score": duration_score,
                    }
                )

    if not hits:
        fallback = _find_best_evidence(aliases, resume_text)

        if fallback:
            score, recency_score, duration_score = _evidence_signal_score("General", fallback)
            hits.append(
                {
                    "section": "General",
                    "text": fallback,
                    "score": score,
                    "recency_score": recency_score,
                    "duration_score": duration_score,
                }
            )

    return sorted(hits, key=lambda item: item["score"], reverse=True)


def _split_job_description_sections(job_description):
    sections = []
    current_section = "general"
    current_lines = []

    for raw_line in job_description.splitlines():
        line = raw_line.strip()

        if not line:
            continue

        normalized = _normalize_text(line)
        matched_section = None

        for section_name, hints in JOB_SECTION_HINTS.items():
            if any(hint in normalized for hint in hints):
                matched_section = section_name
                break

        if matched_section:
            if current_lines:
                sections.append((current_section, " ".join(current_lines)))
                current_lines = []

            current_section = matched_section
            continue

        current_lines.append(line)

    if current_lines:
        sections.append((current_section, " ".join(current_lines)))

    if not sections:
        sections.append(("general", job_description))

    return sections


def _infer_priority(section_name, sentence):
    normalized = _normalize_text(sentence)

    if section_name == "requirements":
        return "must_have"

    if section_name == "preferred":
        return "preferred"

    for priority, patterns in PRIORITY_PATTERNS.items():
        if any(re.search(pattern, normalized) for pattern in patterns):
            return priority

    if section_name == "responsibilities":
        return "core"

    return "supporting"


def _priority_weight(priority):
    return {
        "must_have": 1.45,
        "core": 1.2,
        "supporting": 1.0,
        "preferred": 0.8,
    }.get(priority, 1.0)


def _category_weight(category):
    return {
        "technical": 1.0,
        "framework": 0.98,
        "tooling": 0.88,
        "engineering": 0.82,
        "analytics": 0.9,
        "operations": 0.88,
        "customer": 0.88,
        "sales": 0.86,
        "marketing": 0.86,
        "people": 0.84,
        "business": 0.84,
        "admin": 0.84,
        "finance": 0.9,
        "design": 0.72,
        "methodology": 0.65,
        "soft_skills": 0.58,
    }.get(category, 0.7)


def _missing_penalty_factor(requirement):
    return _priority_weight(requirement.get("priority", "supporting")) * _category_weight(requirement["category"])


def _dominant_categories(requirements):
    category_weights = {}

    for requirement in requirements:
        category = requirement["category"]
        category_weights[category] = category_weights.get(category, 0) + requirement["weight"]

    if not category_weights:
        return set()

    ordered = sorted(category_weights.items(), key=lambda item: item[1], reverse=True)
    total_weight = sum(category_weights.values()) or 1
    dominant = {
        category
        for category, weight in ordered
        if weight / total_weight >= 0.15
    }

    dominant.update(category for category, _ in ordered[:2])
    return dominant


def _primary_domain(requirements):
    domain_scores = {}

    for domain, categories in DOMAIN_CATEGORY_MAP.items():
        domain_scores[domain] = sum(
            requirement["weight"]
            for requirement in requirements
            if requirement["category"] in categories
        )

    if not domain_scores:
        return "general"

    return max(domain_scores.items(), key=lambda item: item[1])[0]


def _role_importance_factor(requirement, dominant_categories, primary_domain):
    category = requirement["category"]
    priority = requirement.get("priority", "supporting")
    primary_categories = DOMAIN_CATEGORY_MAP.get(primary_domain, set())

    if category in primary_categories and category in dominant_categories:
        factor = 1.12
    elif category in primary_categories:
        factor = 0.96
    elif category in dominant_categories:
        factor = 0.88
    else:
        factor = 0.62

    if priority == "must_have":
        factor *= 1.08
    elif priority == "core":
        factor *= 1.02
    elif priority == "preferred":
        factor *= 0.78
    elif category not in dominant_categories:
        factor *= 0.9

    if category in {"soft_skills", "methodology"} and category not in primary_categories:
        factor *= 0.82

    return factor




def _requires_recency(priority, source_section, sentence_text):
    normalized = _normalize_text(sentence_text)

    if re.search(r"\b(recent|currently|current|latest|modern)\b", normalized):
        return True

    return priority in {"must_have", "core"} and source_section in {"requirements", "responsibilities"}


def _gap_severity(requirement):
    severity_score = _priority_weight(requirement.get("priority", "supporting")) * _category_weight(requirement["category"])

    if severity_score >= 1.15:
        return "core blocker"

    if severity_score >= 0.8:
        return "important gap"

    return "bonus gap"


def _generic_category(phrase):
    normalized = _normalize_phrase(phrase)

    for category, terms in GENERIC_CATEGORY_RULES:
        if any(term in normalized for term in terms):
            return category

    return "technical"


def _canonical_requirement_name(phrase):
    normalized = _normalize_phrase(phrase)

    mapping = {
        "html": "HTML",
        "css": "CSS",
        "javascript": "JavaScript",
        "js": "JavaScript",
        "typescript": "TypeScript",
        "node js": "Node.js",
        "node": "Node.js",
        "nodejs": "Node.js",
        "react js": "React",
        "reactjs": "React",
        "git": "Git",
        "sql": "SQL",
        "excel": "Excel",
        "reporting": "Reporting",
        "ms office": "Microsoft Office",
        "office suite": "Microsoft Office",
        "appointments": "Scheduling",
        "api": "REST APIs",
        "apis": "REST APIs",
        "rest api": "REST APIs",
        "rest": "REST APIs",
        "rest apis": "REST APIs",
        "express": "Express",
        "microsoft excel": "Excel",
        "reports": "Reporting",
        "dashboards": "Reporting",
        "analytics": "Data Analysis",
        "analysis": "Data Analysis",
        "documented": "Documentation",
        "stakeholders": "Stakeholder Management",
        "customer service": "Customer Support",
        "crm": "CRM",
        "salesforce": "CRM",
        "hubspot": "CRM",
        "seo": "SEO",
        "campaigns": "Campaign Management",
        "recruiting": "Recruitment",
        "talent acquisition": "Recruitment",
        "human resources": "HR Operations",
        "vendors": "Vendor Management",
        "financial reports": "Financial Reporting",
        "financial statements": "Financial Reporting",
        "budgets": "Budgeting",
        "forecasts": "Forecasting",
        "business analyst": "Business Analysis",
        "presentations": "Presentation Skills",
        "researched": "Research",
    }

    return mapping.get(normalized, normalized.title())


def _generic_weight(phrase, priority):
    base = 3 if len(_normalize_phrase(phrase).split()) <= 3 else 2
    return max(2, min(6, round(base * _priority_weight(priority))))


def _split_requirement_phrase(phrase):
    normalized = _normalize_phrase(phrase)

    if not normalized or normalized in STOP_PHRASES:
        return []

    parts = re.split(r",|/|\band\b|\bor\b", normalized)
    cleaned = []

    for part in parts:
        item = _normalize_phrase(part)

        if not item or len(item) < 3:
            continue

        if item in STOP_PHRASES:
            continue

        cleaned.append(item)

    return cleaned


def _boost_requirement(requirement, priority, section_name):
    boosted = dict(requirement)
    base_weight = requirement["weight"]
    boosted["priority"] = priority
    boosted["source_section"] = section_name
    boosted["recency_required"] = False
    category_adjusted = base_weight * _category_weight(requirement["category"])
    boosted["weight"] = max(2, min(7, round(category_adjusted * _priority_weight(priority))))
    return boosted


def extract_job_requirements(job_description):
    sections = _split_job_description_sections(job_description)
    requirements = {}

    for section_name, block in sections:
        sentences = re.split(r"(?<=[\.\!\?])\s+|(?<=:)\s+", block)

        for sentence in sentences:
            if not sentence.strip():
                continue

            priority = _infer_priority(section_name, sentence)
            normalized_sentence = _normalize_text(sentence)

            for requirement in REQUIREMENT_LIBRARY:
                if any(_contains_alias(normalized_sentence, alias) for alias in requirement["aliases"]):
                    existing = requirements.get(requirement["name"])
                    boosted = _boost_requirement(requirement, priority, section_name)
                    boosted["recency_required"] = _requires_recency(
                        priority,
                        section_name,
                        sentence
                    )

                    if not existing or boosted["weight"] > existing["weight"]:
                        requirements[requirement["name"]] = boosted

            for pattern in GENERIC_REQUIREMENT_PATTERNS:
                for match in re.findall(pattern, normalized_sentence):
                    for phrase in _split_requirement_phrase(match):
                        if phrase in STOP_PHRASES:
                            continue

                        if any(
                            _contains_alias(phrase, alias)
                            for item in REQUIREMENT_LIBRARY
                            for alias in item["aliases"]
                        ):
                            continue

                        name = _canonical_requirement_name(phrase)
                        existing = requirements.get(name)
                        candidate = {
                            "name": name,
                            "category": _generic_category(phrase),
                            "weight": _generic_weight(phrase, priority),
                            "aliases": [phrase],
                            "priority": priority,
                            "source_section": section_name,
                            "recency_required": _requires_recency(
                                priority,
                                section_name,
                                sentence
                            ),
                        }

                        if not existing or candidate["weight"] > existing["weight"]:
                            requirements[name] = candidate

    for skill in detect_skills_from_text(job_description):
        canonical_name = _canonical_requirement_name(skill)

        if canonical_name not in requirements:
            library_item = LIBRARY_BY_NAME.get(canonical_name)

            if library_item:
                requirements[canonical_name] = {
                    "name": library_item["name"],
                    "category": library_item["category"],
                    "weight": max(2, library_item["weight"] - 1),
                    "aliases": library_item["aliases"],
                    "priority": "supporting",
                    "source_section": "general",
                    "recency_required": False,
                }
                continue

            requirements[canonical_name] = {
                "name": canonical_name,
                "category": _generic_category(skill),
                "weight": 2,
                "aliases": [skill],
                "priority": "supporting",
                "source_section": "general",
                "recency_required": False,
            }

    return sorted(
        requirements.values(),
        key=lambda item: (-item["weight"], item["name"])
    )


def _match_requirement(requirement, resume_text, parsed_resume):
    normalized_resume = _normalize_text(resume_text)
    matched_alias = None
    found_in_sections = []

    for alias in requirement["aliases"]:
        if _contains_alias(normalized_resume, alias):
            matched_alias = alias
            break

    for section_name in SECTION_LABELS:
        section_content = parsed_resume.get(section_name, [])
        section_text = " ".join(str(item) for item in section_content)
        normalized_section = _normalize_text(section_text)

        if any(_contains_alias(normalized_section, alias) for alias in requirement["aliases"]):
            found_in_sections.append(section_name.title())

    if matched_alias:
        evidence_hits = _collect_matching_evidence(
            requirement["aliases"],
            parsed_resume,
            resume_text
        )
        best_hit = evidence_hits[0] if evidence_hits else None
        evidence = best_hit["text"] if best_hit else ""
        confidence = best_hit["score"] if best_hit else 0.78
        if requirement.get("recency_required") and best_hit:
            confidence *= best_hit["recency_score"]
        proof_strength = _proof_strength(confidence)
        recent = bool(best_hit and best_hit["recency_score"] >= 0.88)
        duration_signal = int(round((best_hit["duration_score"] if best_hit else 0.45) * 100))

        return {
            "name": requirement["name"],
            "category": requirement["category"],
            "weight": requirement["weight"],
            "priority": requirement.get("priority", "supporting"),
            "matched": True,
            "matched_alias": matched_alias,
            "evidence": evidence,
            "sections": found_in_sections,
            "confidence": confidence,
            "proof_strength": proof_strength,
            "recent_evidence": recent,
            "duration_signal": duration_signal,
        }

    return {
        "name": requirement["name"],
        "category": requirement["category"],
        "weight": requirement["weight"],
        "priority": requirement.get("priority", "supporting"),
        "matched": False,
        "matched_alias": "",
        "evidence": "",
        "sections": [],
        "confidence": 0,
        "proof_strength": "missing",
        "recent_evidence": False,
        "duration_signal": 0,
    }


def _safe_similarity(left_text, right_text):
    if not left_text.strip() or not right_text.strip():
        return 0

    left_embedding = model.encode([left_text])[0]
    right_embedding = model.encode([right_text])[0]

    return float(cosine_similarity([left_embedding], [right_embedding])[0][0])


def _extract_requirement_contexts(job_description):
    lowered = _normalize_text(job_description)
    contexts = []

    patterns = [
        r"(?:proficiency in|experience with|strong understanding of|familiarity with)\s+([^\.]+)",
        r"(?:ability to|responsible for)\s+([^\.]+)",
    ]

    for pattern in patterns:
        contexts.extend(match.strip() for match in re.findall(pattern, lowered))

    return contexts


def _compute_quality_checks(resume_text, parsed_resume):
    checks = []
    normalized_resume = _normalize_text(resume_text)
    lines = [line.strip() for line in resume_text.splitlines() if line.strip()]
    bullet_count = sum(1 for line in lines if re.match(r"^[-*•]", line))

    rules = {
        "contact_email": bool(re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", resume_text, re.I)),
        "contact_phone": bool(re.search(r"(\+?\d[\d\s().-]{7,}\d)", resume_text)),
        "skills_section": bool(parsed_resume.get("skills")),
        "experience_section": bool(parsed_resume.get("experience")),
        "projects_section": bool(parsed_resume.get("projects")),
        "education_section": bool(parsed_resume.get("education")),
        "bullets": bullet_count >= 3,
        "dates": bool(re.search(r"(20\d{2}|19\d{2}|present|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", normalized_resume)),
        "metrics": bool(re.search(r"(\d+%|\d+\+|\$\d+|\d+\s*(users|clients|projects|features|days|months|years))", normalized_resume)),
    }

    total_weight = 0
    passed_weight = 0

    for definition in QUALITY_CHECKS:
        passed = rules[definition["id"]]
        total_weight += definition["weight"]

        if passed:
            passed_weight += definition["weight"]

        checks.append(
            {
                "id": definition["id"],
                "label": definition["label"],
                "passed": passed,
                "weight": definition["weight"],
            }
        )

    return checks, (passed_weight / total_weight if total_weight else 0)


def _resume_lines(resume_text):
    return [line.strip() for line in resume_text.splitlines() if line.strip()]


def _count_bullets(lines):
    return sum(1 for line in lines if re.match(r"^[-*•]", line))


def _bullet_lines(lines):
    return [line for line in lines if re.match(r"^[-*•]", line)]


def _word_count(text):
    return len(re.findall(r"\b\w+\b", text))


def _stringify_section_item(item):
    if isinstance(item, dict):
        parts = []

        for value in item.values():
            if isinstance(value, list):
                parts.extend(str(entry).strip() for entry in value if str(entry).strip())
            else:
                value = str(value).strip()

                if value:
                    parts.append(value)

        return " ".join(parts)

    if isinstance(item, list):
        return " ".join(str(entry).strip() for entry in item if str(entry).strip())

    return str(item).strip()


def _section_text(parsed_resume, section_name):
    return " ".join(
        text
        for text in (_stringify_section_item(item) for item in parsed_resume.get(section_name, []))
        if text
    )


def _extract_email(resume_text):
    match = re.search(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", resume_text, re.I)
    return match.group(0) if match else ""


def _has_phone(resume_text):
    return bool(re.search(r"(\+?\d[\d\s().-]{7,}\d)", resume_text))


def _has_name_header(lines):
    heading_words = {
        "summary",
        "profile",
        "skills",
        "experience",
        "education",
        "projects",
        "resume",
        "curriculum vitae",
    }

    for line in lines[:6]:
        normalized = _normalize_text(line)

        if not normalized or normalized in heading_words:
            continue

        if "@" in line or re.search(r"\d", line) or re.search(r"https?://|linkedin|github", normalized):
            continue

        words = re.findall(r"[A-Za-z][A-Za-z'.-]*", line)

        if 2 <= len(words) <= 5 and len(line) <= 70:
            return True

    return False


def _is_professional_email(email):
    if not email:
        return False

    local = email.split("@", 1)[0].lower()
    risky_terms = {"baby", "boss", "cool", "cute", "gamer", "hot", "princess", "rockstar", "xoxo"}

    if any(term in local for term in risky_terms):
        return False

    return len(local) >= 4 and not re.search(r"^\d+$", local)


def _has_profile_link(resume_text):
    normalized = _normalize_text(resume_text)
    return bool(
        re.search(r"\blinkedin\.com/in/|\bgithub\.com/|\bportfolio\b|\bhttps?://", normalized)
    )


def _section_heading_positions(resume_text):
    positions = {}
    heading_aliases = {
        "summary": ["summary", "professional summary", "profile"],
        "skills": ["skills", "technical skills", "core skills", "key skills", "technologies"],
        "experience": ["experience", "work experience", "professional experience", "employment history", "internship", "internships"],
        "projects": ["projects", "project", "personal projects", "academic projects"],
        "education": ["education", "academic background", "qualification", "qualifications"],
    }

    for index, line in enumerate(_resume_lines(resume_text)):
        normalized = re.sub(r"[^a-z\s]", "", line.lower()).strip()

        for section_name, aliases in heading_aliases.items():
            if normalized in aliases and section_name not in positions:
                positions[section_name] = index

    return positions


def _has_clear_section_headings(resume_text, parsed_resume):
    parsed_sections = sum(
        1 for section in ["skills", "experience", "projects", "education"]
        if parsed_resume.get(section)
    )
    heading_hits = len(
        re.findall(
            r"(?im)^\s*(summary|profile|skills|technical skills|experience|work experience|professional experience|projects|education|certifications)\s*$",
            resume_text,
        )
    )
    return parsed_sections >= 3 or heading_hits >= 3


def _has_summary_section(resume_text, parsed_resume):
    if parsed_resume.get("summary"):
        return True

    return bool(
        re.search(r"(?im)^\s*(summary|professional summary|profile)\s*$", resume_text)
    )


def _has_standard_section_order(resume_text, parsed_resume):
    positions = _section_heading_positions(resume_text)

    if not positions:
        return _has_clear_section_headings(resume_text, parsed_resume)

    if "skills" in positions and "experience" in positions and positions["skills"] > positions["experience"]:
        return False

    if "education" in positions and "experience" in positions and positions["education"] < positions["experience"]:
        return False

    return True


def _uses_ats_safe_characters(resume_text):
    risky_symbols = len(re.findall(r"[■□◆◇●○★☆✓✔✕✖→⇒]", resume_text))
    decorative_lines = len(re.findall(r"(?m)^[=_~\-]{5,}$", resume_text))
    return risky_symbols <= 2 and decorative_lines <= 2


def _has_low_table_risk(lines):
    if not lines:
        return False

    table_like = sum(
        1
        for line in lines
        if "|" in line or "\t" in line or len(re.findall(r"\s{3,}", line)) >= 2
    )

    return table_like / len(lines) <= 0.16


def _has_healthy_text_extraction(lines, word_count):
    if not lines:
        return 0

    average_line_length = sum(len(line) for line in lines) / len(lines)
    very_long_lines = sum(1 for line in lines if len(line) > 180)
    long_line_penalty = min(0.3, very_long_lines / max(1, len(lines)))
    line_shape_score = 1 if average_line_length <= 110 else max(0.35, 110 / average_line_length)

    score = (
        min(1, word_count / 280) * 0.52 +
        min(1, len(lines) / 14) * 0.26 +
        line_shape_score * 0.22
    )

    return max(0, min(1, score - long_line_penalty))


def _has_low_repeated_header_risk(lines):
    normalized_lines = [
        re.sub(r"\s+", " ", re.sub(r"\d+", "", line.lower())).strip()
        for line in lines
    ]
    repeated = [
        line for line in set(normalized_lines)
        if line and len(line) > 8 and normalized_lines.count(line) >= 3
    ]
    footer_patterns = sum(
        1 for line in normalized_lines
        if re.search(r"\bpage\b|\bconfidential\b", line)
    )

    return len(repeated) == 0 and footer_patterns <= 1


def _resume_keyword_signal(resume_text):
    detected_skills = detect_skills_from_text(resume_text)
    normalized = _normalize_text(resume_text)
    role_terms = re.findall(
        r"\b(?:analysis|analytics|automation|budgeting|campaign|compliance|customer|dashboard|design|development|documentation|engineering|finance|forecasting|management|marketing|operations|project|reporting|research|sales|support|testing|workflow)\b",
        normalized,
    )
    return len(set(detected_skills)) + len(set(role_terms))


def _skills_with_experience_context(resume_text, parsed_resume, detected_skills):
    experience_context = " ".join(
        [
            _section_text(parsed_resume, "experience"),
            _section_text(parsed_resume, "projects"),
        ]
    )
    normalized_context = _normalize_text(experience_context or resume_text)
    contextualized = []

    for skill in detected_skills:
        if _contains_alias(normalized_context, skill):
            contextualized.append(skill)

    return contextualized


def _has_title_signal(resume_text, parsed_resume):
    top_text = " ".join(_resume_lines(resume_text)[:10])
    experience_text = _section_text(parsed_resume, "experience")
    return bool(
        re.search(GENERAL_ROLE_TITLE_PATTERN, _normalize_text(top_text))
        or re.search(GENERAL_ROLE_TITLE_PATTERN, _normalize_text(experience_text))
    )


def _has_month_precision(resume_text):
    normalized = _normalize_text(resume_text)
    return bool(
        re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+20\d{2}\b", normalized)
        or re.search(r"\b(0?[1-9]|1[0-2])[/.-]20\d{2}\b", normalized)
    )


def _has_role_structure(resume_text, parsed_resume):
    experience_text = _section_text(parsed_resume, "experience")
    target_text = experience_text or resume_text
    normalized = _normalize_text(target_text)
    has_title = bool(re.search(GENERAL_ROLE_TITLE_PATTERN, normalized))
    has_date = bool(re.search(r"\b(19\d{2}|20\d{2}|present|current)\b", normalized))
    has_company_signal = bool(re.search(r"\b(at|company|inc|llc|ltd|corp|corporation|pvt|private limited)\b", normalized))

    return has_title and has_date and (has_company_signal or bool(parsed_resume.get("experience")))


def _chronology_coverage_score(resume_text, parsed_resume):
    experience_text = _section_text(parsed_resume, "experience")
    target_text = experience_text or resume_text
    years = sorted(set(_extract_years(target_text)))

    if not years:
        return 0

    latest_year = max(years)
    recent_score = 1 if latest_year >= CURRENT_YEAR - 2 else 0.75 if latest_year >= CURRENT_YEAR - 5 else 0.45
    span_score = 1 if len(years) >= 2 else 0.62

    if re.search(r"\b(present|current)\b", _normalize_text(target_text)):
        recent_score = 1

    return min(1, recent_score * 0.65 + span_score * 0.35)


def _metric_count(text):
    return len(
        re.findall(
            r"(\d+%|\d+\+|\$\d+|\d+\s*(users|clients|customers|projects|features|tickets|days|months|years|hours|reports|revenue|costs|stakeholders|team members|transactions))",
            _normalize_text(text),
        )
    )


def _action_verb_ratio(lines):
    bullets = _bullet_lines(lines)

    if not bullets:
        return 0

    action_bullets = 0

    for line in bullets:
        cleaned = re.sub(r"^[-*•]\s*", "", line.lower())
        first_word = re.sub(r"[^a-z]", "", cleaned.split(" ", 1)[0] if cleaned else "")

        if first_word in GENERAL_ACTION_VERBS:
            action_bullets += 1

    return action_bullets / len(bullets)


def _metric_density_score(resume_text, lines):
    bullets = _bullet_lines(lines)
    metrics = _metric_count(resume_text)

    if not bullets:
        return min(1, metrics / 3)

    return min(1, metrics / max(3, round(len(bullets) * 0.35)))


def _has_outcome_language(resume_text):
    normalized = _normalize_text(resume_text)
    return any(re.search(rf"\b{term}\b", normalized) for term in GENERAL_OUTCOME_TERMS)


def _concise_bullet_score(lines):
    bullets = _bullet_lines(lines)

    if not bullets:
        return 0

    word_counts = [_word_count(re.sub(r"^[-*•]\s*", "", bullet)) for bullet in bullets]
    healthy = sum(1 for count in word_counts if 6 <= count <= 32)
    very_long = sum(1 for count in word_counts if count > 42)

    return max(0, healthy / len(bullets) - (very_long / len(bullets) * 0.35))


def _has_first_person_language(resume_text):
    return bool(re.search(r"\b(i|me|my|mine|myself)\b", _normalize_text(resume_text)))


def _buzzword_density_score(resume_text):
    normalized = _normalize_text(resume_text)
    buzzword_hits = sum(1 for term in GENERAL_BUZZWORDS if re.search(rf"\b{re.escape(term)}\b", normalized))
    evidence_hits = _metric_count(resume_text) + len(re.findall(r"\b(built|created|implemented|improved|reduced|delivered|managed|led)\b", normalized))

    if buzzword_hits == 0:
        return 1

    return max(0, min(1, (evidence_hits + 1) / (buzzword_hits * 3)))


def _duplicate_bullet_score(lines):
    bullets = _bullet_lines(lines)

    if len(bullets) < 3:
        return 1

    normalized_bullets = [
        re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\s]", "", bullet.lower())).strip()
        for bullet in bullets
    ]
    unique_count = len(set(normalized_bullets))

    return unique_count / len(normalized_bullets)


def _score_from_rule(value):
    if isinstance(value, bool):
        return 1 if value else 0

    return max(0, min(float(value), 1))


def _compute_general_ats_checks(resume_text, parsed_resume):
    checks = []
    normalized_resume = _normalize_text(resume_text)
    lines = _resume_lines(resume_text)
    word_count = _word_count(resume_text)
    bullet_count = _count_bullets(lines)
    keyword_signal = _resume_keyword_signal(resume_text)
    email = _extract_email(resume_text)
    detected_skills = sorted(set(detect_skills_from_text(resume_text)))
    contextualized_skills = _skills_with_experience_context(resume_text, parsed_resume, detected_skills)
    chronology_score = _chronology_coverage_score(resume_text, parsed_resume)
    metric_density_score = _metric_density_score(resume_text, lines)
    concise_bullet_score = _concise_bullet_score(lines)
    buzzword_score = _buzzword_density_score(resume_text)
    duplicate_bullet_score = _duplicate_bullet_score(lines)
    skill_context_score = (
        len(contextualized_skills) / max(3, len(detected_skills))
        if detected_skills else 0
    )

    rules = {
        "name_header": _has_name_header(lines),
        "contact_email": bool(email),
        "professional_email": _is_professional_email(email),
        "contact_phone": _has_phone(resume_text),
        "profile_link": _has_profile_link(resume_text),
        "summary_section": _has_summary_section(resume_text, parsed_resume),
        "skills_section": bool(parsed_resume.get("skills")),
        "experience_section": bool(parsed_resume.get("experience")),
        "education_section": bool(parsed_resume.get("education")),
        "clear_section_headings": _has_clear_section_headings(resume_text, parsed_resume),
        "section_order": _has_standard_section_order(resume_text, parsed_resume),
        "ats_safe_characters": _uses_ats_safe_characters(resume_text),
        "low_table_risk": _has_low_table_risk(lines),
        "text_extractable": _has_healthy_text_extraction(lines, word_count),
        "no_repeated_headers": _has_low_repeated_header_risk(lines),
        "keyword_density": keyword_signal >= 7,
        "hard_skill_depth": len(detected_skills) >= 5,
        "skill_context": skill_context_score,
        "title_signal": _has_title_signal(resume_text, parsed_resume),
        "dates": bool(re.search(r"(20\d{2}|19\d{2}|present|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)", normalized_resume)),
        "date_month_precision": _has_month_precision(resume_text),
        "role_structure": _has_role_structure(resume_text, parsed_resume),
        "chronology_coverage": chronology_score,
        "action_verbs": _action_verb_ratio(lines),
        "metrics": _metric_count(resume_text) >= 1,
        "metric_density": metric_density_score,
        "outcome_language": _has_outcome_language(resume_text),
        "bullet_points": bullet_count >= 4,
        "concise_bullets": concise_bullet_score,
        "reasonable_length": 250 <= word_count <= 1200,
        "no_objective": not re.search(r"(?im)^\s*objective\s*$|\bcareer objective\b", resume_text),
        "no_first_person": not _has_first_person_language(resume_text),
        "low_buzzword_risk": buzzword_score,
        "low_duplicate_risk": duplicate_bullet_score,
    }

    total_weight = 0
    passed_weight = 0

    for definition in GENERAL_ATS_CHECKS:
        score = _score_from_rule(rules[definition["id"]])
        passed = score >= 0.68
        total_weight += definition["weight"]
        passed_weight += definition["weight"] * score

        checks.append(
            {
                "id": definition["id"],
                "label": definition["label"],
                "passed": passed,
                "weight": definition["weight"],
                "category": definition["category"],
                "score": int(round(score * 100)),
            }
        )

    profile = {
        "word_count": word_count,
        "line_count": len(lines),
        "bullet_count": bullet_count,
        "metric_count": _metric_count(resume_text),
        "detected_skills": len(detected_skills),
        "contextualized_skills": len(contextualized_skills),
        "action_verb_ratio": int(round(_action_verb_ratio(lines) * 100)),
        "metric_density": int(round(metric_density_score * 100)),
        "chronology_coverage": int(round(chronology_score * 100)),
        "duplicate_bullet_score": int(round(duplicate_bullet_score * 100)),
    }

    return checks, (passed_weight / total_weight if total_weight else 0), profile


def _score_check_group(checks, category):
    grouped = [check for check in checks if check["category"] == category]
    total = sum(check["weight"] for check in grouped) or 1
    score = sum(check["weight"] * ((check.get("score", 0) or 0) / 100) for check in grouped)
    return score / total


def _general_strengths_and_priorities(checks):
    strengths = []
    priorities = []

    message_by_id = {
        "name_header": "Put your full name at the top in plain text so parsers can identify the candidate record cleanly.",
        "contact_email": "Add a professional email address so ATS systems can capture your contact details.",
        "professional_email": "Use a simple professional email address based on your name.",
        "contact_phone": "Add a phone number in plain text so recruiters can contact you quickly.",
        "profile_link": "Add a LinkedIn, GitHub, portfolio, or relevant professional profile link.",
        "summary_section": "Add a short professional summary that frames your role, domain, and strongest evidence.",
        "skills_section": "Add a dedicated skills section with role-relevant tools, methods, and domain keywords.",
        "experience_section": "Add a clear experience section so your work history is easy to parse.",
        "education_section": "Add education details with degree, school, and dates where appropriate.",
        "clear_section_headings": "Use standard headings like Summary, Skills, Experience, Projects, and Education.",
        "section_order": "Use a conventional order so parsers and recruiters can scan from profile to skills, experience, and education.",
        "ats_safe_characters": "Reduce decorative symbols, icons, and separators that can confuse resume parsers.",
        "low_table_risk": "Avoid tables, text boxes, heavy columns, and tab-separated layouts that often scramble ATS extraction.",
        "text_extractable": "Increase clean resume text and avoid image-only or overly compressed layouts.",
        "no_repeated_headers": "Remove repeated page headers, footers, and page labels that can pollute parsed resume text.",
        "keyword_density": "Add more meaningful role keywords and concrete tools that reflect your actual background.",
        "hard_skill_depth": "Add more concrete tools, platforms, methods, or domain skills that describe what you can actually do.",
        "skill_context": "Repeat important skills inside experience or project bullets so they are backed by evidence.",
        "title_signal": "Add a clear target title or current professional title near the top of the resume.",
        "dates": "Include dates for roles, education, certifications, or projects so the timeline is credible.",
        "date_month_precision": "Use month and year date ranges for roles when possible, such as Jan 2024 - Present.",
        "role_structure": "Make each role easy to parse with job title, company, location if useful, and date range.",
        "chronology_coverage": "Make the timeline clear enough to understand recent work and career progression.",
        "action_verbs": "Start more bullets with strong action verbs such as built, led, improved, managed, or delivered.",
        "metrics": "Add measurable outcomes such as percentages, volume, cost, time, users, tickets, or revenue.",
        "metric_density": "Spread metrics across more bullets instead of having only one isolated number.",
        "outcome_language": "Use outcome verbs such as improved, reduced, increased, saved, optimized, or delivered.",
        "bullet_points": "Use concise bullets under roles and projects instead of dense paragraph blocks.",
        "concise_bullets": "Keep bullets short enough to scan, usually one line or a tight two-line statement.",
        "reasonable_length": "Keep the resume scannable, usually one to two pages for most candidates.",
        "no_objective": "Replace old-style objective language with a short professional summary.",
        "no_first_person": "Remove first-person phrasing like I, me, or my; resume bullets should be direct and professional.",
        "low_buzzword_risk": "Replace generic buzzwords with concrete responsibilities, tools, metrics, and outcomes.",
        "low_duplicate_risk": "Avoid repeated bullets; each bullet should add a distinct accomplishment or responsibility.",
    }

    for check in sorted(checks, key=lambda item: (-item["weight"], item["label"])):
        score = (check.get("score", 0) or 0) / 100
        item = {
            "name": check["label"],
            "category": check["category"],
            "weight": check["weight"],
            "priority": "core" if check["weight"] >= 7 else "supporting",
            "matched": check["passed"],
            "sections": [check["category"]],
            "confidence": score if check["passed"] else 0,
            "proof_strength": _proof_strength(score) if check["passed"] else "missing",
            "recent_evidence": False,
            "duration_signal": check.get("score", 0),
            "evidence": (
                f"{check['label']} is already working in this resume with a {check.get('score', 100)}% signal."
                if check["passed"]
                else message_by_id.get(check["id"], f"Improve {check['label'].lower()} for stronger ATS readability.")
            ),
        }

        if check["passed"]:
            strengths.append(item)
        else:
            priorities.append(item)

    return strengths, priorities


def _enterprise_risk_flags(checks):
    flags = []
    risk_map = {
        "text_extractable": ("Parser extraction risk", "critical", 45),
        "low_table_risk": ("Layout parsing risk", "high", 68),
        "contact_email": ("Missing email", "critical", 68),
        "contact_phone": ("Missing phone", "high", 68),
        "experience_section": ("Missing experience section", "critical", 68),
        "role_structure": ("Weak work-history structure", "high", 68),
        "skill_context": ("Skills lack evidence context", "high", 50),
        "metrics": ("Missing measurable outcomes", "high", 68),
        "low_duplicate_risk": ("Repeated bullet risk", "medium", 68),
        "low_buzzword_risk": ("Generic language risk", "medium", 68),
    }
    by_id = {check["id"]: check for check in checks}

    for check_id, (label, severity, threshold) in risk_map.items():
        check = by_id.get(check_id)

        if check and check.get("score", 0) < threshold:
            flags.append(
                {
                    "label": label,
                    "severity": severity,
                    "message": check["label"],
                    "score": check.get("score", 0),
                }
            )

    return flags


def build_general_ats_breakdown(resume_text, parsed_resume):
    checks, overall_readiness, profile = _compute_general_ats_checks(resume_text, parsed_resume)
    strengths, priorities = _general_strengths_and_priorities(checks)
    detected_skills = sorted(set(detect_skills_from_text(resume_text)))
    normalized_resume = _normalize_text(resume_text)
    lines = _resume_lines(resume_text)
    bullet_count = _count_bullets(lines)
    word_count = _word_count(resume_text)
    risk_flags = _enterprise_risk_flags(checks)

    subscores = {
        "parser_readiness": int(
            (
                _score_check_group(checks, "Identity") * 0.3 +
                _score_check_group(checks, "Structure") * 0.34 +
                _score_check_group(checks, "Parseability") * 0.36
            ) * 100
        ),
        "format_readiness": int(_score_check_group(checks, "Parseability") * 100),
        "section_strength": int(
            (
                _score_check_group(checks, "Identity") * 0.28 +
                _score_check_group(checks, "Structure") * 0.72
            ) * 100
        ),
        "readability": int(_score_check_group(checks, "Readability") * 100),
        "impact": int(_score_check_group(checks, "Evidence") * 100),
        "searchability": int(_score_check_group(checks, "Searchability") * 100),
        "chronology": int(_score_check_group(checks, "Chronology") * 100),
        "professionalism": int(_score_check_group(checks, "Professionalism") * 100),
        "content_depth": int(
            (
                _score_check_group(checks, "Searchability") * 0.48 +
                _score_check_group(checks, "Chronology") * 0.2 +
                _score_check_group(checks, "Evidence") * 0.32
            ) * 100
        ),
        "credibility": int(
            (
                _score_check_group(checks, "Identity") * 0.3 +
                _score_check_group(checks, "Chronology") * 0.3 +
                _score_check_group(checks, "Evidence") * 0.22 +
                _score_check_group(checks, "Professionalism") * 0.18
            ) * 100
        ),
    }

    overall_score = int(round(
        (
            subscores["parser_readiness"] * 0.2 +
            subscores["searchability"] * 0.18 +
            subscores["impact"] * 0.18 +
            subscores["chronology"] * 0.14 +
            subscores["readability"] * 0.12 +
            subscores["professionalism"] * 0.1 +
            subscores["credibility"] * 0.08
        )
    ))

    if risk_flags:
        critical_count = sum(1 for flag in risk_flags if flag["severity"] == "critical")
        high_count = sum(1 for flag in risk_flags if flag["severity"] == "high")
        overall_score = max(0, overall_score - critical_count * 6 - high_count * 3)

    overall_score = max(0, min(100, overall_score))
    explanation_cards = []

    for item in priorities[:5]:
        explanation_cards.append(
            {
                "title": item["name"],
                "type": "missing",
                "severity": "high impact" if item["weight"] >= 7 else "recommended",
                "message": item["evidence"],
            }
        )

    for flag in risk_flags[:3]:
        explanation_cards.append(
            {
                "title": flag["label"],
                "type": "missing" if flag["severity"] in {"critical", "high"} else "weak_evidence",
                "severity": flag["severity"],
                "message": f"{flag['message']} is creating an enterprise ATS risk signal.",
            }
        )

    if bullet_count < 4:
        explanation_cards.append(
            {
                "title": "Bullet readability",
                "type": "weak_evidence",
                "severity": "needs stronger proof",
                "message": "ATS and recruiters scan bullets faster than paragraphs. Convert dense role descriptions into short impact bullets.",
            }
        )

    if not re.search(r"(\d+%|\d+\+|\$\d+)", normalized_resume):
        explanation_cards.append(
            {
                "title": "Measurable impact",
                "type": "weak_evidence",
                "severity": "needs stronger proof",
                "message": "The resume needs more measurable outcomes so achievements read as evidence instead of responsibilities.",
            }
        )

    category_summary = {}

    for check in checks:
        bucket = category_summary.setdefault(
            check["category"],
            {"matched": 0, "total": 0, "score": 0}
        )
        bucket["total"] += 1
        bucket["score"] += check.get("score", 0)

        if check["passed"]:
            bucket["matched"] += 1

    for bucket in category_summary.values():
        bucket["score"] = int(round(bucket["score"] / bucket["total"])) if bucket["total"] else 0

    enterprise_profile = {
        "parser_confidence": subscores["parser_readiness"],
        "searchability_score": subscores["searchability"],
        "chronology_score": subscores["chronology"],
        "evidence_score": subscores["impact"],
        "readability_score": subscores["readability"],
        "professionalism_score": subscores["professionalism"],
        "overall_readiness": int(round(overall_readiness * 100)),
        "risk_flags": risk_flags,
        "diagnostics": {
            "words": profile["word_count"],
            "lines": profile["line_count"],
            "bullets": profile["bullet_count"],
            "metrics": profile["metric_count"],
            "detected_skills": profile["detected_skills"],
            "contextualized_skills": profile["contextualized_skills"],
            "action_verb_ratio": profile["action_verb_ratio"],
            "metric_density": profile["metric_density"],
            "chronology_coverage": profile["chronology_coverage"],
            "duplicate_bullet_score": profile["duplicate_bullet_score"],
        },
    }

    return {
        "overall_score": overall_score,
        "subscores": subscores,
        "requirements": strengths + priorities,
        "matched_requirements": strengths,
        "missing_requirements": priorities,
        "category_summary": category_summary,
        "primary_domain": "general",
        "quality_checks": checks,
        "keyword_matched": detected_skills[:18],
        "keyword_missing": [
            item["name"]
            for item in priorities
            if item["category"] in {"Searchability", "Evidence", "Structure", "Chronology"}
        ][:8],
        "explanation_cards": explanation_cards[:8],
        "enterprise_profile": enterprise_profile,
        "resume_stats": {
            "word_count": word_count,
            "bullet_count": bullet_count,
            "detected_skills": len(detected_skills),
            "risk_flags": len(risk_flags),
        },
    }


def build_ats_breakdown(job_description, resume_text, parsed_resume):
    requirements = extract_job_requirements(job_description)
    dominant_categories = _dominant_categories(requirements)
    primary_domain = _primary_domain(requirements)
    jd_contexts = _extract_requirement_contexts(job_description)
    matches = [
        _match_requirement(requirement, resume_text, parsed_resume)
        for requirement in requirements
    ]

    total_weight = sum(item["weight"] for item in matches) or 1
    matched_weight = sum(
        item["weight"]
        * _role_importance_factor(item, dominant_categories, primary_domain)
        * max(
            item["confidence"],
            0.74 if item["category"] in DOMAIN_CATEGORY_MAP.get(primary_domain, set()) else 0.66
        )
        for item in matches
        if item["matched"]
    )
    weighted_total = sum(
        item["weight"] * _role_importance_factor(item, dominant_categories, primary_domain)
        if item["matched"]
        else item["weight"] * _role_importance_factor(item, dominant_categories, primary_domain) * _missing_penalty_factor(item)
        for item in matches
    ) or total_weight
    requirement_score = matched_weight / weighted_total if weighted_total else 0

    technical_job_skills = [
        item["name"].lower()
        for item in requirements
        if item["category"] in {"technical", "framework", "tooling"}
    ]

    section_score = compute_section_scores(parsed_resume, technical_job_skills)
    keyword_list = extract_important_keywords(job_description, top_n=15)
    keyword_score, keyword_matched, keyword_missing = keyword_match_score(
        keyword_list,
        resume_text
    )
    competency_coverage = _jaccard_competency_coverage(requirements, resume_text)
    competency_score = (
        competency_coverage["coverage_score"] * 0.7 +
        competency_coverage["score"] * 0.3
    )

    experience_text = " ".join(str(item) for item in parsed_resume.get("experience", []))
    projects_text = " ".join(str(item) for item in parsed_resume.get("projects", []))
    evidence_text = " ".join(filter(None, [experience_text, projects_text, resume_text]))
    experience_score = _safe_similarity(job_description, evidence_text)
    quality_checks, format_score = _compute_quality_checks(resume_text, parsed_resume)
    context_score = _safe_similarity(
        " ".join(jd_contexts),
        resume_text
    ) if jd_contexts else 0

    matched_requirements = sorted(
        [item for item in matches if item["matched"]],
        key=lambda item: (-item["weight"], -item["confidence"], item["name"])
    )
    missing_requirements = sorted(
        [item for item in matches if not item["matched"]],
        key=lambda item: (-item["weight"], item["name"])
    )
    evidence_score = (
        sum(item["confidence"] for item in matched_requirements)
        / len(matched_requirements)
        if matched_requirements else 0
    )
    requirement_signal = requirement_score * 0.9 + competency_score * 0.1

    overall_score = int(
        (
            requirement_signal * 0.4 +
            section_score * 0.15 +
            keyword_score * 0.15 +
            experience_score * 0.15 +
            format_score * 0.1 +
            context_score * 0.05 +
            evidence_score * 0.1
        ) * 100
    )

    category_summary = {}

    for item in matches:
        category = item["category"]
        bucket = category_summary.setdefault(
            category,
            {"matched": 0, "total": 0}
        )
        bucket["total"] += 1

        if item["matched"]:
            bucket["matched"] += 1

    weak_evidence = [
        item for item in matched_requirements
        if item["confidence"] < 0.86 or "Skills" in item.get("sections", [])
    ]

    explanation_cards = []

    for item in missing_requirements[:4]:
        explanation_cards.append(
            {
                "title": item["name"],
                "type": "missing",
                "severity": _gap_severity(item),
                "message": (
                    f"{item['name']} is not clearly evidenced in your resume yet. "
                    f"This reads as a {_gap_severity(item)} for this job."
                ),
            }
        )

    for item in weak_evidence[:3]:
        sections = ", ".join(item.get("sections", [])) or "general resume content"
        explanation_cards.append(
            {
                "title": item["name"],
                "type": "weak_evidence",
                "severity": "needs stronger proof",
                "message": (
                    f"{item['name']} is present, but the strongest evidence is mainly in {sections}. "
                    "Add clearer project or experience proof if you have it."
                ),
            }
        )

    return {
        "overall_score": overall_score,
        "subscores": {
            "requirements": int(requirement_signal * 100),
            "requirement_match": int(requirement_score * 100),
            "competency_coverage": int(competency_score * 100),
            "section_strength": int(section_score * 100),
            "keyword_alignment": int(keyword_score * 100),
            "experience_relevance": int(experience_score * 100),
            "format_readiness": int(format_score * 100),
            "jd_context_alignment": int(context_score * 100),
            "evidence_strength": int(evidence_score * 100),
        },
        "requirements": matches,
        "matched_requirements": matched_requirements,
        "missing_requirements": missing_requirements,
        "category_summary": category_summary,
        "primary_domain": primary_domain,
        "quality_checks": quality_checks,
        "competency_coverage": {
            **competency_coverage,
            "score": int(competency_coverage["score"] * 100),
            "coverage_score": int(competency_coverage["coverage_score"] * 100),
            "blended_score": int(competency_score * 100),
        },
        "keyword_matched": keyword_matched,
        "keyword_missing": keyword_missing,
        "explanation_cards": explanation_cards,
    }
