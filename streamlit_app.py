import streamlit as st

from app.github.fetcher import fetch_repo_data
from app.analysis.repo_analyzer import analyze_repo
from app.analysis.scorer import score_repo
from app.llm.summary import generate_summary

st.set_page_config(
    page_title="RMG",
    page_icon="🤩",
    layout="centered"
)

st.title("RateMyGit🤩")
st.write(
    "Analyze any public GitHub repository and get a score, summary, and improvement roadmap"
)

repo_url = st.text_input(
    "Enter GitHub Repository URL",
    placeholder="https://github.com/username/repository"
)

analyze_btn = st.button("Analyze Repository")

if analyze_btn:
    if not repo_url.strip():
        st.error("Please enter a valid GitHub repository URL")
    else:
        with st.spinner("Analyzing repository..."):
            try:
                repo_data = fetch_repo_data(repo_url)
                features = analyze_repo(repo_data)
                score, level = score_repo(features)
                summary, roadmap = generate_summary(score, level, features)

                st.success("Analysis Complete")

                st.metric("Score", f"{score} / 100")
                st.write(f"**Level:** {level}")

                st.subheader("Summary")
                st.write(summary)

                st.subheader("Personalized Roadmap")
                for step in roadmap:
                    st.write(f"- {step}")

            except Exception as e:
                st.error(f"Failed to analyze repository: {e}")
