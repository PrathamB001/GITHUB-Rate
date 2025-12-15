import streamlit as st
import base64

from app.gh_utils.fetcher import fetch_repo_data, fetch_file_content
from app.analysis.repo_analyzer import analyze_repo
from app.analysis.scorer import score_repo
from app.llm.summary import generate_summary

# NEW analysis imports
from app.analysis.code_quality import analyze_code_quality
from app.analysis.structure_analysis import analyze_structure
from app.analysis.proof_of_work import analyze_proof_of_work


# PAGE CONFIG
st.set_page_config(
    page_title="RateMyGit",
    page_icon="🤩",
    layout="centered"
)


#  BACKGROUND
def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


set_bg("assets/img2.png")


#  STYLES
st.markdown(
    """
    <style>
    h1 {
        text-align: center;
        color: #FFFFFF;
        font-size: 3.5rem;
        margin-bottom: 0.5rem;
    }
    .description {
        text-align: center;
        color: #EDE9FE;
        font-size: 1.3rem;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: rgba(76, 29, 149, 0.7) !important;
        color: #FFFFFF !important;
        border-radius: 12px !important;
        border: 2px solid #FFFFFF !important;
        padding: 1rem;
        font-size: 1.1rem;
        text-align: center;
    }
    div.stButton > button {
        background-color: #7C3AED;
        color: #FFFFFF;
        border-radius: 12px;
        padding: 0.9rem 2rem;
        font-weight: 700;
        border: none;
        font-size: 1.2rem;
        display: block;
        margin: 2rem auto;
    }
    .big-score {
        font-size: 6rem;
        color: #FDE68A;
        text-align: center;
        font-weight: 900;
        margin: 2rem 0;
    }
    .level {
        text-align: center;
        font-size: 2.2rem;
        color: #FFFFFF;
        margin-bottom: 3rem;
    }
    .section-title {
        color: #FFFFFF;
        font-size: 2rem;
        margin-top: 3rem;
    }
    .summary {
        color: #EDE9FE;
        font-size: 1.3rem;
        line-height: 1.8;
        max-width: 900px;
        margin: 1rem auto;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)


#  HEADER
st.markdown("<h1>RateMyGit 🤩</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='description'>Analyze any public GitHub repository and get a detailed score, qualitative summary, and personalized improvement roadmap.</p>",
    unsafe_allow_html=True
)


# INPUT
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
    label_visibility="collapsed"
)

analyze_btn = st.button("Analyze Repository")


#  ANALYSIS
if analyze_btn:
    if not repo_url.strip() or not repo_url.startswith("https://github.com/"):
        st.error("⚠️ Please enter a valid public GitHub repository URL.")
    else:
        with st.spinner("Analyzing your repository..."):
            try:
                #  FETCH
                repo_data = fetch_repo_data(repo_url)
                features = analyze_repo(repo_data)

                #  BUILD LLM INPUTS
                sample_code = ""
                for f in repo_data.get("files", []):
                    if f.endswith(".py"):
                        try:
                            sample_code = fetch_file_content(repo_url, f)[:3500]
                            break
                        except Exception:
                            pass

                tree_summary = ""
                for folder in repo_data.get("folders", []):
                    tree_summary += f"{folder}/\n"
                for f in repo_data.get("files", [])[:15]:
                    tree_summary += f"  {f}\n"

                #  ANALYSIS
                code_quality = analyze_code_quality(sample_code)
                structure = analyze_structure(tree_summary)
                proof_of_work = analyze_proof_of_work(repo_data.get("readme_text", ""))

                score, level, breakdown = score_repo(
                    features,
                    code_quality=code_quality,
                    structure=structure,
                    proof_of_work=proof_of_work
                )

                summary, roadmap = generate_summary(score, level, features)

                #  RESULTS
                st.markdown(f'<div class="big-score">{score}/100</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="level">Level: <strong>{level}</strong></div>', unsafe_allow_html=True)

                st.markdown('<h2 class="section-title">Summary</h2>', unsafe_allow_html=True)
                st.markdown(f'<p class="summary">{summary}</p>', unsafe_allow_html=True)

                st.markdown('<h2 class="section-title">Personalized Improvement Roadmap</h2>', unsafe_allow_html=True)
                for step in roadmap:
                    st.markdown(f"- {step}")


                st.markdown('<h2 class="section-title">Repository Stats</h2>', unsafe_allow_html=True)

                # Score Breakdown
                st.subheader("Score Breakdown")
                for k, v in breakdown.items():
                    st.write(f"- **{k}**: {v}")

                #  Code Quality
                st.subheader("Code Quality Review")
                cq_score = code_quality.get("score", "N/A")
                st.write(f"Overall code quality score: **{cq_score}/10**")

                if code_quality.get("issues"):
                    st.write("Main issues found:")
                    for issue in code_quality["issues"]:
                        st.write(f"- {issue}")

                if code_quality.get("actionable_fixes"):
                    st.write("Recommended improvements:")
                    for fix in code_quality["actionable_fixes"]:
                        st.write(f"- {fix}")

                #  Structure
                st.subheader("Project Structure Review")
                struct_score = structure.get("structure_score", "N/A")
                st.write(f"Structure score: **{struct_score}/10**")

                if structure.get("issues"):
                    st.write("Structural issues:")
                    for issue in structure["issues"]:
                        st.write(f"- {issue}")

                if structure.get("suggestions"):
                    st.write("How to improve the structure:")
                    for suggestion in structure["suggestions"]:
                        st.write(f"- {suggestion}")

                #Proof of Work
                st.subheader("Proof of Work")

                if proof_of_work.get("score") == "STRONG":
                    st.success("This repository shows strong proof of work.")
                    if proof_of_work.get("signals"):
                        st.write("Evidence found:")
                        for signal in proof_of_work["signals"]:
                            st.write(f"- {signal}")
                else:
                    st.warning(
                        "No strong proof of work detected. "
                        "Consider adding screenshots, demo videos, or a live deployment link."
                    )

                st.success("Analysis Complete! ✅")

            except Exception as e:
                st.error(f"Failed to analyze repository: {str(e)}")
                st.info("Make sure the URL is correct and the repo is public.")
