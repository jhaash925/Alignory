from app.services.skill_dictionary import detect_skills_from_text
from app.services.skill_normalizer import normalize_skill_list
from app.services.skill_utils import canonicalize_list


SECTION_WEIGHTS = {
    "skills": 1.0,
    "experience": 0.8,
    "projects": 0.7
}


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


def score_section(section_text, job_skills):

    detected = detect_skills_from_text(section_text)

    detected = normalize_skill_list(detected)

    detected = canonicalize_list(detected)

    matched = [s for s in job_skills if s in detected]

    if not job_skills:
        return 0

    return len(matched) / len(job_skills)


def compute_section_scores(parsed_resume, job_skills):

    skills_section = normalize_section(parsed_resume.get("skills", []))
    experience_section = normalize_section(parsed_resume.get("experience", []))
    projects_section = normalize_section(parsed_resume.get("projects", []))

    skills_text = " ".join(skills_section)
    experience_text = " ".join(experience_section)
    projects_text = " ".join(projects_section)

    skills_score = score_section(skills_text, job_skills)
    experience_score = score_section(experience_text, job_skills)
    projects_score = score_section(projects_text, job_skills)

    weighted_score = (
        skills_score * SECTION_WEIGHTS["skills"] +
        experience_score * SECTION_WEIGHTS["experience"] +
        projects_score * SECTION_WEIGHTS["projects"]
    ) / sum(SECTION_WEIGHTS.values())

    return weighted_score