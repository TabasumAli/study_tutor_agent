"""
Custom tools available to the Study Tutor Agent.
Each tool is defined using CrewAI's @tool decorator.
"""

from crewai.tools import tool
import json


@tool("Explain Concept")
def explain_concept(topic: str) -> str:
    """
    Generate a structured explanation plan for a given topic.
    Useful for breaking down a concept into digestible parts.
    """
    return (
        f"Provide a clear, structured explanation of '{topic}'. Include:\n"
        f"1. A simple definition\n"
        f"2. Why it matters\n"
        f"3. A real-world analogy\n"
        f"4. Key sub-points (3-5 bullets)\n"
        f"5. A common misconception\n"
        f"Keep it beginner-friendly but accurate."
    )


@tool("Generate Quiz")
def generate_quiz(topic: str, num_questions: int = 5) -> str:
    """
    Generate quiz questions for a given topic.
    Returns instructions for the agent to create a quiz.
    """
    return (
        f"Create {num_questions} quiz questions on '{topic}'. "
        f"Mix of multiple-choice and short-answer. "
        f"Provide an answer key at the end with brief explanations."
    )


@tool("Create Study Plan")
def create_study_plan(topic: str, days: int = 7) -> str:
    """
    Create a day-by-day study plan for a topic.
    """
    return (
        f"Design a {days}-day study plan for '{topic}'. "
        f"For each day include: focus area, learning objective, "
        f"estimated time (minutes), and a small practice task."
    )


@tool("Summarize Text")
def summarize_text(text: str) -> str:
    """
    Produce a concise summary of provided study material.
    """
    return (
        f"Summarize the following study material into key takeaways, "
        f"a 3-sentence overview, and 3 flashcards (Q/A pairs):\n\n{text}"
    )


@tool("Flashcard Maker")
def flashcard_maker(topic: str, count: int = 8) -> str:
    """
    Create flashcards for spaced repetition on a given topic.
    """
    return (
        f"Generate {count} flashcards on '{topic}'. "
        f"Format each as:\nQ: <question>\nA: <concise answer>\n"
        f"Cover core definitions, formulas, and edge cases."
    )


ALL_TOOLS = [
    explain_concept,
    generate_quiz,
    create_study_plan,
    summarize_text,
    flashcard_maker,
]