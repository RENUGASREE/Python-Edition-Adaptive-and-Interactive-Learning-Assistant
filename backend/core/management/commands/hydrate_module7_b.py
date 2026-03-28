"""python manage.py hydrate_module7_b -- Module 7 Error Handling Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: Custom Exception Classes ───────────────────────────────────
    "les-error-handling-6-beginner": {
        "title": "Creating Your Own Exceptions",
        "content": """# Creating Your Own Exceptions

## 🎯 Learning Objectives
- Define custom exception classes
- Understand why inheriting from `Exception` is necessary
- Distinguish your library's errors from standard Python errors

## 📚 Concept Overview
Standard exceptions like `ValueError` are sometimes too generic. If you're building a Banking app, you might want an `InsufficientFundsError`.

```python
class InsufficientFundsError(Exception):
    \"\"\"Raised when the account balance is too low.\"\"\"
    pass

# Usage
balance = 100
if balance < 500:
    raise InsufficientFundsError("You need at least 500!")
```

## 🏆 Key Takeaways
- Custom exceptions should always inherit from the built-in `Exception` class.
- They help other developers understand exactly "what" went wrong in your specific domain.
""",
        "questions": [
            {"text": "Which class must a custom exception inherit from?", "options": [
                {"text": "Exception", "correct": True}, {"text": "Error", "correct": False},
                {"text": "BaseObject", "correct": False}, {"text": "Problem", "correct": False}]},
            {"text": "What is the primary benefit of custom exceptions?", "options": [
                {"text": "Clearer, more descriptive error reporting for specific domains", "correct": True},
                {"text": "Making the code run faster", "correct": False},
                {"text": "Catching syntax errors", "correct": False},
                {"text": "Encryption", "correct": False}]},
        ],
        "challenge": {
            "title": "Bank Error",
            "description": "Define a custom exception `WithdrawalError`. Write code to raise it if a variable `amount` is greater than 1000.",
            "initial_code": "class WithdrawalError(Exception): pass\namount = 2000\n# check and raise\n",
            "solution_code": "class WithdrawalError(Exception): pass\namount = 2000\nif amount > 1000:\n    raise WithdrawalError('Too much')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-error-handling-6-intermediate": {
        "title": "Adding Data to Exceptions",
        "content": """# Adding Data to Exceptions

## 🎯 Learning Objectives
- Add custom attributes to your exception classes
- override `__init__` and `__str__`
- Provide rich error information to the catcher

## 📚 Concept Overview
You can store specific details (like a status code or a timestamp) inside the error object.

```python
class ValidationError(Exception):
    def __init__(self, message, field_name):
        super().__init__(message)
        self.field_name = field_name

try:
    raise ValidationError("Required", "email")
except ValidationError as e:
    print(f"Error in field: {e.field_name}")
```

## 🏆 Key Takeaways
- Custom exceptions are just regular classes! You can add any methods or properties you want.
""",
        "questions": [
            {"text": "How do you add custom data to an exception class?", "options": [
                {"text": "By overriding the __init__ method", "correct": True},
                {"text": "By using the 'meta' keyword", "correct": False},
                {"text": "It is not possible", "correct": False},
                {"text": "By setting global variables", "correct": False}]},
        ],
        "challenge": {
            "title": "Rich Error",
            "description": "Modify `AppError` to accept a `code` (int). Raise it with code 404.",
            "initial_code": "class AppError(Exception):\n    # add init\n    pass\n",
            "solution_code": "class AppError(Exception):\n    def __init__(self, msg, code):\n        super().__init__(msg)\n        self.code = code\nraise AppError('NF', 404)\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-error-handling-6-pro": {
        "title": "Exception Nesting & Hierarchies",
        "content": """# Exception Nesting & Hierarchies

## 🎯 Learning Objectives
- Build a tree of related custom exceptions
- Catch "General" vs "Specific" custom errors
- Organize errors in a large project

## 📚 Concept Overview
Professional libraries often have one base exception and many specific children.

```python
class MyLibraryError(Exception): pass
class NetworkError(MyLibraryError): pass
class DatabaseError(MyLibraryError): pass

try:
    # ...
except MyLibraryError: # Catches BOTH Network and Database errors
    print("Something went wrong in the library")
```

## 🏆 Key Takeaways
- Broad base exceptions allow users to catch "Any error from this library" easily.
""",
        "questions": [
            {"text": "If `DatabaseError` inherits from `MyBaseError`, what happens if you try to catch `MyBaseError`?", "options": [
                {"text": "It will catch DatabaseError too", "correct": True},
                {"text": "It will ignore DatabaseError", "correct": False},
                {"text": "The computer will crash", "correct": False},
                {"text": "Python will warn you", "correct": False}]},
        ],
        "challenge": {
            "title": "Base Catcher",
            "description": "Create a base `APIError` and a child `AuthError`. Write an `except` block that catches both but only uses one class name.",
            "initial_code": "# Definitions\n",
            "solution_code": "class APIError(Exception): pass\nclass AuthError(APIError): pass\ntry:\n    raise AuthError()\nexcept APIError:\n    print('Caught')\n",
            "test_cases": [{"input": "", "expected": "Caught"}],
        },
    },

    # ── Lesson 7: Exception Best Practices ──────────────────────────────────
    "les-error-handling-7-beginner": {
        "title": "Exception Best Practices",
        "content": """# Exception Best Practices

## 🎯 Learning Objectives
- Write clean and maintainable error handling code
- Understand "LBYL" vs "EAFP"
- Avoid anti-patterns

## 📚 Concept Overview
### EAFP (Easier to Ask for Forgiveness than Permission)
This is the Python way. Try something, and handle it if it fails.
```python
# Python style (EAFP)
try:
    do_work()
except:
    # handle
```

### LBYL (Look Before You Leap)
Common in C/Java. Check first.
```python
# C style (LBYL)
if can_do_work():
    do_work()
```

## 🏆 Key Takeaways
- Prefer EAFP in Python. It's more readable and often faster.
- Never use a bare `except:`!
""",
        "questions": [
            {"text": "What does EAFP stand for?", "options": [
                {"text": "Easier to Ask for Forgiveness than Permission", "correct": True},
                {"text": "Every Error Always Fixed Promptly", "correct": False},
                {"text": "Executive Error Finding Program", "correct": False},
                {"text": "Errors Are Frequently Present", "correct": False}]},
            {"text": "What is considered a major 'anti-pattern' in Python error handling?", "options": [
                {"text": "Using a bare 'except:' without a type", "correct": True},
                {"text": "Using 'with' statements", "correct": False},
                {"text": "Using 'finally'", "correct": False},
                {"text": "Defining custom classes", "correct": False}]},
        ],
        "challenge": {
            "title": "EAFP style",
            "description": "You have a dictionary `d = {}`. Write the EAFP way to print `d['key']` or 'MISS' if missing.",
            "initial_code": "d = {}\n# write in EAFP style\n",
            "solution_code": "d = {}\ntry:\n    print(d['key'])\nexcept KeyError:\n    print('MISS')\n",
            "test_cases": [{"input": "", "expected": "MISS"}],
        },
    },

    "les-error-handling-7-intermediate": {
        "title": "Minimal Try Blocks",
        "content": """# Minimal Try Blocks

## 🎯 Learning Objectives
- Keep `try` blocks as small as possible
- Avoid "Double Catching" errors
- Use `else` to clarify intent

## 📚 Concept Overview
If you have a 50-line `try` block, a `ValueError` on line 2 might be caught by the same handler as a `ValueError` on line 45. This makes debugging impossible!

### Better:
```python
try:
    num = int(input()) # Only this line might raise ValueError
except ValueError:
    print("Input error")
else:
    process_big_logic(num) # This runs without being inside the 'try'
```

## 🏆 Key Takeaways
- Smaller `try` blocks make your code much easier to debug.
""",
        "questions": [
            {"text": "Why should you keep the code inside a `try` block minimal?", "options": [
                {"text": "To ensure we only catch the specific error we intended to handle", "correct": True},
                {"text": "To make the file smaller", "correct": False},
                {"text": "To avoid slow execution", "correct": False},
                {"text": "It is required for performance", "correct": False}]},
        ],
        "challenge": {
            "title": "Cleanup Attempt",
            "description": "You are given a snippet with 3 lines in a try block. One line opens a file, one reads it, one closes it. Which line is the SAFEST to move out of 'try' and into 'finally'?",
            "initial_code": "# answer: open, read, or close\n",
            "solution_code": "print('close')\n",
            "test_cases": [{"input": "", "expected": "close"}],
        },
    },

    "les-error-handling-7-pro": {
        "title": "Exception Suppression",
        "content": """# Exception Suppression

## 🎯 Learning Objectives
- Use `contextlib.suppress` to ignore errors elegantly
- Understand when it's safe to "silent" an error
- Compare `suppress` vs `try/except: pass`

## 📚 Concept Overview
```python
from contextlib import suppress
import os

# Instead of try: os.remove(f); except: pass
with suppress(FileNotFoundError):
    os.remove("junk.txt")
```

## 🏆 Key Takeaways
- `suppress` is more readable and explicitly states which error is being ignored and why.
""",
        "questions": [
            {"text": "Which module provides the `suppress` context manager?", "options": [
                {"text": "contextlib", "correct": True}, {"text": "sys", "correct": False},
                {"text": "os", "correct": False}, {"text": "errorlib", "correct": False}]},
        ],
        "challenge": {
            "title": "Elegant Silence",
            "description": "From `contextlib` import `suppress`. Use it to ignore a `ZeroDivisionError` when calculating `1/0`.",
            "initial_code": "from contextlib import suppress\n# do work\n",
            "solution_code": "from contextlib import suppress\nwith suppress(ZeroDivisionError):\n    1/0\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    # ── Lesson 8: Logging Exceptions ─────────────────────────────────────────
    "les-error-handling-8-beginner": {
        "title": "The Logging Module",
        "content": """# The Logging Module

## 🎯 Learning Objectives
- Understand why `print()` is NOT a logger
- Use `logging.error()` and `logging.warning()`
- Log to files instead of the console

## 📚 Concept Overview
Loggers can be configured to save errors to a file for later inspection.

```python
import logging
logging.basicConfig(filename="app.log", level=logging.ERROR)

try:
    1 / 0
except ZeroDivisionError:
    logging.error("Divided by zero!")
```

## 🏆 Key Takeaways
- Logs have priority levels: DEBUG, INFO, WARNING, ERROR, CRITICAL.
""",
        "questions": [
            {"text": "What is a main advantage of logging over printing?", "options": [
                {"text": "It can save errors to files and can be disabled easily without removing code", "correct": True},
                {"text": "It's faster", "correct": False},
                {"text": "It can be read by babies", "correct": False},
                {"text": "It's newer", "correct": False}]},
            {"text": "Which level is higher in priority?", "options": [
                {"text": "CRITICAL", "correct": True}, {"text": "INFO", "correct": False},
                {"text": "DEBUG", "correct": False}, {"text": "WARNING", "correct": False}]},
        ],
        "challenge": {
            "title": "Logging Setup",
            "description": "Write the `logging.basicConfig` line to log into a file named 'errors.txt'.",
            "initial_code": "import logging\n# config line\n",
            "solution_code": "import logging\nlogging.basicConfig(filename='errors.txt')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-error-handling-8-intermediate": {
        "title": "Logging Stack Traces",
        "content": """# Logging Stack Traces

## 🎯 Learning Objectives
- Use `logging.exception()` to save the full traceback
- Understand why the traceback is critical for debugging
- Inspect logs for line numbers and file names

## 📚 Concept Overview
Just logging "Error" is not enough. You need to know **where** and **why**.
`logging.exception()` automatically includes the stack trace.

```python
try:
    process_data()
except Exception:
    logging.exception("Failed to process data")
```

## 🏆 Key Takeaways
- `logging.exception()` should only be used inside an `except` block.
""",
        "questions": [
            {"text": "Which logging method automatically includes the full Traceback info?", "options": [
                {"text": "logging.exception()", "correct": True}, {"text": "logging.log_trace()", "correct": False},
                {"text": "logging.error(trace=True)", "correct": False}, {"text": "logging.dump()", "correct": False}]},
        ],
        "challenge": {
            "title": "Full Trace",
            "description": "Within an `except` block for any Error, use the correct method to log the message 'System Failure' with a full traceback.",
            "initial_code": "try:\n    pass\nexcept Exception:\n    # log correctly\n",
            "solution_code": "try:\n    pass\nexcept Exception:\n    import logging\n    logging.exception('System Failure')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-error-handling-8-pro": {
        "title": "Logging Configurations (DictConfig)",
        "content": """# Logging Configurations (DictConfig)

## 🎯 Learning Objectives
- Use professional YAML/Dict configurations for logging
- Set up different destinations for different modules
- Master the `Logger`, `Handler`, and `Formatter` trio

## 📚 Concept Overview
1. **Logger**: The entry point.
2. **Handler**: Sends logs to destination (File, Console, Email).
3. **Formatter**: Decides the layout (Time, Level, Message).

## 🏆 Key Takeaways
- High-level enterprise apps use `logging.config.dictConfig` for ultimate flexibility.
""",
        "questions": [
            {"text": "In the logging ecosystem, what component decides WHERE the log goes (e.g. file vs terminal)?", "options": [
                {"text": "Handler", "correct": True}, {"text": "Logger", "correct": False},
                {"text": "Formatter", "correct": False}, {"text": "Level", "correct": False}]},
        ],
        "challenge": {
            "title": "Components",
            "description": "Name the object that decides which level (e.g. INFO) is allowed to pass through.",
            "initial_code": "# answer: Handler or Logger or Formatter\n",
            "solution_code": "print('Logger')\n",
            "test_cases": [{"input": "", "expected": "Logger"}],
        },
    },

    # ── Lesson 9: Tracebacks & Debugging ─────────────────────────────────────
    "les-error-handling-9-beginner": {
        "title": "Reading a Traceback",
        "content": """# Reading a Traceback

## 🎯 Learning Objectives
- Learn to read an error message from bottom to top
- Identify the type of error and the file/line number
- Differentiate between "Your code" and "Framework code" in a trace

## 📚 Concept Overview
Tracebacks are not random noise!
1. **Bottom line**: The *type* and *summary* of the error.
2. **Middle lines**: The file path and line number.
3. **Top lines**: The path the execution took to get to that error.

## 🏆 Key Takeaways
- Always read the **last line** first.
""",
        "questions": [
            {"text": "Where is the most important information (Type of Error) usually located in a Traceback?", "options": [
                {"text": "The very bottom line", "correct": True}, {"text": "The very top line", "correct": False},
                {"text": "Somewhere in the middle", "correct": False}, {"text": "In a separate log file", "correct": False}]},
        ],
        "challenge": {
            "title": "Path Finder",
            "description": "True or False: A traceback lists every file involved in the path to the crash.",
            "initial_code": "# True or False?\n",
            "solution_code": "print('True')\n",
            "test_cases": [{"input": "", "expected": "True"}],
        },
    },

    "les-error-handling-9-intermediate": {
        "title": "The pdb Debugger",
        "content": """# The pdb Debugger

## 🎯 Learning Objectives
- Use the built-in Python debugger
- Set breakpoints using `breakpoint()`
- Step through code line-by-line

## 📚 Concept Overview
Instead of `print()` debugging, use `breakpoint()`.
It pauses execution and gives you a terminal inside your running program!

```python
x = 10
breakpoint() # Program stops here!
y = 20
```

### Commands:
- `n` (next line)
- `c` (continue to end)
- `q` (quit)
- `p variable` (print variable)

## 🏆 Key Takeaways
- `breakpoint()` is the modern (3.7+) way to debug.
""",
        "questions": [
            {"text": "Which built-in function is the standard way to pause execution and start the debugger?", "options": [
                {"text": "breakpoint()", "correct": True}, {"text": "debugger()", "correct": False},
                {"text": "pause()", "correct": False}, {"text": "stop()", "correct": False}]},
        ],
        "challenge": {
            "title": "Debugger command",
            "description": "In PDB, what single letter command continues the program until the next breakpoint or the end?",
            "initial_code": "# cmd\n",
            "solution_code": "print('c')\n",
            "test_cases": [{"input": "", "expected": "c"}],
        },
    },

    "les-error-handling-9-pro": {
        "title": "Post-Mortem Debugging",
        "content": """# Post-Mortem Debugging

## 🎯 Learning Objectives
- Enter the debugger AFTER a crash
- Use `pdb.pm()` and `sys.last_traceback`
- Inspect variables at the exact moment of failure

## 📚 Concept Overview
If a script fails in the REPL, you can jump into the state it was in right before crashing.

```python
import pdb
pdb.pm()
```

## 🏆 Key Takeaways
- Post-mortem debugging is a superpower for fixing bugs that are hard to reproduce.
""",
        "questions": [
            {"text": "Which module and function allow for 'post-mortem' debugging in Python?", "options": [
                {"text": "pdb.pm()", "correct": True}, {"text": "sys.debug()", "correct": False},
                {"text": "os.check_crash()", "correct": False}, {"text": "error.inspect()", "correct": False}]},
        ],
        "challenge": {
            "title": "Variable State",
            "description": "True or False: In post-mortem debugging, you can see the values of variables as they were when the crash happened.",
            "initial_code": "# Fact check\n",
            "solution_code": "print('True')\n",
            "test_cases": [{"input": "", "expected": "True"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-error-handling-10-beginner": {
        "title": "Project: User Input Protector",
        "content": """# Project: User Input Protector

## 🎯 Goal
Build a loop that keeps asking for a number until the user provides a valid integer.

## 📝 Features
- `while True` loop
- `try...except ValueError`
- `break` on success
""",
        "questions": [],
        "challenge": {
            "title": "Infinite Number Asker",
            "description": "Write a `while` loop that takes `input()`. If it's a valid integer, print it and `break`. If not, print 'Retry' and continue.",
            "initial_code": "# Loop and ask\n",
            "solution_code": "while True:\n    try:\n        print(int(input()))\n        break\n    except:\n        print('Retry')\n",
            "test_cases": [{"input": "hi\n10", "expected": "Retry\n10"}],
        },
    },

    "les-error-handling-10-intermediate": {
        "title": "Project: File System Guard",
        "content": """# Project: File System Guard

## 🎯 Goal
Write a function `safe_write(filename, data)` that handles every possible file error.

## 📝 Error list
- `PermissionError`
- `FileNotFoundError` (for the path)
- `IsADirectoryError`
""",
        "questions": [],
        "challenge": {
            "title": "File Guard",
            "description": "Read a filename. Try to open it in 'x' mode. If it fails because it exists, print 'Exists'. Catch any other OS errors and print 'Error'.",
            "initial_code": "name = input()\n# try logic\n",
            "solution_code": "name = input()\ntry:\n    f = open(name, 'x')\nexcept FileExistsError:\n    print('Exists')\nexcept OSError:\n    print('Error')\n",
            "test_cases": [{"input": "existing_file", "expected": "Exists"}],
        },
    },

    "les-error-handling-10-pro": {
        "title": "Project: Custom Validation Framework",
        "content": """# Project: Custom Validation Framework

## 🎯 Goal
Build a "User" object that validates its own fields using custom exceptions.

## 📝 Features
- `EmailFormatError`
- `UsernameLengthError`
- A single `Validator.check(user)` method that catches any of these and logs them.
""",
        "questions": [],
        "challenge": {
            "title": "Validator Chain",
            "description": "Define `check_email(s)`. If `@` not in `s`, raise `EmailError`. Call it on 'user.com' inside a try block and catch it.",
            "initial_code": "class EmailError(Exception): pass\n# logic\n",
            "solution_code": "class EmailError(Exception): pass\ndef check_email(s):\n    if '@' not in s: raise EmailError()\ntry:\n    check_email('user.com')\nexcept EmailError:\n    print('Invalid')\n",
            "test_cases": [{"input": "", "expected": "Invalid"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 7 (Error Handling) — Lessons 6-10"

    def handle(self, *args, **options):
        count = 0
        with transaction.atomic():
            for lesson_id, data in LESSONS.items():
                updated = Lesson.objects.filter(id=lesson_id).update(
                    title=data["title"], content=data["content"]
                )
                if not updated:
                    self.stdout.write(self.style.WARNING(f"  ⚠  Not found: {lesson_id}"))
                    continue
                
                # Add Quiz
                quiz, _ = Quiz.objects.get_or_create(
                    id=f"quiz-{lesson_id}",
                    defaults={"lesson_id": lesson_id, "title": f"Quiz: {data['title']}"}
                )
                Question.objects.filter(quiz_id=quiz.id).delete()
                for i, q in enumerate(data["questions"]):
                    Question.objects.create(
                        id=f"q-{lesson_id}-{i+1}",
                        quiz_id=quiz.id,
                        text=q["text"],
                        type="mcq",
                        options=q["options"],
                        points=5
                    )

                # Add Challenge
                ch = data["challenge"]
                Challenge.objects.filter(lesson_id=lesson_id).delete()
                Challenge.objects.create(
                    lesson_id=lesson_id,
                    title=ch["title"],
                    description=ch["description"],
                    initial_code=ch["initial_code"],
                    solution_code=ch["solution_code"],
                    test_cases=ch["test_cases"],
                    points=20
                )
                count += 1
                self.stdout.write(f"  ✅ {lesson_id}")
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 7 (6-10)"))
