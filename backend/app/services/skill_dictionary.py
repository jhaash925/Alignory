import re

# --------------------------------
# KNOWN TECH SKILLS
# --------------------------------

KNOWN_TECH_SKILLS = {
    "javascript",
    "react",
    "node",
    "express",
    "html",
    "css",
    "tailwind",
    "bootstrap",
    "mongodb",
    "mysql",
    "postgresql",
    "sql",
    "nosql",
    "git",
    "rest",
    "api",
    "python",
    "java",
    "typescript",
    "docker",
    "aws",
    "azure",
    "gcp",
    "kubernetes",
    "redux",
    "next",
    "vite",
    "linux",
    "excel",
    "reporting",
    "documentation",
    "crm",
    "seo",
    "marketing",
    "recruitment",
    "customer support",
    "data analysis",
    "microsoft office",
    "scheduling",
    "data entry",
    "bookkeeping",
    "accounts payable",
    "accounts receivable",
    "financial reporting",
    "budgeting",
    "forecasting",
    "business analysis",
    "requirements gathering",
    "research",
    "compliance",
    "vendor management"
}


# --------------------------------
# SKILL PATTERNS
# --------------------------------

SKILL_PATTERNS = {

    "html": r"\bhtml5?\b",
    "css": r"\bcss3?\b",

    "javascript": r"\bjavascript\b|\bjs\b",

    "node": r"\bnode\.?js\b|\bnode\b",

    "react": r"\breact\.?js\b|\breact\b",

    "express": r"\bexpress\.?js\b|\bexpress\b",

    "git": r"\bgit\b|\bgithub\b",

    "sql": r"\bsql\b",
    "mysql": r"\bmysql\b",
    "postgresql": r"\bpostgresql\b|\bpostgres\b",
    "mongodb": r"\bmongodb\b",

    "rest": r"\brest\b|\brest api\b|\brestful\b",

    "api": r"\bapi\b",

    "python": r"\bpython\b",
    "java": r"\bjava\b",

    "typescript": r"\btypescript\b",

    "docker": r"\bdocker\b",
    "aws": r"\baws\b",
    "azure": r"\bazure\b",
    "gcp": r"\bgcp\b",

    "kubernetes": r"\bkubernetes\b",

    "redux": r"\bredux\b",

    "next": r"\bnext\.?js\b|\bnext\b",

    "vite": r"\bvite\b",

    "linux": r"\blinux\b",

    "excel": r"\bexcel\b|\bmicrosoft excel\b",
    "reporting": r"\breporting\b|\bdashboards\b",
    "documentation": r"\bdocumentation\b|\brecord keeping\b",
    "crm": r"\bcrm\b|\bsalesforce\b|\bhubspot\b",
    "seo": r"\bseo\b|\bsearch engine optimization\b",
    "marketing": r"\bmarketing\b|\bdigital marketing\b",
    "recruitment": r"\brecruitment\b|\brecruiting\b|\btalent acquisition\b",
    "customer support": r"\bcustomer support\b|\bcustomer service\b|\bsupport tickets\b",
    "data analysis": r"\bdata analysis\b|\banalytics\b",
    "microsoft office": r"\bmicrosoft office\b|\bms office\b|\boffice suite\b",
    "scheduling": r"\bscheduling\b|\bcalendar management\b|\bappointments\b",
    "data entry": r"\bdata entry\b",
    "bookkeeping": r"\bbookkeeping\b|\bgeneral ledger\b|\bledger management\b",
    "accounts payable": r"\baccounts payable\b|\bap processing\b|\binvoice processing\b",
    "accounts receivable": r"\baccounts receivable\b|\bar\b|\bbilling collections\b",
    "financial reporting": r"\bfinancial reporting\b|\bfinancial reports\b|\bfinancial statements\b",
    "budgeting": r"\bbudgeting\b|\bbudgets\b|\bbudget planning\b",
    "forecasting": r"\bforecasting\b|\bforecasts\b|\bfinancial planning\b",
    "business analysis": r"\bbusiness analysis\b|\bbusiness analyst\b",
    "requirements gathering": r"\brequirements gathering\b|\bgathered requirements\b",
    "research": r"\bresearch\b|\bmarket research\b",
    "compliance": r"\bcompliance\b|\bregulatory compliance\b",
    "vendor management": r"\bvendor management\b|\bvendors\b|\bsupplier coordination\b"
}


# --------------------------------
# DETECT SKILLS FROM TEXT
# --------------------------------

def detect_skills_from_text(text):

    text = text.lower()

    detected = []

    for skill, pattern in SKILL_PATTERNS.items():

        if re.search(pattern, text):

            detected.append(skill)

    return list(set(detected))
