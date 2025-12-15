import re
import json
from app.llm.qwen_client import get_qwen_client


def analyze_structure(file_tree_summary: str):
    client = get_qwen_client()

    prompt = f"""
Evaluate the repository structure based ONLY on:
1. Folder organization
2. Separation of concerns
3. Entry point clarity
4. Scalability of structure

Do NOT:
- Comment on code style
- Suggest new features
- Assume missing files

Return JSON ONLY:
{{
  "structure_score": "0-10",
  "strengths": [],
  "issues": [],
  "suggestions": []
}}

Repository structure:
{file_tree_summary}
"""

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a senior software engineer reviewing repository structure."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=350,
        temperature=0.2
    )

    text = response.choices[0].message.content

    match = re.search(r"\{.*?\}", text, re.S)
    if not match:
        return {
            "error": "LLM output invalid",
            "raw_output": text
        }

    result = json.loads(match.group())

    score = result.get("structure_score", "")
    if isinstance(score, str) and "-" in score:
        result["structure_score"] = score.split("-")[0]

    return result
