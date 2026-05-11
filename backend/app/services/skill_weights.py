# backend/app/services/skill_weights.py

SKILL_WEIGHTS = {

    # core frontend
    "javascript": 5,
    "react": 5,
    "typescript": 5,

    # backend
    "node": 5,
    "express": 4,
    "python": 4,
    "java": 4,

    # web fundamentals
    "html": 3,
    "css": 3,

    # databases
    "mongodb": 4,
    "mysql": 4,
    "postgresql": 4,
    "sql": 4,
    "nosql": 3,

    # tooling
    "git": 2,
    "github": 2,

    # APIs
    "api": 3,
    "rest": 3
}


def get_skill_weight(skill):
    """
    Returns importance weight of a skill.
    Default weight = 1 if not defined.
    """

    return SKILL_WEIGHTS.get(skill, 1)