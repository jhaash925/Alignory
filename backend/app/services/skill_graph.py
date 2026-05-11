SKILL_GRAPH = {

    "node": ["node.js","express","backend","rest api"],

    "react": ["javascript","frontend","ui","spa"],

    "mongodb": ["database","nosql"],

    "sql": ["mysql","postgresql","database"],

    "javascript": ["js","frontend","web development"],

}


def expand_skill_graph(skill):

    skill = skill.lower()

    if skill in SKILL_GRAPH:

        return [skill] + SKILL_GRAPH[skill]

    return [skill]