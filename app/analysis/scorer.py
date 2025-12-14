def score_repo(features: dict):
    score = 0


    if features.get("has_readme"):
        score += 15
    else:
        score += 5


    if features.get("has_tests"):
        score += 15
    else:
        score += 5


    if features.get("has_ci"):
        score += 10


    commits = features.get("commit_count", 0)
    if commits >= 25:
        score += 20
    elif commits >= 10:
        score += 15
    elif commits >= 5:
        score += 10
    else:
        score += 5


    files = features.get("file_count", 0)
    if files >= 30:
        score += 20
    elif files >= 15:
        score += 15
    else:
        score += 10

    score = min(score, 100)

    if score < 50:
        level = "Beginner"
    elif score < 80:
        level = "Intermediate"
    else:
        level = "Advanced"

    return score, level
