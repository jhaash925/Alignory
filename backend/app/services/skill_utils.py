# skill_utils.py

SKILL_CANONICAL = {

    "node.js": "node",
    "nodejs": "node",
    "reactjs": "react",
    "react.js": "react",

    "rest api": "rest",
    "restful api": "rest",

    "github": "git",

    "html5": "html",
    "css3": "css",

    "postgres": "postgresql",
    "postgre": "postgresql",
}


def canonicalize(skill):

    s = skill.lower().strip()

    return SKILL_CANONICAL.get(s, s)


def canonicalize_list(skills):

    return list(set([canonicalize(s) for s in skills]))