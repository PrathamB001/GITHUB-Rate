import os
import requests
from typing import Dict, List, Optional

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Accept": "application/vnd.github.mercy-preview+json"
}

if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# Generic infra / tooling indicators (NOT domains)
FRAMEWORK_TERMS = {
    "framework", "toolkit", "library", "boilerplate",
    "starter", "sdk", "template", "faster way to build"
}


def fetch_similar_projects(
    intent: Optional[Dict] = None,
    *,
    keywords: Optional[List[str]] = None,   # backward compatibility
    primary_language: str,
    exclude_repo: str,
    limit: int = 5
) -> List[Dict]:
    """
    Fetch similar repositories using LLM-inferred intent.
    No hardcoded domains. No project bias.
    """

    # ---- BACKWARD COMPATIBILITY ----
    if intent is None:
        if not keywords:
            return []
        intent = {
            "problem_domain": [],
            "core_function": [],
            "search_phrases": keywords[:5]
        }

    problem_domain = intent.get("problem_domain", [])
    core_function = intent.get("core_function", [])
    search_phrases = intent.get("search_phrases", [])

    if not search_phrases or not primary_language:
        return []

    # ---- BUILD SEARCH QUERY ----
    query_terms = [f'"{p}"' for p in search_phrases[:3]]

    query = " ".join([
        f"({' OR '.join(query_terms)})",
        f"language:{primary_language}",
        "stars:>20",
        "fork:false",
        "archived:false"
    ])

    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit + 12
    }

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if response.status_code != 200:
            return []

        items = response.json().get("items", [])
        results = []

        for item in items:
            full_name = item.get("full_name", "")
            if not full_name or full_name.lower() == exclude_repo.lower():
                continue

            desc = (item.get("description") or "").lower()
            topics = " ".join(item.get("topics", [])).lower()
            name = full_name.lower()

            # Reject infra / framework repos
            if any(term in desc for term in FRAMEWORK_TERMS):
                continue

            score = 0

            for d in problem_domain:
                if d in name:
                    score += 4
                if d in desc:
                    score += 3
                if d in topics:
                    score += 3

            for f in core_function:
                if f in desc or f in topics:
                    score += 2

            if score <= 0:
                continue

            repo_url = item.get("html_url")

            results.append({
                "score": score,
                "name": full_name,
                "url": repo_url,        # new
                "html_url": repo_url,   # REQUIRED for UI
                "stars": item.get("stargazers_count", 0),
                "description": item.get("description") or "No description provided."
            })

        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    except Exception:
        return []
