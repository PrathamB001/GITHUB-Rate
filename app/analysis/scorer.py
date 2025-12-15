def score_repo(
    features: dict,
    code_quality: dict | None = None,
    structure: dict | None = None,
    proof_of_work: dict | None = None
):
    """
    Aggregates deterministic repo signals + optional LLM analyses
    into a final score, level, and breakdown.
    """

    breakdown = {}


    doc_score = 0
    if features.get("has_readme"):
        doc_score += 10
        readme_len = len(features.get("readme_text", ""))
        if readme_len > 1000:
            doc_score += 10
        elif readme_len > 300:
            doc_score += 5
    breakdown["Documentation"] = doc_score

    test_score = 0
    files_lower = features.get("files_lower", [])
    folders_lower = features.get("folders_lower", [])

    if any("test" in f for f in files_lower):
        test_score += 10
    if "tests" in folders_lower:
        test_score += 10

    breakdown["Testing"] = test_score


    breakdown["CI/CD"] = 15 if features.get("has_ci") else 0


    commits = features.get("commit_count", 0)
    if commits >= 50:
        breakdown["Commits"] = 20
    elif commits >= 20:
        breakdown["Commits"] = 15
    elif commits >= 8:
        breakdown["Commits"] = 10
    else:
        breakdown["Commits"] = 5


    struct_score = 5
    if features.get("file_count", 0) >= 20:
        struct_score += 5
    if features.get("folder_count", 0) >= 2:
        struct_score += 5

    breakdown["Structure (Deterministic)"] = struct_score


    pro_score = 0


    if features.get("license"):
        pro_score += 5

    if any(
        f in files_lower
        for f in ["requirements.txt", "pyproject.toml", "setup.py", "environment.yml"]
    ):
        pro_score += 5

    breakdown["Professional Signals"] = pro_score

    cq_bonus = 0
    if code_quality and isinstance(code_quality, dict):
        try:
            cq_score = int(code_quality.get("score", 0))
            cq_bonus = min(max(cq_score, 0), 10)
        except Exception:
            cq_bonus = 0

    breakdown["Code Quality (LLM)"] = cq_bonus


    struct_llm_bonus = 0
    if structure and isinstance(structure, dict):
        try:
            s_score = int(structure.get("structure_score", 0))
            struct_llm_bonus = min(max(s_score // 2, 0), 5)
        except Exception:
            struct_llm_bonus = 0

    breakdown["Structure (LLM)"] = struct_llm_bonus


    pow_bonus = 0
    if proof_of_work and isinstance(proof_of_work, dict):
        if proof_of_work.get("score") == "STRONG":
            signals = proof_of_work.get("signals", [])
            pow_bonus = min(len(signals) * 2, 5)

    breakdown["Proof of Work"] = pow_bonus


    score = sum(breakdown.values())
    score = min(score, 100)

    # Levels
    if score < 55:
        level = "Beginner"
    elif score < 80:
        level = "Intermediate"
    else:
        level = "Advanced"

    return score, level, breakdown
