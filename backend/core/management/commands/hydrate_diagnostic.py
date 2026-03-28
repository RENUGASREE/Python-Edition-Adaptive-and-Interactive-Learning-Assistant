"""python manage.py hydrate_diagnostic -- 40 Question Professional Placement Quiz"""
from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import DiagnosticQuiz, DiagnosticQuestion

QUESTIONS = [
    # --- Module 1: Introduction ---
    {
        "topic": "mod-introduction", "difficulty": "Beginner",
        "text": "What is the primary extension for Python files?",
        "options": [".py", ".pyt", ".txt", ".exe"], "correct_index": 0
    },
    {
        "topic": "mod-introduction", "difficulty": "Beginner",
        "text": "Which command-line command is used to check the installed version of Python?",
        "options": ["python version", "python --version", "py -v", "check-python"], "correct_index": 1
    },
    {
        "topic": "mod-introduction", "difficulty": "Intermediate",
        "text": "Python is known for its readability. Which of these is a core design principle?",
        "options": ["Explicit is better than implicit", "Memory efficiency at all costs", "Strict static typing", "Manual resource cleanup"], "correct_index": 0
    },
    {
        "topic": "mod-introduction", "difficulty": "Pro",
        "text": "Which PEP (Python Enhancement Proposal) serves as the style guide for Python code?",
        "options": ["PEP 1", "PEP 13", "PEP 8", "PEP 484"], "correct_index": 2
    },

    # --- Module 2: Variables & Data Types ---
    {
        "topic": "mod-variables-types", "difficulty": "Beginner",
        "text": "How do you declare a variable named 'score' with a value of 100?",
        "options": ["var score = 100", "int score = 100", "score := 100", "score = 100"], "correct_index": 3
    },
    {
        "topic": "mod-variables-types", "difficulty": "Intermediate",
        "text": "What is the result of `type(3.0)`?",
        "options": ["<class 'int'>", "<class 'float'>", "<class 'double'>", "<class 'number'>"], "correct_index": 1
    },
    {
        "topic": "mod-variables-types", "difficulty": "Intermediate",
        "text": "Which collection type preserves the order of elements and is immutable?",
        "options": ["List", "Set", "Dictionary", "Tuple"], "correct_index": 3
    },
    {
        "topic": "mod-variables-types", "difficulty": "Pro",
        "text": "What is the output of `bool('')` in Python?",
        "options": ["True", "False", "None", "Error"], "correct_index": 1
    },

    # --- Module 3: Control Flow ---
    {
        "topic": "mod-control-flow", "difficulty": "Beginner",
        "text": "What is the correct logical operator for 'not equal'?",
        "options": ["<>", "==", "!=", "/="], "correct_index": 2
    },
    {
        "topic": "mod-control-flow", "difficulty": "Intermediate",
        "text": "The `match` keyword in Python 3.10 is used for:",
        "options": ["Regular expressions", "Structural Pattern Matching", "Finding items in a list", "Comparing identities"], "correct_index": 1
    },
    {
        "topic": "mod-control-flow", "difficulty": "Intermediate",
        "text": "In Python, which indentation style is the standard according to PEP 8?",
        "options": ["2 spaces", "4 spaces", "One tab", "Flexible"], "correct_index": 1
    },
    {
        "topic": "mod-control-flow", "difficulty": "Pro",
        "text": "What is the difference between '==' and 'is'?",
        "options": ["None", "'==' checks value, 'is' checks identity", "'is' checks value, '==' checks identity", "'is' only works for strings"], "correct_index": 1
    },

    # --- Module 4: Loops & Iteration ---
    {
        "topic": "mod-loops-iteration", "difficulty": "Beginner",
        "text": "What will `range(5)` produce in a loop?",
        "options": ["0, 1, 2, 3, 4", "1, 2, 3, 4, 5", "0, 1, 2, 3, 4, 5", "List of 5 ones"], "correct_index": 0
    },
    {
        "topic": "mod-loops-iteration", "difficulty": "Intermediate",
        "text": "What keyword is used to stop the current loop entirely?",
        "options": ["stop", "exit", "break", "continue"], "correct_index": 2
    },
    {
        "topic": "mod-loops-iteration", "difficulty": "Intermediate",
        "text": "How do you access both the index and the value in a for loop?",
        "options": ["With zip()", "With enumerate()", "With range(len())", "With map()"], "correct_index": 1
    },
    {
        "topic": "mod-loops-iteration", "difficulty": "Pro",
        "text": "When does the 'else' block of a for loop execute?",
        "options": ["Always", "Never", "If the loop finished without hitting a break", "If the loop was skipped"], "correct_index": 2
    },

    # --- Module 5: Functions & Scope ---
    {
        "topic": "mod-functions-scope", "difficulty": "Beginner",
        "text": "How do you define a function in Python?",
        "options": ["def my_func():", "function my_func():", "define my_func():", "method my_func():"], "correct_index": 0
    },
    {
        "topic": "mod-functions-scope", "difficulty": "Intermediate",
        "text": "What happens if a function has no 'return' statement?",
        "options": ["It returns None", "It returns False", "It returns an error", "It returns 0"], "correct_index": 0
    },
    {
        "topic": "mod-functions-scope", "difficulty": "Pro",
        "text": "What does a lambda function represent?",
        "options": ["A high-performance function", "An anonymous, one-line function", "A function that generates numbers", "A system process"], "correct_index": 1
    },
    {
        "topic": "mod-functions-scope", "difficulty": "Pro",
        "text": "Which keyword allows you to modify a global variable from inside a function?",
        "options": ["global", "nonlocal", "self", "outer"], "correct_index": 0
    },

    # --- Module 6: File Handling ---
    {
        "topic": "mod-file-handling", "difficulty": "Beginner",
        "text": "Which mode is used to append data to an existing file?",
        "options": ["'r'", "'w'", "'a'", "'x'"], "correct_index": 2
    },
    {
        "topic": "mod-file-handling", "difficulty": "Intermediate",
        "text": "What is the recommended way to handle file resources to ensure they close properly?",
        "options": ["Using f.close()", "Using the 'with' statement", "Using a try-catch-finally block", "Letting the garbage collector handle it"], "correct_index": 1
    },
    {
        "topic": "mod-file-handling", "difficulty": "Intermediate",
        "text": "Which standard library module is used for object-oriented path manipulation?",
        "options": ["os", "os.path", "pathlib", "shutil"], "correct_index": 2
    },
    {
        "topic": "mod-file-handling", "difficulty": "Pro",
        "text": "When opening a file with 'w', what happens if the file already exists?",
        "options": ["It appends to the end", "It raises an error", "It overwrites the entire file", "It creates a backup"], "correct_index": 2
    },

    # --- Module 7: Error Handling ---
    {
        "topic": "mod-error-handling", "difficulty": "Beginner",
        "text": "Which block is used to catch errors in Python?",
        "options": ["try", "except", "catch", "handle"], "correct_index": 1
    },
    {
        "topic": "mod-error-handling", "difficulty": "Intermediate",
        "text": "What is the purpose of the 'finally' block?",
        "options": ["Run only if an error occurred", "Run only if no error occurred", "Run regardless of whether an error occurred", "Stop the program"], "correct_index": 2
    },
    {
        "topic": "mod-error-handling", "difficulty": "Pro",
        "text": "What is the output of `1 / 0` in Python?",
        "options": ["0", "Infinity", "ZeroDivisionError", "None"], "correct_index": 2
    },
    {
        "topic": "mod-error-handling", "difficulty": "Pro",
        "text": "How do you manually trigger an exception?",
        "options": ["throw", "trigger", "raise", "fail"], "correct_index": 2
    },

    # --- Module 8: OOP ---
    {
        "topic": "mod-oop", "difficulty": "Beginner",
        "text": "What is the conventional first parameter of an instance method?",
        "options": ["this", "obj", "self", "cls"], "correct_index": 2
    },
    {
        "topic": "mod-oop", "difficulty": "Intermediate",
        "text": "What is the purpose of the super() function?",
        "options": ["To call methods of the parent class", "To make a method faster", "To define a static method", "To exit a method"], "correct_index": 0
    },
    {
        "topic": "mod-oop", "difficulty": "Intermediate",
        "text": "Inheriting from multiple parent classes is called:",
        "options": ["Single inheritance", "Hierarchical inheritance", "Multiple inheritance", "Polymorphism"], "correct_index": 2
    },
    {
        "topic": "mod-oop", "difficulty": "Pro",
        "text": "@classmethod vs @staticmethod: which one receives the class itself as an argument?",
        "options": ["@classmethod", "@staticmethod", "Both", "Neither"], "correct_index": 0
    },

    # --- Module 9: Advanced Python ---
    {
        "topic": "mod-advanced-python", "difficulty": "Pro",
        "text": "What is a decorator in Python?",
        "options": ["A function that wraps another function", "A tool to draw UI icons", "A static method", "A built-in variable"], "correct_index": 0
    },
    {
        "topic": "mod-advanced-python", "difficulty": "Pro",
        "text": "Generators in Python use which keyword to return values?",
        "options": ["return", "yield", "provide", "output"], "correct_index": 1
    },
    {
        "topic": "mod-advanced-python", "difficulty": "Pro",
        "text": "What is a closure?",
        "options": ["A function ending early", "A nested function that 'remembers' its outer scope", "A private class", "A code block that closes a file"], "correct_index": 1
    },
    {
        "topic": "mod-advanced-python", "difficulty": "Pro",
        "text": "Which tool provides memory-efficient, lazy iteration over sequences?",
        "options": ["List", "Generator", "Dictionary", "Tuple"], "correct_index": 1
    },

    # --- Module 10: Projects ---
    {
        "topic": "mod-real-world-projects", "difficulty": "Pro",
        "text": "Which tool is used to install and manage third-party libraries?",
        "options": ["npm", "pip", "brew", "apt"], "correct_index": 1
    },
    {
        "topic": "mod-real-world-projects", "difficulty": "Pro",
        "text": "What is the purpose of a virtual environment?",
        "options": ["Run code faster", "Isolate project dependencies", "Simulate a different OS", "Encrypt source code"], "correct_index": 1
    },
    {
        "topic": "mod-real-world-projects", "difficulty": "Pro",
        "text": "Which library is standard for handling HTTP requests in professional Python?",
        "options": ["math", "requests", "sys", "re"], "correct_index": 1
    },
    {
        "topic": "mod-real-world-projects", "difficulty": "Pro",
        "text": "In a FastAPI or Flask application, what is a 'route'?",
        "options": ["A type of list", "A URL path linked to a function", "A database connection", "A loop direction"], "correct_index": 1
    },
]

class Command(BaseCommand):
    help = "Hydrate professional diagnostic placement quiz with 40 questions"

    def handle(self, *args, **options):
        self.stdout.write("🧹 Cleaning up old diagnostic data...")
        DiagnosticQuiz.objects.filter(title__iexact="Python Placement Diagnostic").delete()
        
        quiz = DiagnosticQuiz.objects.create(title="Python Placement Diagnostic")
        
        self.stdout.write(f"🚀 Seeding 40 diagnostic questions...")
        
        with transaction.atomic():
            for q_data in QUESTIONS:
                DiagnosticQuestion.objects.create(
                    quiz=quiz,
                    topic=q_data["topic"],
                    difficulty=q_data["difficulty"],
                    text=q_data["text"],
                    options=q_data["options"],
                    correct_index=q_data["correct_index"]
                )
        
        self.stdout.write(self.style.SUCCESS(f"✅ Successfully hydrated {DiagnosticQuestion.objects.filter(quiz=quiz).count()} questions."))
