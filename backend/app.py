"""
FastAPI backend for the Study Tutor Agent.
Deployed on Render. Accepts Groq API key from the frontend per request.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional

from agent import run_tutor
from memory import add_turn, get_history, clear_session

app = FastAPI(title="Study Tutor Agent API", version="1.0.0")

# Allow Streamlit Cloud (and localhost) to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    api_key: str = Field(..., description="User's Groq API key")
    session_id: str = Field(..., description="Client session identifier")
    message: str = Field(..., description="User's message")


class ChatResponse(BaseModel):
    reply: str
    session_id: str


class ClearRequest(BaseModel):
    session_id: str


@app.get("/")
def root():
    return {"status": "ok", "service": "Study Tutor Agent"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    if not req.api_key or not req.api_key.strip():
        raise HTTPException(status_code=400, detail="Missing Groq API key.")
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Empty message.")

    try:
        # store user turn in short-term memory
        add_turn(req.session_id, "user", req.message)

        reply = run_tutor(req.api_key, req.session_id, req.message)

        # store assistant turn
        add_turn(req.session_id, "assistant", reply)

        return ChatResponse(reply=reply, session_id=req.session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")


@app.post("/clear")
def clear(req: ClearRequest):
    clear_session(req.session_id)
    return {"status": "cleared", "session_id": req.session_id}


@app.get("/history/{session_id}")
def history(session_id: str):
    return {"session_id": session_id, "history": get_history(session_id)}