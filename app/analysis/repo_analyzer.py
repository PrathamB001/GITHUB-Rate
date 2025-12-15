def analyze_repo(repo_data: dict):
    files = repo_data.get("files", []) or []
    folders = repo_data.get("folders", []) or []

    files_lower = [f.lower() for f in files]
    folders_lower = [f.lower() for f in folders]

    return {
        "file_count": len(files),
        "folder_count": len(folders),
        "has_readme": repo_data.get("has_readme", False),
        "has_tests": any("test" in f for f in files_lower),
        "has_ci": repo_data.get("has_ci", False),
        "commit_count": repo_data.get("commit_count", 0),
        "languages": list(repo_data.get("languages", {}).keys()),
        "readme_text": repo_data.get("readme_text", ""),
        "files_lower": files_lower,
        "folders_lower": folders_lower,
    }
