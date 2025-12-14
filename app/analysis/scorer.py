def score_repo(features: dict):
    breakdown = {}

    # 1. Documentation (20 points max)
    doc_score = 0
    if features.get("has_readme"):
        doc_score += 10
        readme_len = len(features.get("readme_text", ""))
        if readme_len > 1000:
            doc_score += 10
        elif readme_len > 300:
            doc_score += 5
    breakdown["Documentation"] = doc_score

    # 2. Testing (20 points max)
    test_score = 0
    files_lower = features.get("files_lower", [])
    folders_lower = features.get("folders_lower", [])
    if any("test" in f for f in files_lower):
        test_score += 10
    if "tests" in folders_lower:
        test_score += 10
    breakdown["Testing"] = test_score

    # 3. CI/CD (15 points)
    breakdown["CI/CD"] = 15 if features.get("has_ci") else 0

    # 4. Commit Activity (20 points)
    commits = features.get("commit_count", 0)
    if commits >= 50:
        breakdown["Commits"] = 20
    elif commits >= 20:
        breakdown["Commits"] = 15
    elif commits >= 8:
        breakdown["Commits"] = 10
    else:
        breakdown["Commits"] = 5

    # 5. Project Structure (15 points)
    struct_score = 5
    if features.get("file_count", 0) >= 20:
        struct_score += 5
    if features.get("folder_count", 0) >= 2:
        struct_score += 5
    breakdown["Structure"] = struct_score

    # 6. Professional Signals (10 points bonus)
    pro_score = 0
    if any("license" in f for f in files_lower):
        pro_score += 5
    if any(f in files_lower for f in ["requirements.txt", "pyproject.toml", "setup.py", "environment.yml"]):
        pro_score += 5
    breakdown["Professional Signals"] = pro_score

    #SCORE
    score = sum(breakdown.values())
    score = min(score, 100)  # No artificial floor — low-effort repos stay low

    # Levels
    if score < 55:
        level = "Beginner"
    elif score < 80:
        level = "Intermediate"
    else:
        level = "Advanced"

    return score, level, breakdown