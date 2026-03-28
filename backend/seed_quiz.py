import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from assessments.models import DiagnosticQuiz, DiagnosticQuestion

def seed_quiz_questions():
    quiz = DiagnosticQuiz.objects.filter(title__iexact="Python Placement Diagnostic").first()
    if not quiz:
        quiz = DiagnosticQuiz.objects.create(title="Python Placement Diagnostic")
    
    questions = [
        {
            "topic": "Python Intro",
            "difficulty": "Beginner",
            "text": "What is the primary goal of Python's design philosophy?",
            "options": ["Readability", "Execution speed", "Memory efficiency", "Platform dependency"],
            "correct_index": 0
        },
        {
            "topic": "Variables",
            "difficulty": "Beginner",
            "text": "Which of these is a valid variable name?",
            "options": ["1_var", "my-var", "my_var", "var!"],
            "correct_index": 2
        },
        {
            "topic": "Python Lists",
            "difficulty": "Intermediate",
            "text": "Which method is used to add an item to the end of a list?",
            "options": ["insert()", "add()", "append()", "push()"],
            "correct_index": 2
        },
        {
            "topic": "If-Else Statements",
            "difficulty": "Intermediate",
            "text": "What keyword is used for 'else if' in Python?",
            "options": ["elseif", "elif", "else if", "switf"],
            "correct_index": 1
        },
        {
            "topic": "Loops",
            "difficulty": "Beginner",
            "text": "How many times will a 'for i in range(5)' loop run?",
            "options": ["4", "5", "6", "Infinite"],
            "correct_index": 1
        },
        {
            "topic": "Classes and Objects",
            "difficulty": "Pro",
            "text": "What is the purpose of the '__init__' method?",
            "options": ["Deleting objects", "Initializing object state", "Defining class methods", "Inheriting attributes"],
            "correct_index": 1
        }
    ]

    print("🚀 Seeding Diagnostic Questions...")
    for q_data in questions:
        # Check if exists
        if not DiagnosticQuestion.objects.filter(text=q_data["text"]).exists():
            DiagnosticQuestion.objects.create(
                quiz=quiz,
                topic=q_data["topic"],
                difficulty=q_data["difficulty"],
                text=q_data["text"],
                options=q_data["options"],
                correct_index=q_data["correct_index"]
            )
    print("✅ Questions Seeded.")

if __name__ == "__main__":
    seed_quiz_questions()
