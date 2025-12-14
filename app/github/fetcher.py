import os
from urllib.parse import urlparse
from github import Github
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def extract_repo_full_name(repo_url: str) -> str:
    parsed = urlparse(repo_url.strip())

    if "github.com" not in parsed.netloc:
        raise ValueError("Not a GitHub URL")

    path = parsed.path.strip("/")

    if path.endswith(".git"):
        path = path[:-4]

    parts = path.split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub repository URL")

    return f"{parts[0]}/{parts[1]}"


def fetch_repo_data(repo_url: str):
    readme_text = ""

    try:
        readme = repo.get_readme()
        readme_text = readme.decoded_content.decode("utf-8")[:4000]
    except Exception:
        pass

    repo_name = extract_repo_full_name(repo_url)

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
        "file_count": len(files),
        "commit_count": len(commits),
        "languages": languages,
        "has_readme": any("README" in f.upper() for f in files),
        "has_tests": any("test" in f.lower() for f in files),
        "has_ci": any(".github/workflows" in f for f in files),
        "readme_text": readme_text,
        "description": repo.description or "",

    }
