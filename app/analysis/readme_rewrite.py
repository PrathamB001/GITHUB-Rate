from app.llm.qwen_client import get_qwen_client


def rewrite_readme(readme_text: str):
    client = get_qwen_client()

    prompt = f"""
Rewrite this README to be clearer and more professional.

Include:
- Short description
- Installation
- Usage
- Limitations
- Future improvements

Do NOT add fake features.
Do NOT invent results or benchmarks.

README:
{readme_text[:3500]}
"""

    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an expert open-source maintainer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.3
    )

    return response.choices[0].message.content
