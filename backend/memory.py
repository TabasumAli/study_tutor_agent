"""
Short-term (session) memory for the Study Tutor Agent.

We keep an in-process dictionary keyed by session_id.
Each session holds the recent conversation history (user + assistant turns).
This acts as short-term memory passed into CrewAI on each request.
"""

import threading
from collections import deque
from typing import Deque, Dict, List

MAX_TURNS = 6  # keep last 6 exchanges per session (short-term)

_lock = threading.Lock()
_sessions: Dict[str, Deque[dict]] = {}


def _get_session(session_id: str) -> Deque[dict]:
    if session_id not in _sessions:
        _sessions[session_id] = deque(maxlen=MAX_TURNS)
    return _sessions[session_id]


def add_turn(session_id: str, role: str, content: str) -> None:
    """role is 'user' or 'assistant'."""
    with _lock:
        _get_session(session_id).append({"role": role, "content": content})


def get_history(session_id: str) -> List[dict]:
    with _lock:
        return list(_get_session(session_id))


def format_history(session_id: str) -> str:
    """Format history as a readable string for the agent's context."""
    history = get_history(session_id)
    if not history:
        return "No prior conversation."
    lines = []
    for turn in history:
        prefix = "Student" if turn["role"] == "user" else "Tutor"
        lines.append(f"{prefix}: {turn['content']}")
    return "\n".join(lines)


def clear_session(session_id: str) -> None:
    with _lock:
        _sessions.pop(session_id, None)