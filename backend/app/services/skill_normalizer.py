import re

def clean_skill(skill):

    skill = skill.lower().strip()

    # remove brackets
    skill = re.sub(r"\(.*?\)", "", skill)

    # remove punctuation
    skill = re.sub(r"[^\w\s\.]", "", skill)

    return skill.strip()


def normalize_skill(skill):

    skill = clean_skill(skill)

    mapping = {
        "node.js": "node",
        "nodejs": "node",
        "express.js": "express",
        "rest apis": "rest api",
        "restful api": "rest api",
        "html5": "html",
        "css3": "css",
        "javascript es6": "javascript",
        "js": "javascript"
    }

    return mapping.get(skill, skill)


def normalize_skill_list(skills):

    normalized = []

    for skill in skills:
        normalized.append(normalize_skill(skill))

    return list(set(normalized))