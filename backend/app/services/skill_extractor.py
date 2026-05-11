import ollama
import json
import re


def extract_skills_llm(text):

    prompt = f"""
Extract all technical skills from the text.

Return ONLY a JSON list.

Example:
["React","Node.js","MongoDB","REST API","HTML","CSS"]

Text:
{text}
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response["message"]["content"]

    try:
        skills = json.loads(content)

        cleaned = []

        for skill in skills:

            # split combined skills
            parts = re.split(r",|and|/", skill)

            for p in parts:
                p = p.strip()
                if p:
                    cleaned.append(p.lower())

        return list(set(cleaned))

    except:
        return []