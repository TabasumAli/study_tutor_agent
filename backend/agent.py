"""
CrewAI single-agent Study Tutor.
Uses Groq's openai/gpt-oss-120b model.
"""

import os
from crewai import Agent, Task, Crew, Process, LLM
from tools import ALL_TOOLS
from memory import format_history


def build_llm(api_key: str) -> LLM:
    """Groq LLM wrapper compatible with CrewAI (litellm under the hood)."""
    os.environ["GROQ_API_KEY"] = api_key
    return LLM(
        model="groq/openai/gpt-oss-120b",
        temperature=0.4,
        api_key=api_key,
    )


def build_agent(llm: LLM) -> Agent:
    return Agent(
        role="Study Tutor",
        goal=(
            "Help students learn any topic deeply by explaining concepts, "
            "creating quizzes, flashcard sets, and personalized study plans."
        ),
        backstory=(
            "You are a patient, encouraging, and highly knowledgeable tutor "
            "with expertise across math, science, humanities, and programming. "
            "You use tools when they help produce a better structured answer. "
            "You always tailor explanations to the student's level and "
            "reference the ongoing conversation for continuity."
        ),
        tools=ALL_TOOLS,
        llm=llm,
        verbose=False,
        allow_delegation=False,
        max_iter=5,
    )


def run_tutor(api_key: str, session_id: str, user_message: str) -> str:
    """
    Run the single-agent crew for one user turn.
    Short-term memory (conversation history) is injected into the task.
    """
    llm = build_llm(api_key)
    agent = build_agent(llm)

    history = format_history(session_id)

    description = (
        f"Conversation so far (short-term memory):\n{history}\n\n"
        f"Student's new message:\n{user_message}\n\n"
        f"Instructions:\n"
        f"- Respond directly to the student in a friendly, tutor-like tone.\n"
        f"- If the student asks for a quiz, plan, flashcards, summary, or an "
        f"explanation, USE the relevant tool to structure your answer.\n"
        f"- Keep answers focused but complete. Use markdown formatting.\n"
    )

    task = Task(
        description=description,
        expected_output=(
            "A helpful, well-formatted tutor response in markdown that "
            "directly addresses the student's request."
        ),
        agent=agent,
    )

    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)