import re

from sklearn.feature_extraction.text import TfidfVectorizer


NOISY_KEYWORDS = {
    "job",
    "jobs",
    "role",
    "roles",
    "responsibility",
    "responsibilities",
    "requirement",
    "requirements",
    "skills",
    "skill",
    "description",
}


TECH_TOKENS = {
    "html",
    "css",
    "javascript",
    "typescript",
    "react",
    "node",
    "express",
    "mongodb",
    "mysql",
    "postgresql",
    "sql",
    "git",
    "api",
    "apis",
    "web",
    "frontend",
    "backend",
}


def _normalize_text(text):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text.lower())).strip()


def _split_terms(keyword):
    return [term for term in _normalize_text(keyword).split() if term]


def _is_noisy_keyword(keyword):
    terms = _split_terms(keyword)

    if not terms:
        return True

    if len(terms) == 1 and terms[0] in NOISY_KEYWORDS:
        return True

    return False


def _should_skip_phrase(keyword, kept_keywords):
    terms = _split_terms(keyword)

    if len(terms) < 2:
        return False

    if all(term in TECH_TOKENS for term in terms):
        return True

    kept_terms = {_normalize_text(item) for item in kept_keywords}

    if all(term in kept_terms for term in terms):
        return True

    return False


# --------------------------------
# IMPORTANT KEYWORD EXTRACTION
# --------------------------------

def extract_important_keywords(job_description, top_n=20):

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1,2)
    )

    tfidf_matrix = vectorizer.fit_transform([job_description])

    feature_names = vectorizer.get_feature_names_out()

    scores = tfidf_matrix.toarray()[0]

    keyword_scores = list(zip(feature_names, scores))

    keyword_scores = sorted(
        keyword_scores,
        key=lambda x: x[1],
        reverse=True
    )

    top_keywords = []

    for keyword, _ in keyword_scores:
        normalized_keyword = _normalize_text(keyword)

        if not normalized_keyword:
            continue

        if _is_noisy_keyword(normalized_keyword):
            continue

        if normalized_keyword in top_keywords:
            continue

        if _should_skip_phrase(normalized_keyword, top_keywords):
            continue

        top_keywords.append(normalized_keyword)

        if len(top_keywords) >= top_n:
            break

    return top_keywords


# --------------------------------
# KEYWORD MATCH SCORE
# --------------------------------

def keyword_match_score(keywords, resume_text):

    resume_lower = _normalize_text(resume_text)

    matched = []

    missing = []

    for keyword in keywords:

        normalized_keyword = _normalize_text(keyword)
        keyword_terms = _split_terms(normalized_keyword)

        exact_match = normalized_keyword in resume_lower
        token_match = keyword_terms and all(
            re.search(rf"(?<!\w){re.escape(term)}(?!\w)", resume_lower)
            for term in keyword_terms
        )

        if exact_match or token_match:

            matched.append(normalized_keyword)

        else:

            missing.append(normalized_keyword)

    if len(keywords) == 0:

        score = 0

    else:

        score = len(matched) / len(keywords)

    return score, matched, missing
