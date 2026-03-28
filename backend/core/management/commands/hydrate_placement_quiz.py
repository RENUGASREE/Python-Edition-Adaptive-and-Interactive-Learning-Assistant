"""python manage.py hydrate_placement_quiz -- Consolidated Professional Diagnostic Quiz for Assessments App"""
from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import DiagnosticQuiz, DiagnosticQuestion
from core.models import Quiz, Question, DiagnosticQuestionMeta

QUESTIONS = [
    # --- Module 1: Basics ---
    {"topic": "mod-introduction", "text": "Which function is used to display output to the console in Python?", "options": ["print()", "echo()", "log()", "display()"], "correct_index": 0},
    {"topic": "mod-introduction", "text": "What is the correct way to take string input from a user?", "options": ["input('Prompt')", "get_string()", "read()", "prompt()"], "correct_index": 0},
    {"topic": "mod-introduction", "text": "How do you start a single-line comment in Python?", "options": ["#", "//", "/*", "<!--"], "correct_index": 0},
    {"topic": "mod-introduction", "text": "What does the `\\n` character represent in a string?", "options": ["A new line", "A tab space", "A null character", "A backspace"], "correct_index": 0},

    # --- Module 2: Variables & Types ---
    {"topic": "mod-variables-types", "text": "Which of these is a valid Python variable name?", "options": ["my_variable_1", "1_variable", "my-variable", "global"], "correct_index": 0},
    {"topic": "mod-variables-types", "text": "What is the data type of the value `3.14`?", "options": ["float", "int", "decimal", "double"], "correct_index": 0},
    {"topic": "mod-variables-types", "text": "Which collection type is unordered and does not allow duplicate elements?", "options": ["set", "list", "tuple", "dict"], "correct_index": 0},
    {"topic": "mod-variables-types", "text": "How do you create a dictionary in Python?", "options": ["{'key': 'value'}", "['key': 'value']", "('key', 'value')", "{'key', 'value'}"], "correct_index": 0},

    # --- Module 3: Control Flow ---
    {"topic": "mod-control-flow", "text": "What is the result of `5 > 3 and 2 > 4`?", "options": ["False", "True", "None", "Error"], "correct_index": 0},
    {"topic": "mod-control-flow", "text": "Which keyword is used for 'else if' in Python?", "options": ["elif", "elseif", "else if", "if else"], "correct_index": 0},
    {"topic": "mod-control-flow", "text": "The `match` statement (structural pattern matching) was introduced in which Python version?", "options": ["3.10", "3.8", "3.9", "3.11"], "correct_index": 0},
    {"topic": "mod-control-flow", "text": "What does the `is` operator compare in Python?", "options": ["Memory identity (ID)", "Value equality", "Type equality", "Logical truth"], "correct_index": 0},

    # --- Module 4: Loops ---
    {"topic": "mod-loops-iteration", "text": "Which loop is best used when you know the exact number of iterations?", "options": ["for loop", "while loop", "do-while loop", "infinite loop"], "correct_index": 0},
    {"topic": "mod-loops-iteration", "text": "What keyword is used to skip the rest of the current loop iteration and move to the next one?", "options": ["continue", "break", "pass", "skip"], "correct_index": 0},
    {"topic": "mod-loops-iteration", "text": "What is the output of `list(range(2, 10, 2))`?", "options": ["[2, 4, 6, 8]", "[2, 3, 4, 5, 6, 7, 8, 9]", "[2, 4, 6, 8, 10]", "[4, 6, 8]"], "correct_index": 0},
    {"topic": "mod-loops-iteration", "text": "Which statement allows an 'else' block to run only if the loop finished normally (without a break)?", "options": ["for...else", "if...else", "while...finally", "try...else"], "correct_index": 0},

    # --- Module 5: Functions ---
    {"topic": "mod-functions-scope", "text": "How do you define a function in Python?", "options": ["def my_func():", "function my_func():", "func my_func():", "define my_func():"], "correct_index": 0},
    {"topic": "mod-functions-scope", "text": "What is the purpose of `*args` in a function signature?", "options": ["To accept a variable number of positional arguments as a tuple", "To accept a variable number of keyword arguments as a dictionary", "To make all arguments optional", "To multiply the arguments"], "correct_index": 0},
    {"topic": "mod-functions-scope", "text": "What is a 'lambda' function in Python?", "options": ["A small anonymous function", "A recursive function", "A function that returns multiple values", "A generator function"], "correct_index": 0},
    {"topic": "mod-functions-scope", "text": "What keyword is used to return a value from a function?", "options": ["return", "give", "output", "yield"], "correct_index": 0},

    # --- Module 6: File Handling ---
    {"topic": "mod-file-handling", "text": "Which mode is used to open a file for both reading and writing (updating)?", "options": ["r+", "w", "a", "rb"], "correct_index": 0},
    {"topic": "mod-file-handling", "text": "What is the primary benefit of using the `with` statement when opening files?", "options": ["It ensures the file is automatically closed", "It makes the file read faster", "It encrypts the file", "It allows multiple users to edit"], "correct_index": 0},
    {"topic": "mod-file-handling", "text": "Which library is the modern, object-oriented way to handle file paths in Python?", "options": ["pathlib", "os.path", "filesys", "shutil"], "correct_index": 0},
    {"topic": "mod-file-handling", "text": "What method is used to read all lines of a file into a list?", "options": ["readlines()", "read_all()", "get_lines()", "list()"], "correct_index": 0},

    # --- Module 7: Exceptions ---
    {"topic": "mod-error-handling", "text": "Which block is used to catch and handle exceptions in Python?", "options": ["except", "catch", "handle", "rescue"], "correct_index": 0},
    {"topic": "mod-error-handling", "text": "What is the purpose of the `finally` block?", "options": ["To execute code regardless of whether an exception occurred", "To catch the final exception", "To end the program gracefully", "To re-raise the exception"], "correct_index": 0},
    {"topic": "mod-error-handling", "text": "How do you manually trigger an exception in your code?", "options": ["raise Exception('Error')", "trigger Exception('Error')", "throw Exception('Error')", "fail Exception('Error')"], "correct_index": 0},
    {"topic": "mod-error-handling", "text": "What does a `ZeroDivisionError` indicate?", "options": ["An attempt to divide a number by zero", "A variable was not initialized", "An index was out of range", "The math module is missing"], "correct_index": 0},

    # --- Module 8: OOP ---
    {"topic": "mod-oop", "text": "What does the `self` parameter represent in a class method?", "options": ["The specific instance of the class", "The class constructor", "A global variable", "The parent class"], "correct_index": 0},
    {"topic": "mod-oop", "text": "Which 'Dunder' method is called when an object is initialized?", "options": ["__init__", "__new__", "__start__", "__create__"], "correct_index": 0},
    {"topic": "mod-oop", "text": "What is 'Inheritance' in OOP?", "options": ["A way to create a new class based on an existing class", "Hiding internal data from the user", "The ability of a method to take many forms", "Comparing two objects for equality"], "correct_index": 0},
    {"topic": "mod-oop", "text": "What is the purpose of the `@property` decorator?", "options": ["To treat a class method as an attribute (getter)", "To make a method private", "To speed up method calls", "To define a static variable"], "correct_index": 0},

    # --- Module 9: Advanced ---
    {"topic": "mod-advanced-python", "text": "What is a 'Generator' in Python?", "options": ["A function that uses `yield` to return a stream of values lazily", "A tool to compile Python to C", "A class that generates random numbers", "A script that creates other scripts"], "correct_index": 0},
    {"topic": "mod-advanced-python", "text": "Which decorator is used to fix the metadata (__name__, __doc__) of a wrapped function?", "options": ["@functools.wraps", "@decorator.fix", "@wraps.metadata", "@functools.meta"], "correct_index": 0},
    {"topic": "mod-advanced-python", "text": "What is the 'GIL' in CPython?", "options": ["Global Interpreter Lock", "General Interface Library", "Generic Integer List", "Graph Interpretation Layer"], "correct_index": 0},
    {"topic": "mod-advanced-python", "text": "Which method is used to wait for a thread to finish executing?", "options": ["join()", "wait()", "stop()", "end()"], "correct_index": 0},

    # --- Module 10: General/Projects ---
    {"topic": "mod-real-world-projects", "text": "Which library is built-in for handling JSON data?", "options": ["json", "simplejson", "jsondata", "requests"], "correct_index": 0},
    {"topic": "mod-real-world-projects", "text": "What command creates a virtual environment in modern Python?", "options": ["python -m venv env", "venv create env", "virtualenv start", "pip install env"], "correct_index": 0},
    {"topic": "mod-real-world-projects", "text": "What is the primary use of the `pip` tool?", "options": ["To install and manage Python packages", "To compile Python code", "To debug logic errors", "To create desktop icons"], "correct_index": 0},
    {"topic": "mod-real-world-projects", "text": "Which of these is a popular modern web framework for building APIs in Python?", "options": ["FastAPI", "Pandas", "Matplotlib", "Pytest"], "correct_index": 0},
]

class Command(BaseCommand):
    help = "Hydrate Consolidated Diagnostic Placement Quiz for Assessments App"

    def handle(self, *args, **options):
        self.stdout.write("🧹 Cleaning up old placement quizzes in both apps...")
        # Core app cleanup
        Quiz.objects.filter(id="quiz-placement-test").delete()
        Question.objects.filter(quiz_id="quiz-placement-test").delete()
        DiagnosticQuestionMeta.objects.all().delete()
        
        # Assessments app cleanup
        DiagnosticQuiz.objects.filter(title__iexact="Python Placement Diagnostic").delete()
        
        quiz = DiagnosticQuiz.objects.create(
            title="Python Placement Diagnostic"
        )

        self.stdout.write(f"🚀 Hydrating 40 diagnostic questions for {quiz.title} into assessments app...")

        with transaction.atomic():
            for q_data in QUESTIONS:
                DiagnosticQuestion.objects.create(
                    quiz=quiz,
                    topic=q_data["topic"],
                    difficulty="Intermediate",
                    text=q_data["text"],
                    options=q_data["options"],
                    correct_index=q_data["correct_index"]
                )

        self.stdout.write(self.style.SUCCESS(f"✅ Successfully hydrated {len(QUESTIONS)} diagnostic questions in Assessments system."))
