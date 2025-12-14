import streamlit as st
import base64

from app.github.fetcher import fetch_repo_data
from app.analysis.repo_analyzer import analyze_repo
from app.analysis.scorer import score_repo
from app.llm.summary import generate_summary
from app.github.similar_projects import fetch_similar_projects
from app.llm.keyword_extractor import extract_keywords_from_repo


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="RateMyGit",
    page_icon="🤩",
    layout="centered"
)


# ---------- BACKGROUND ----------
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


# ---------- STYLES ----------
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

    div.stButton > button:hover {
        background-color: #6D28D9;
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

    .summary, .roadmap-item {
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


# ---------- HEADER ----------
st.markdown("<h1>RateMyGit 🤩</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='description'>Analyze any public GitHub repository and get a detailed score, qualitative summary, and personalized improvement roadmap.</p>",
    unsafe_allow_html=True
)


# ---------- INPUT ----------
repo_url = st.text_input(
    "GitHub Repository URL",
    placeholder="https://github.com/username/repository",
    label_visibility="collapsed"
)

analyze_btn = st.button("Analyze Repository")


# ---------- ANALYSIS ----------
if analyze_btn:
    if not repo_url.strip() or not repo_url.startswith("https://github.com/"):
        st.error("⚠️ Please enter a valid public GitHub repository URL.")
    else:
        with st.spinner("Analyzing your repository..."):
            try:
                # Core analysis
                repo_data = fetch_repo_data(repo_url)
                features = analyze_repo(repo_data)
                score, level, breakdown = score_repo(features)
                summary, roadmap = generate_summary(score, level, features)
                primary_language = max(
                    repo_data.get("languages", {}),
                    key=repo_data.get("languages", {}).get,
                    default=None
                ) if repo_data.get("languages") else None
                # Initialize keywords safely
                keywords = []



                # Keyword extraction
                llm_info = extract_keywords_from_repo(
                    description=repo_data.get("description", ""),
                    readme_text=repo_data.get("readme_text", "")
                )
                keywords = llm_info.get("keywords", [])
                # Fallback: if no keywords from LLM, use primary language
                if not keywords and primary_language:
                    keywords = [primary_language.lower()]
                EXPANSION_MAP = {
                    "ml": ["machine learning", "deep learning", "model"],
                    "api": ["backend", "rest", "service", "fastapi"]
                }


                expanded = []
                for kw in keywords:
                    expanded.append(kw)
                    expanded.extend(EXPANSION_MAP.get(kw.lower(), []))

                # Deduplicate + cap
                keywords = list(dict.fromkeys(expanded))[:6]

                if not keywords:
                    keywords = [primary_language.lower()]






                similar_projects = fetch_similar_projects(
                    keywords=keywords,
                    primary_language=primary_language,
                    exclude_repo=repo_url.replace("https://github.com/", "")
                )


                # ---------- RESULTS ----------
                st.markdown(f'<div class="big-score">{score}/100</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="level">Level: <strong>{level}</strong></div>', unsafe_allow_html=True)

                st.markdown('<h2 class="section-title">Summary</h2>', unsafe_allow_html=True)
                st.markdown(f'<p class="summary">{summary}</p>', unsafe_allow_html=True)

                # ---------- ROADMAP (FIXED) ----------
                st.markdown(
                    '<h2 class="section-title">Personalized Improvement Roadmap</h2>',
                    unsafe_allow_html=True
                )

                # DEBUG — remove later
                st.write(f"Roadmap items generated: {len(roadmap)}")

                if roadmap and len(roadmap) > 0:
                    for step in roadmap:
                        st.markdown(f"- {step}")
                else:
                    st.warning(
                        "No specific roadmap items were generated for this repository. "
                        "This usually happens when the repository structure is very minimal."
                    )

                # ---------- SIMILAR PROJECTS ----------
                if similar_projects:
                    st.markdown(
                        '<h2 class="section-title">Similar High-Quality Open Source Projects</h2>',
                        unsafe_allow_html=True
                    )

                    st.write(
                        "These repositories are semantically similar based on project intent, domain, and tech stack:"
                    )

                    for proj in similar_projects:
                        st.markdown(
                            f"• **[{proj['name']}]({proj['url']})** ⭐ {proj['stars']}  \n"
                            f"{proj['description']}"
                        )

                # Success at the END
                st.success("Analysis Complete! ✅")

            except Exception as e:
                st.error(f"Failed to analyze repository: {str(e)}")
                st.info("Make sure the URL is correct and the repo is public.")