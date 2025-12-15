import requests
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


def get_repo_overview(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}"
    r = requests.get(url, headers=HEADERS, timeout=15)
    if r.status_code != 200:
        return {}

    data = r.json()

    return {
        "stars": data["stargazers_count"],
        "forks": data["forks_count"],
        "watchers": data["watchers_count"],
        "open_issues": data["open_issues_count"],
        "last_updated": data["pushed_at"],
        "license": bool(data.get("license")),
        "language": data.get("language"),
        "archived": data.get("archived", False),
        "size_kb": data.get("size", 0)
    }
