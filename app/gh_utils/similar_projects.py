import os
import requests
from typing import List, Dict

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


STOPWORDS = {
    "system", "model", "application", "tool", "framework",
    "library", "project", "repo", "code"
}


def fetch_similar_projects(
    keywords: List[str],
    primary_language: str,
    exclude_repo: str,
    limit: int = 5
) -> List[Dict]:
    """
    Fetch similar repositories using GitHub-search-optimized keywords.
    """

    if not keywords or not primary_language:
        return []

    clean_keywords = [
        k for k in keywords
        if k.lower() not in STOPWORDS and len(k) > 3
    ]

    if not clean_keywords:
        return []

    keyword_query = " OR ".join(f'"{k}"' for k in clean_keywords[:4])
    query = f"({keyword_query}) language:{primary_language} stars:>10 fork:false archived:false"

    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit + 3
    }
    print("DEBUG QUERY:", query)

    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    if response.status_code != 200:
        return []

    results = []
    for repo in response.json().get("items", []):
        full_name = repo["full_name"]

        if full_name.lower() == exclude_repo.lower():
            continue

        results.append({
            "name": full_name,
            "url": repo["html_url"],
            "html_url": repo["html_url"],  # UI safety
            "stars": repo["stargazers_count"],
            "description": repo["description"] or "No description provided."
        })

        if len(results) >= limit:
            break

    return results
