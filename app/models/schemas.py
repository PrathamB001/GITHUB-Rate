from pydantic import BaseModel
from typing import List

class RepoRequest(BaseModel):
    repo_url: str

class RepoResponse(BaseModel):
    score: int
    level: str
    summary: str
    roadmap: List[str]
