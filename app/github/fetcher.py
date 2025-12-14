import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_repo_data(repo_url: str):
    repo_name = repo_url.replace("https://github.com/", "").strip("/")
    gh = Github(GITHUB_TOKEN) if GITHUB_TOKEN else Github()
    repo = gh.get_repo(repo_name)

    contents = repo.get_contents("")
    files = []
    folders = []

    while contents:
        item = contents.pop(0)
        if item.type == "dir":
            folders.append(item.path)
            contents.extend(repo.get_contents(item.path))
        else:
            files.append(item.path)

    commits = list(repo.get_commits()[:100])
    languages = repo.get_languages()

    return {
        "files": files,
        "folders": folders,
        "commit_count": len(commits),
        "languages": languages,
        "has_readme": any("README" in f.upper() for f in files),
        "has_tests": any("test" in f.lower() for f in files),
        "has_ci": any(".github/workflows" in f for f in files),
    }
