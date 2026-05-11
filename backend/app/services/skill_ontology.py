# Maps JD skills to equivalent or related terms that might appear in resumes

SKILL_ONTOLOGY = {
    "node.js": ["node", "nodejs"],
    "express.js": ["express"],
    "rest api": ["rest apis", "restful api", "api integration"],
    "mysql": ["sql", "database"],
    "postgresql": ["sql", "database"],
    "mongodb": ["mongo"],
    "react.js": ["react"],
    "javascript": ["js", "ecmascript"]
}


def expand_skill(skill):

    skill = skill.lower()

    related = SKILL_ONTOLOGY.get(skill, [])

    return [skill] + related