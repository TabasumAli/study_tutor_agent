"""
Streamlit frontend for the Study Tutor Agent.
- Black background, white text, yellow buttons.
- Sidebar for settings & controls.
- User enters Groq API key on the frontend.
"""

import os
import uuid
import requests
import streamlit as st

# ------------------------------------------------------------------
# Config
# ------------------------------------------------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

st.set_page_config(
    page_title="Study Tutor Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------------------------------------------------
# Custom CSS: black bg, white text, yellow buttons
# ------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* App background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    /* Main text */
    h1, h2, h3, h4, h5, h6, p, label, span, div {
        color: #FFFFFF !important;
    }
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid #FFD400;
    }
    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }
    /* Buttons */
    .stButton > button,
    .stFormSubmitButton > button {
        background-color: #FFD400 !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        padding: 0.5rem 1rem !important;
    }
    .stButton > button:hover,
    .stFormSubmitButton > button:hover {
        background-color: #FFC400 !important;
        color: #000000 !important;
    }
    /* Inputs */
    .stTextInput input, .stTextArea textarea {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFD400 !important;
        border-radius: 8px !important;
    }
    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        background-color: #111111;
        border: 1px solid #262626;
        border-radius: 12px;
        padding: 0.75rem;
    }
    /* Chat input */
    div[data-testid="stChatInput"] textarea {
        background-color: #111111 !important;
        color: #FFFFFF !important;
        border: 1px solid #FFD400 !important;
    }
    /* Expander */
    details {
        background-color: #0d0d0d;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ------------------------------------------------------------------
# Session state
# ------------------------------------------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🎓 Study Tutor")
    st.markdown("Your AI-powered personal tutor.")

    st.markdown("### 🔑 Groq API Key")
    api_key = st.text_input(
        "Enter your Groq API key",
        type="password",
        placeholder="gsk_...",
        help="Get a free key at https://console.groq.com/keys",
    )

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    st.caption(f"Session ID: `{st.session_state.session_id[:8]}...`")

    if st.button("🧹 Clear Conversation", use_container_width=True):
        try:
            requests.post(
                f"{BACKEND_URL}/clear",
                json={"session_id": st.session_state.session_id},
                timeout=10,
            )
        except Exception:
            pass
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.success("Conversation cleared.")
        st.rerun()

    if st.button("🔄 New Session", use_container_width=True):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.markdown("### 💡 Try asking")
    st.markdown(
        "- Explain quantum entanglement\n"
        "- Quiz me on Python lists\n"
        "- 7-day plan to learn calculus\n"
        "- Flashcards for Spanish verbs\n"
        "- Summarize this: <paste text>"
    )

# ------------------------------------------------------------------
# Main area
# ------------------------------------------------------------------
st.title("🎓 Study Tutor Agent")
st.caption("Powered by CrewAI + Groq `openai/gpt-oss-120b` · Short-term memory enabled")

if not api_key:
    st.warning("⚠️ Please enter your **Groq API key** in the sidebar to start.")
    st.stop()

# Render chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask your tutor anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("_Thinking..._")
        try:
            resp = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "api_key": api_key,
                    "session_id": st.session_state.session_id,
                    "message": user_input,
                },
                timeout=180,
            )
            if resp.status_code == 200:
                reply = resp.json().get("reply", "")
            else:
                try:
                    detail = resp.json().get("detail", resp.text)
                except Exception:
                    detail = resp.text
                reply = f"❌ **Error {resp.status_code}**: {detail}"
        except requests.exceptions.Timeout:
            reply = "❌ **Timeout**: The tutor took too long to respond. Please try again."
        except Exception as e:
            reply = f"❌ **Connection error**: {e}"

        placeholder.markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})