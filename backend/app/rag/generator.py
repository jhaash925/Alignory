import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"


def generate_resume_text(job_description, resume_context):

    prompt = f"""
You are an advanced ATS resume analyzer and resume writer.

Analyze the candidate resume against the job description.

Job Description:
{job_description}

Candidate Resume:
{resume_context}

Tasks:

1. Calculate ATS score from 0–100 based on relevance.
2. List matched skills.
3. List missing skills.
4. Explain briefly why the score was given.
5. Rewrite the resume so it better matches the job description.

Return the response strictly in this JSON format:

{{
"ats_score": number,
"matched_skills": [],
"missing_skills": [],
"analysis": "",
"improved_resume": ""
}}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()["response"]

    return result