import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_keywords_from_repo(description: str, readme_text: str) -> dict:
    """
    Extract GitHub-search-optimized keywords.
    LLM may internally reason in categories, but MUST output final keywords only.
    """

    prompt = f"""
You are an expert GitHub project analyst.

Your goal is to generate KEYWORDS that will WORK WELL with GitHub Search.

You may internally think in categories like:
- domain keywords
- functional keywords
- secondary context keywords

But you must OUTPUT ONLY the FINAL keywords that should be used
DIRECTLY in GitHub repository search.

Repository Description:
{description or "No description"}

README excerpt:
{readme_text[:3500]}

Format (OUTPUT EXACTLY THIS JSON):

{{
  "summary": "One short sentence describing what the project does",
  "keywords": ["keyword1", "keyword2", "keyword3", "keyword4"]
}}

Rules:
- Return 3 to 5 keywords ONLY
- Keywords must be concrete phrases likely to appear in GitHub repos
- Use lowercase
- Use hyphens instead of spaces
- Keywords should represent DOMAIN + PURPOSE
- NEVER include generic or tooling words:
  streamlit, flask, django, react, ml, ai, model, app, tool, framework, api, python
- If multiple categories are possible, choose the ONE set
  that best represents what someone would name a similar repo
- If keywords are not explicitly present, INFER realistic repo-style names
- Output ONLY valid JSON, nothing else
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=150
        )

        data = json.loads(response.choices[0].message.content.strip())

        keywords = [
            k.lower().strip().replace(" ", "-")
            for k in data.get("keywords", [])
            if isinstance(k, str) and len(k) > 3
        ]

        if len(keywords) < 3:
            raise ValueError("Too few keywords")

        return {
            "summary": data.get("summary", ""),
            "keywords": keywords[:5]
        }

    except Exception:
        return {
            "summary": description[:100] or "Software project",
            "keywords": ["software-project", "codebase-analysis", "developer-tooling"]
        }
