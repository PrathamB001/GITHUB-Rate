def analyze_repo(repo_data: dict):
    files = repo_data.get("files", [])
    folders = repo_data.get("folders", [])

    features = {
        "file_count": len(files),
        "folder_count": len(folders),
        "has_readme": repo_data.get("has_readme", False),
        "has_tests": repo_data.get("has_tests", False),
        "has_ci": repo_data.get("has_ci", False),
        "commit_count": repo_data.get("commit_count", 0),
        "languages": list(repo_data.get("languages", {}).keys()),
    }

    return features
