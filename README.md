# RateMyGit

An AI-powered system that evaluates a public GitHub repository and provides a meaningful score, qualitative summary, and personalized improvement roadmap.
The goal is to help students (and developers) understand how their GitHub projects appear to recruiters, mentors, and potential collaborators based purely on repository quality and good development practices.

## Problem Statement

A GitHub repository is a developer’s most visible proof of work. Yet most students have no objective way to evaluate:

- Code quality
- Project structure
- Documentation completeness
- Testing practices
- Development consistency (commit history, branching, etc.)

RateMyGit acts as a repo mirror, reflecting real strengths and weaknesses through automated analysis and AI-generated feedback.

## Features

- Accepts a public GitHub repository URL
- Fetches metadata and structure via GitHub APIs
- Extracts key features:
  - File and folder organization
  - Commit activity and history
  - Presence and quality of documentation (README, docs folder, etc.)
  - Testing indicators (test folders, frameworks, CI configs)
- Heuristic scoring engine (0–100)
- AI-powered qualitative summary and personalized improvement roadmap
- Clean, structured output for easy understanding

## Output Example

- **Score**: 72/100
- **Level**: Intermediate
- **Summary**: Honest, concise evaluation of the repository's strengths and weaknesses
- **Roadmap**: Prioritized, actionable steps to improve the project and make it more appealing to recruiters

## Tech Stack

- **Backend**: Python + FastAPI
- **GitHub Integration**: PyGithub (GitHub REST API)
- **AI**: Groq + LLaMA 3
- **Data Validation**: Pydantic

## How to Run Locally

### Prerequisites

- Python 3.9+
- GitHub Personal Access Token (with `public_repo` scope)
- Groq API key

### Installation

```bash
git clone https://github.com/your-username/GITHUB-Rate.git
cd GITHUB-Rate
pip install -r requirements.txt
```
Create a .env file in the root directory
Start the Server using 
```bash
uvicorn app.main:app --reload
```

