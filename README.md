# 🎓 Study Tutor Agent

A single-agent AI tutor built with **CrewAI**, powered by **Groq's `openai/gpt-oss-120b`**, with a **Streamlit** frontend and a **FastAPI** backend. Includes **short-term memory** across turns and 5 custom study tools.

---

## ✨ Features

- 🧠 **Single CrewAI agent** with a Study Tutor persona
- ⚡ **Groq `openai/gpt-oss-120b`** for fast inference
- 🛠️ **5 custom tools**: Explain Concept, Generate Quiz, Create Study Plan, Summarize Text, Flashcard Maker
- 💾 **Short-term memory** (last 6 turns per session)
- 🎨 **Streamlit UI**: black background, white text, yellow buttons, sidebar
- 🔑 **User-provided Groq API key** (entered on the frontend, never stored server-side)
- ☁️ **Backend deployable on Render**, frontend on **Streamlit Cloud**

---

## 📁 Structure

```
study-tutor-agent/
├── backend/
│   ├── app.py            # FastAPI entry
│   ├── agent.py          # CrewAI agent
│   ├── tools.py          # Custom tools
│   ├── memory.py         # Short-term memory
│   └── requirements.txt
└── frontend/
    ├── streamlit_app.py  # Streamlit UI
    └── requirements.txt
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
export BACKEND_URL="http://localhost:8000"   # Windows: set BACKEND_URL=...
streamlit run streamlit_app.py
```

Open `http://localhost:8501`, paste your **Groq API key** in the sidebar, and start chatting.

---

## ☁️ Deployment

### Backend → Render

1. Push the repo to GitHub.
2. On [Render](https://render.com): **New → Web Service**.
3. Connect your repo.
4. Settings:
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or Starter for better performance)
5. No env vars required (API key comes from the frontend).
6. Deploy → copy your Render URL, e.g. `https://study-tutor-backend.onrender.com`.

### Frontend → Streamlit Cloud

1. On [share.streamlit.io](https://share.streamlit.io): **New app**.
2. Pick your repo, set **Main file path**: `frontend/streamlit_app.py`.
3. Under **Advanced settings → Secrets**, add:

   ```toml
   BACKEND_URL = "https://your-backend.onrender.com"
   ```

   Or, since we read `os.getenv("BACKEND_URL")`, also works if you add it as an env var in the Streamlit Cloud app settings.
4. Deploy.

---

## 🔑 Getting a Groq API Key

1. Go to https://console.groq.com/keys
2. Create a new key (starts with `gsk_...`).
3. Paste it into the Streamlit sidebar.

The key is sent only to your backend per-request and is never persisted.

---

## 🧪 Example Prompts

- "Explain recursion like I'm 12."
- "Quiz me on the French Revolution — 5 questions."
- "Give me a 10-day plan to learn React."
- "Make 8 flashcards for the periodic table trends."
- "Summarize: <paste your notes>"

---

## 📜 License

MIT