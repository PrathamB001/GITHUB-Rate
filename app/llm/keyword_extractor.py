import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_keywords_from_repo(description: str, readme_text: str) -> dict:
    """
    LLM-driven intent extraction for GitHub search.
    Output is STRICT JSON used directly for GitHub API querying.
    """

    prompt = f"""
You are an expert GitHub project analyst.

Your task is to extract SEARCH-OPTIMIZED intent from a repository
so that similar, high-quality repositories can be found via GitHub Search.

This is NOT a summarization task.
This is NOT about tools or frameworks.
This is about identifying the REAL PROBLEM DOMAIN and CORE FUNCTION.

Repository Description:
{description or "No description"}

README excerpt:
{readme_text[:3500]}

Return ONLY valid JSON in EXACTLY this format:

{{
  "summary": "<one clear sentence describing what this project does>",
  "problem_domain": ["domain-1", "domain-2"],
  "core_function": ["function-1", "function-2"],
  "search_phrases": ["phrase-1", "phrase-2", "phrase-3"]
}}

Rules:
- problem_domain MUST be real-world areas (finance, security, healthcare, vision, nlp, geospatial, robotics, forecasting, etc.)
- core_function MUST be actions (prediction, detection, estimation, tracking, analysis, classification, monitoring)
- search_phrases MUST combine domain + function (e.g. "fraud-detection", "time-series-forecasting")
- search_phrases MUST be suitable for GitHub repository search
- Use lowercase only
- Use hyphens instead of spaces
- Be specific and concrete, not abstract
- NEVER include tooling or implementation words:
  ml, ai, model, app, tool, api, python, streamlit, flask, django, react, framework, sdk, library
- If the domain or function is not explicitly stated, INFER it from context
- Do NOT return generic placeholders
- Do NOT return empty fields
- Output ONLY valid JSON, nothing else
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=220
        )

        raw = response.choices[0].message.content.strip()
        data = json.loads(raw)

        # ---- HARD VALIDATION & CLEANING ----
        summary = data.get("summary", "").strip()
        problem_domain = data.get("problem_domain", [])
        core_function = data.get("core_function", [])
        search_phrases = data.get("search_phrases", [])

        if not summary or not problem_domain or not core_function or not search_phrases:
            raise ValueError("Incomplete LLM output")

        def clean(arr, min_len):
            return [
                x.lower().strip().replace(" ", "-")
                for x in arr
                if isinstance(x, str) and len(x.strip()) >= min_len
            ]

        problem_domain = clean(problem_domain, 3)
        core_function = clean(core_function, 4)
        search_phrases = clean(search_phrases, 6)

        if not problem_domain or not search_phrases:
            raise ValueError("Invalid cleaned output")

        return {
            "summary": summary,
            "problem_domain": problem_domain[:3],
            "core_function": core_function[:3],
            "search_phrases": search_phrases[:5]
        }

    except Exception:
        # Schema-safe fallback (still search-usable, no tool leakage)
        return {
            "summary": description[:120] or "Software project with inferred purpose",
            "problem_domain": ["software"],
            "core_function": ["analysis"],
            "search_phrases": ["software-analysis"]
        }
