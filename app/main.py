from fastapi import FastAPI, HTTPException
from app.models.schemas import RepoRequest, RepoResponse
from app.gh_utils.fetcher import fetch_repo_data
from app.analysis.repo_analyzer import analyze_repo
from app.analysis.scorer import score_repo
from app.llm.summary import generate_summary

app = FastAPI(title="GITHUB-Rate")

@app.post("/analyze", response_model=RepoResponse)
def analyze_repository(request: RepoRequest):
    try:
        repo_data = fetch_repo_data(request.repo_url)
        features = analyze_repo(repo_data)
        score, level = score_repo(features)
        summary, roadmap = generate_summary(score, level, features)

        return {
            "score": score,
            "level": level,
            "summary": summary,
            "roadmap": roadmap
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
