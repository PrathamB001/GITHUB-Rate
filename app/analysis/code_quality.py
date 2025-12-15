import re
import json
from app.llm.qwen_client import get_qwen_client


def analyze_code_quality(code_snippet):
    client = get_qwen_client()

    prompt = f"""
You are a senior software engineer reviewing code quality.

Evaluate ONLY on:
1. Readability
2. Function size
3. Error handling
4. Separation of concerns

Return JSON ONLY:
{{
  "score": "0-10",
  "strengths": [],
  "issues": [],
  "actionable_fixes": []
}}

Code:
{code_snippet[:3500]}
"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a senior software engineer reviewing code quality."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,
        temperature=0.2
    )

    text = response.choices[0].message.content

    match = re.search(r"\{.*\}", text, re.S)

    if not match:
        return {"error": "LLM output invalid"}

    return json.loads(match.group())





