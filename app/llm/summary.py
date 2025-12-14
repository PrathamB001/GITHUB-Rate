import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client ONCE at module load
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_summary(score: int, level: str, features: dict):
    prompt = f"""
You are a strict coding mentor.

Repository evaluation:
Score: {score}
Level: {level}
Extracted features: {features}

Rules:
- Only suggest improvements that correspond to missing or weak signals.
- If tests are missing, suggest tests.
- If CI is missing, suggest CI.
- If commits are sparse, suggest commit hygiene.
- If structure is weak, suggest restructuring.
- DO NOT suggest generic advice.

Return ONLY valid JSON in this exact schema:

{{
  "summary": "<short paragraph>",
  "roadmap": [
    "<actionable improvement step 1>",
    "<actionable improvement step 2>",
    "<actionable improvement step 3>"
  ]
}}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=300
    )

    raw = response.choices[0].message.content.strip()

    print("\n=== LLM RAW SUMMARY OUTPUT ===")
    print(raw)
    print("=== END LLM OUTPUT ===\n")

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        return (
            "Summary generation failed due to malformed LLM output.",
            []
        )

    summary = data.get("summary", "").strip()
    roadmap = data.get("roadmap", [])

    if not isinstance(roadmap, list):
        roadmap = []

    roadmap = [step for step in roadmap if isinstance(step, str) and step.strip()]

    return summary, roadmap