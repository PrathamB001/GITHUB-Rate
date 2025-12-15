# RateMyGit

An AI-powered system that evaluates a public GitHub repository and provides a meaningful score, qualitative summary, and personalized improvement roadmap.
The goal is to help students (and developers) understand how their GitHub projects appear to recruiters, mentors, and potential collaborators based purely on repository quality and good development practices.

Video Demonstration : https://tinyurl.com/34tj3bfh

## Problem Statement

A GitHub repository is a developer’s most visible proof of work. Yet most students have no objective way to evaluate:

- Code quality
- Project structure
- Documentation completeness
- Testing practices
- Development consistency (commit history, branching, etc.)

RateMyGit acts as a repo mirror, reflecting real strengths and weaknesses through automated analysis and AI-generated feedback.

### Core Analysis
- Accepts a public GitHub repository URL
- Fetches metadata and structure via GitHub APIs
- Extracts key deterministic signals:
  - File and folder organization
  - Commit activity
  - Presence of documentation (README, config files)
  - Testing indicators
  - CI/CD configuration

### Scoring & Feedback
- Heuristic scoring engine (0–100)
- Repository maturity classification:
  - **Beginner** / **Intermediate** / **Advanced**
- AI-powered qualitative summary
- Personalized, actionable improvement roadmap

### Repository Stats & Deep Review
- **Score Breakdown** (transparent category-wise scoring):
  - Documentation
  - Testing
  - CI/CD
  - Commits
  - Project structure
  - Professional signals
- **Code Quality Review** (LLM-assisted):
  - Readability
  - Function size
  - Error handling
  - Separation of concerns
- **Project Structure Analysis**:
  - Folder organization
  - Entry-point clarity
  - Scalability of layout
- **Proof-of-Work Detection**:
  - Screenshots
  - Video demos
  - Live deployment links  
  - Confidence grading (**STRONG** / **MEDIUM** / **WEAK**)
## Output Example

**Score:** 72 / 100  
**Level:** Intermediate  

**Summary:**  
Clear explanation of strengths and weaknesses.

**Roadmap:**
- Add unit tests for core modules
- Introduce CI for automated checks
- Improve commit hygiene

**Repository Stats:**
- Code Quality: 6/10
- Structure: 7/10
- Proof of Work: MEDIUM

---

## Tech Stack

- **Backend:** Python
- **GitHub Integration:** PyGithub (GitHub REST API)
- **LLMs:** Qwen 2.5 (via Hugging Face Inference)
- **UI:** Streamlit
- **Configuration:** dotenv
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





