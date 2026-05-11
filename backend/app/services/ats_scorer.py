from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# -----------------------------
# EXPERIENCE RELEVANCE
# -----------------------------

def experience_relevance(job_description, experience_chunks):

    if not experience_chunks:
        return 0

    job_embedding = model.encode([job_description])

    exp_embeddings = model.encode(experience_chunks)

    similarities = cosine_similarity(job_embedding, exp_embeddings)[0]

    return float(np.mean(similarities))


# -----------------------------
# PROJECT RELEVANCE
# -----------------------------

def project_relevance(job_description, resume_text):

    job_embedding = model.encode([job_description])
    resume_embedding = model.encode([resume_text])

    similarity = cosine_similarity(job_embedding, resume_embedding)[0][0]

    return float(similarity)


# -----------------------------
# KEYWORD DENSITY
# -----------------------------

def keyword_density(job_skills, resume_text):

    if not job_skills:
        return 0

    resume_text = resume_text.lower()

    matches = 0

    for skill in job_skills:
        if skill.lower() in resume_text:
            matches += 1

    return matches / len(job_skills)


# -----------------------------
# FINAL ATS SCORE
# -----------------------------

def compute_final_ats_score(
    skill_score,
    exp_score,
    project_score,
    keyword_score
):

    final_score = (
        skill_score * 0.40 +
        exp_score * 0.25 +
        project_score * 0.20 +
        keyword_score * 0.15
    )

    return int(final_score * 100)