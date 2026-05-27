import sys
import asyncio
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).parent
sys.path.append(str(APP_DIR))

import ingest
import search_agent
import logs


REPO_OWNER = "evidentlyai"
REPO_NAME = "docs"
MODEL_NAME = "mistral:latest"


@st.cache_resource
def init_app():
    index = ingest.index_data(
        repo_owner=REPO_OWNER,
        repo_name=REPO_NAME,
        chunk=True
    )

    agent = search_agent.init_agent(
        index=index,
        model_name=MODEL_NAME
    )

    return agent


st.set_page_config(
    page_title="RepoGuide AI",
    page_icon="📘",
    layout="wide"
)

st.markdown(
    """
    <style>
    .main {
        background-color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1050px;
    }

    .hero-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 60%, #334155 100%);
        padding: 34px;
        border-radius: 22px;
        color: white;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.18);
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 8px;
        letter-spacing: -0.5px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #cbd5e1;
        margin-bottom: 18px;
        line-height: 1.5;
    }

    .badge {
        display: inline-block;
        background-color: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #e2e8f0;
        padding: 8px 13px;
        border-radius: 999px;
        font-size: 13px;
        margin-right: 8px;
        margin-top: 8px;
    }

    .feature-card {
        background-color: white;
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
        min-height: 120px;
        margin-bottom: 18px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }

    .feature-text {
        font-size: 14px;
        color: #475569;
        line-height: 1.6;
    }

    .sidebar-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 14px;
        border-radius: 14px;
        margin-bottom: 12px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        margin-top: 18px;
        margin-bottom: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


with st.sidebar:
    st.markdown("## 📘 RepoGuide AI")
    st.caption("GitHub documentation assistant")

    st.markdown(
        f"""
        <div class="sidebar-card">
            <b>Knowledge Base</b><br>
            {REPO_OWNER}/{REPO_NAME}
        </div>
        <div class="sidebar-card">
            <b>Model</b><br>
            {MODEL_NAME}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info("Ask questions from indexed GitHub documentation. The assistant searches relevant docs before answering.")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-title">RepoGuide AI</div>
        <div class="hero-subtitle">
            A smart assistant that helps users understand GitHub documentation through natural-language questions.
        </div>
        <span class="badge">RAG-powered</span>
        <span class="badge">GitHub Docs</span>
        <span class="badge">Documentation Assistant</span>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="feature-card">
        <div class="feature-title">📚 Documentation Q&A</div>
        <div class="feature-text">
            Ask technical questions and get answers grounded in indexed documentation from the selected GitHub repository.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="section-title">Ask RepoGuide AI</div>', unsafe_allow_html=True)

agent = init_app()

if "messages" not in st.session_state:
    st.session_state.messages = []

example_questions = [
    "What is Evidently AI used for?",
    "How can I evaluate model performance?",
    "What are reports in Evidently?",
    "How can I monitor data drift?"
]

with st.expander("Try example questions"):
    for q in example_questions:
        st.markdown(f"- {q}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


prompt = st.chat_input("Ask a question from the documentation...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching documentation and generating answer..."):
            result = asyncio.run(agent.run(user_prompt=prompt))
            answer = result.output
            st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    logs.log_interaction(
        question=prompt,
        answer=answer,
        model_name=MODEL_NAME,
        source="streamlit"
    )
