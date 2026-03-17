from __future__ import annotations

from typing import List, Dict
import re


def _contains(text: str, keywords: list[str]) -> bool:
    text_low = text.lower()
    return any(k in text_low for k in keywords)


def generate_quiz_from_lesson(lesson) -> List[Dict]:
    """
    Rule-based quiz generator. Produces 3–5 MCQs from lesson title/content.
    Output format:
    [
      { "question": str, "options": [str, str, str, str], "correct": int },
      ...
    ]
    """
    title = (getattr(lesson, "title", "") or "").strip()
    content = (getattr(lesson, "content", "") or "").strip()
    text = f"{title}\n{content}"

    questions: List[Dict] = []

    if _contains(text, ["loop", "for ", "while "]):
        questions.append({
            "question": "Which statement iterates over a sequence in Python?",
            "options": ["for", "iterate", "repeat", "switch"],
            "correct": 0,
        })
        questions.append({
            "question": "What does 'break' do inside a loop?",
            "options": ["Skips to next iteration", "Exits the loop", "Restarts the loop", "Pauses the loop"],
            "correct": 1,
        })

    if _contains(text, ["variable", "assign", "value"]):
        questions.append({
            "question": "Which is a valid variable assignment in Python?",
            "options": ["x == 10", "10 = x", "x = 10", "assign x 10"],
            "correct": 2,
        })

    if _contains(text, ["list", "[]", "append"]):
        questions.append({
            "question": "How do you access the first element of a list 'nums'?",
            "options": ["nums(0)", "nums[1]", "nums[0]", "nums.first"],
            "correct": 2,
        })

    if _contains(text, ["function", "def ", "return"]):
        questions.append({
            "question": "Which keyword defines a function in Python?",
            "options": ["func", "def", "function", "lambda"],
            "correct": 1,
        })

    if _contains(text, ["class", "object", "method"]):
        questions.append({
            "question": "What keyword defines a class in Python?",
            "options": ["object", "class", "structure", "define"],
            "correct": 1,
        })

    if _contains(text, ["dict", "{}", "key"]):
        questions.append({
            "question": "How do you get a value from a dictionary `d` with key `k`?",
            "options": ["d(k)", "d.get(k)", "d[k]", "Both d.get(k) and d[k]"],
            "correct": 3,
        })

    if _contains(text, ["set", "unique", "add"]):
        questions.append({
            "question": "What is a key feature of a Python set?",
            "options": ["Ordered elements", "Allows duplicate elements", "Stores unique elements", "Key-value pairs"],
            "correct": 2,
        })

    if _contains(text, ["string", "slice", "strip"]):
        questions.append({
            "question": "What does the `strip()` method do on a string?",
            "options": ["Removes leading/trailing whitespace", "Converts to uppercase", "Splits the string into a list", "Replaces a substring"],
            "correct": 0,
        })

    # Fallback generic questions if we have fewer than 3
    if len(questions) < 3:
        questions.append({
            "question": "What does the Python len() function return?",
            "options": ["Length of a sequence", "Type of a variable", "Memory address", "None"],
            "correct": 0,
        })
    if len(questions) < 4:
        questions.append({
            "question": "Which symbol is used to start a comment in Python?",
            "options": ["//", "#", "/*", "<!--"],
            "correct": 1,
        })
    if len(questions) < 5:
        questions.append({
            "question": "Which data type is immutable in Python?",
            "options": ["List", "Dictionary", "Tuple", "Set"],
            "correct": 2,
        })

    return questions
