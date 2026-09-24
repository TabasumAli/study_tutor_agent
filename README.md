# 🎓 Study Tutor Agent

A single-agent AI tutor built with **CrewAI**, powered by **Groq's `openai/gpt-oss-120b`**, with a **Streamlit** frontend and a **FastAPI** backend. Includes **short-term memory** across turns and 5 custom study tools.

---

## ✨ Features

- 🧠 **Single CrewAI agent** with a Study Tutor persona
- ⚡ **Groq `openai/gpt-oss-120b`** via Groq's OpenAI-compatible endpoint (no LiteLLM needed)
- 🛠️ **5 custom tools**: Explain Concept, Generate Quiz, Create Study Plan, Summarize Text, Flashcard Maker
- 💾 **Short-term memory** (last 6 turns per session)
- 🎨 **Streamlit UI**: black background, white text, yellow buttons, sidebar
- 🔑 **User-provided Groq API key** (entered on the frontend, never stored server-side)
- ☁️ **Backend deployable on Render**, frontend on **Streamlit Cloud**

---

## 📁 Structure

```text
study-tutor-agent/
├── .python-version       # Pins Python 3.13.4 for Render (CrewAI requires <3.14)
├── .gitignore
├── README.md
├── backend/
│   ├── app.py            # FastAPI entry point
│   ├── agent.py          # CrewAI agent + Groq LLM setup
│   ├── tools.py          # Custom tools
│   ├── memory.py         # Short-term memory
│   ├── requirements.txt
│   └── .gitignore
└── frontend/
    ├── streamlit_app.py  # Streamlit UI
    ├── requirements.txt
    └── .gitignore
```

---

## 🚀 Local Setup

### 1. Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```

Backend runs at `http://localhost:8000`.

### 2. Frontend

```bash
cd frontend
pip install -r requirements.txt
export BACKEND_URL="http://localhost:8000"   # Windows: set BACKEND_URL=http://localhost:8000
streamlit run streamlit_app.py
```

Open `http://localhost:8501`, paste your Groq API key in the sidebar, and start chatting.

---

## ☁️ Deployment

### Backend → Render

1. Push the repo to GitHub.
2. On Render: **New** → **Web Service**.
3. Connect your repo.
4. Settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or Starter for better performance)
5. No environment variables required (API key comes from the frontend per request).
6. Deploy → copy your Render URL, e.g. `https://study-tutor-backend.onrender.com`.

> **Important:** A `.python-version` file at the repo root pins Python to `3.13.4`. CrewAI does not support Python 3.14 yet, and Render defaults to 3.14 for new services. Without this file, the build will fail with `No matching distribution found for crewai`.

### Frontend → Streamlit Cloud

1. On [share.streamlit.io](https://share.streamlit.io): **New app**.
2. Pick your repo, set **Main file path**: `frontend/streamlit_app.py`.
3. Under **Advanced settings** → **Secrets**, add:

```toml
BACKEND_URL = "https://your-backend.onrender.com"
```

The app reads this via `os.getenv("BACKEND_URL")`, so it also works if you add it as an environment variable in Streamlit Cloud settings.
4. Deploy.

---

## 🔑 Getting a Groq API Key

1. Go to [console.groq.com/keys](https://console.groq.com/keys).
2. Create a new key (starts with `gsk_...`).
3. Paste it into the Streamlit sidebar.

The key is sent only to your backend per-request and is never persisted.

---

## 🧪 Example Prompts

- *"Explain recursion like I'm 12."*
- *"Quiz me on the French Revolution — 5 questions."*
- *"Give me a 10-day plan to learn React."*
- *"Make 8 flashcards for the periodic table trends."*
- *"Summarize: `<paste your notes>`"*

---

## 🛠️ Troubleshooting

These are real issues encountered during deployment — documenting them here so they're easy to fix if they resurface.

- **Build fails on `crewai` version:** Ensure `.python-version` at the repo root contains `3.13.4`. CrewAI's requirement is `>=3.10,<3.14`, and Render's default of Python 3.14 will cause `No matching distribution found for crewai`.
- **Dependency conflicts (`pydantic` / `uvicorn` / `python-dotenv`):** CrewAI's dependency tree moves fast. Use loose pins in `backend/requirements.txt` (e.g., `uvicorn[standard]>=0.31.1,<0.32.0`) rather than exact versions, so `pip` can resolve a working set.
- **`Fallback to LiteLLM is not available` error at runtime:** This means the model string routes through LiteLLM. The backend avoids this by using Groq's OpenAI-compatible endpoint (`https://api.groq.com/openai/v1`) with the `openai/gpt-oss-120b` model name and CrewAI's native OpenAI SDK integration.
- **Render free-tier cold start:** First request after 15 minutes of inactivity takes 30–60 seconds. Streamlit's request timeout is 180s, so it will wait rather than fail.
- **Root Directory errors on Render:** Set Root Directory to exactly `backend` (no slashes, no quotes). This makes Render `cd` into the backend folder before running build and start commands.

---

## 📜 License

[MIT](LICENSE)
