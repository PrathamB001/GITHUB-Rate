import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(score: int, level: str, features: dict):
    prompt = f"""
You are an honest and strict coding mentor.

Repository evaluation:
Score: {score}
Level: {level}
Extracted features: {features}

Tasks:
1. Write a concise 2-line summary of the repository quality.
2. Provide a 5-step actionable improvement roadmap.
Use bullet points for the roadmap.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    text = response.choices[0].message.content.strip().splitlines()

    summary = text[0]
    roadmap = [
        line.lstrip("-• ").strip()
        for line in text
        if line.strip().startswith(("-", "•"))
    ]

    return summary, roadmap
