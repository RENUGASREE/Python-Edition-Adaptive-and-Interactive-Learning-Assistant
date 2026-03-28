"""python manage.py hydrate_module7 -- Module 7 Error Handling Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: Introduction to Exceptions ─────────────────────────────────
    "les-error-handling-1-beginner": {
        "title": "Try & Except Basics",
        "content": """# Try & Except Basics

## 🎯 Learning Objectives
- Understand why programs "crash"
- Use the `try...except` block to catch runtime errors
- Prevent app crashes caused by bad user input

## 📚 Concept Overview
An **Exception** is an error that happens while the program is running. For example, dividing by zero or trying to open a file that doesn't exist.

```python
try:
    num = int(input("Enter a number: "))
    result = 10 / num
    print(result)
except:
    print("Oops! Something went wrong.")
```

## ⚠️ Common Pitfalls
- **Bare Except**: Catching *everything* with just `except:` is generally bad practice because it hides bugs you didn't expect (like typos). Always try to be specific.

## 🏆 Key Takeaways
- Use `try` for code that "might fail".
- Use `except` to handle the failure gracefully.
""",
        "questions": [
            {"text": "Which keyword is used to start a block that might raise an error?", "options": [
                {"text": "try", "correct": True}, {"text": "attempt", "correct": False},
                {"text": "check", "correct": False}, {"text": "error", "correct": False}]},
            {"text": "What does a 'bare except' (except:) do?", "options": [
                {"text": "Catches every possible exception", "correct": True},
                {"text": "Catches only syntax errors", "correct": False},
                {"text": "Does nothing", "correct": False},
                {"text": "Restarts the computer", "correct": False}]},
        ],
        "challenge": {
            "title": "Safe Divider",
            "description": "Read two numbers and divide them. Use `try...except` to print 'Error' if the user enters 0 as the second number.",
            "initial_code": "a = int(input())\nb = int(input())\n# Divide safely\n",
            "solution_code": "try:\n    print(a / b)\nexcept:\n    print('Error')\n",
            "test_cases": [{"input": "10\n0", "expected": "Error"}, {"input": "10\n2", "expected": "5.0"}],
        },
    },

    "les-error-handling-1-intermediate": {
        "title": "Specific Exception Types",
        "content": """# Specific Exception Types

## 🎯 Learning Objectives
- Catch specific errors like `ValueError` and `ZeroDivisionError`
- Provide different feedback for different errors
- Understand the Exception Hierarchy

## 📚 Concept Overview
Python has many built-in error types. Being specific makes your code more robust and helpful.

```python
try:
    x = int("abc")
except ValueError:
    print("That was not a valid integer!")
except ZeroDivisionError:
    print("You cannot divide by zero!")
```

## 🏆 Key Takeaways
- Common types: `ValueError`, `TypeError`, `IndexError`, `KeyError`.
- Catching specific exceptions prevents "hiding" unrelated system bugs.
""",
        "questions": [
            {"text": "Which exception is raised when you try to access a list index that doesn't exist?", "options": [
                {"text": "IndexError", "correct": True}, {"text": "ValueError", "correct": False},
                {"text": "KeyError", "correct": False}, {"text": "TypeError", "correct": False}]},
        ],
        "challenge": {
            "title": "Multi-Error Handler",
            "description": "Read a string. Try to convert it to `int` and calculate `100 / value`. Catch `ValueError` to print 'Bad Input' and `ZeroDivisionError` to print 'No Zero'.",
            "initial_code": "s = input()\n# Handle two types\n",
            "solution_code": "try:\n    val = int(s)\n    print(100 / val)\nexcept ValueError:\n    print('Bad Input')\nexcept ZeroDivisionError:\n    print('No Zero')\n",
            "test_cases": [{"input": "abc", "expected": "Bad Input"}, {"input": "0", "expected": "No Zero"}],
        },
    },

    "les-error-handling-1-pro": {
        "title": "Exception Aliasing & Inspection",
        "content": """# Exception Aliasing & Inspection

## 🎯 Learning Objectives
- Use the `as` keyword to inspect the error object
- Access the error message dynamically
- Log detailed error information

## 📚 Concept Overview
When an error happens, Python creates an "Error Object" that contains details.

```python
try:
    1 / 0
except ZeroDivisionError as e:
    print(f"Log: An error occurred -> {e}")
```

## 🏆 Key Takeaways
- The variable `e` (or any name) contains the human-readable error string.
- This is useful for writing errors to log files or showing them to developers.
""",
        "questions": [
            {"text": "How do you 'capture' the exception object into a variable?", "options": [
                {"text": "except ValueError as e:", "correct": True}, {"text": "except ValueError = e:", "correct": False},
                {"text": "catch e from ValueError:", "correct": False}, {"text": "e = ValueError", "correct": False}]},
        ],
        "challenge": {
            "title": "Error Message Printer",
            "description": "Trigger an error (any type) and print the exception object using the `as` keyword.",
            "initial_code": "# code here\n",
            "solution_code": "try:\n    print(1/0)\nexcept Exception as error:\n    print(error)\n",
            "test_cases": [{"input": "", "expected": "division by zero"}],
        },
    },

    # ── Lesson 2: Multiple Exceptions & Base Exception ───────────────────────
    "les-error-handling-2-beginner": {
        "title": "Grouping Exceptions",
        "content": """# Grouping Exceptions

## 🎯 Learning Objectives
- Handle multiple error types in a single block
- Use tuples for concise exception handling
- Reduce code duplication

## 📚 Concept Overview
If you want to do the same thing for two different errors, you can group them.

```python
try:
    # logic ...
except (ValueError, TypeError):
    print("Data type error!")
```

## 🏆 Key Takeaways
- Use a tuple `(Error1, Error2)` if the recovery logic is the same for both.
""",
        "questions": [
            {"text": "What is the correct syntax to catch both ValueError and IndexError in one line?", "options": [
                {"text": "except (ValueError, IndexError):", "correct": True},
                {"text": "except ValueError or IndexError:", "correct": False},
                {"text": "except [ValueError, IndexError]:", "correct": False},
                {"text": "except ValueError, IndexError:", "correct": False}]},
        ],
        "challenge": {
            "title": "Grouped Handler",
            "description": "Write a `try` block that catches both `KeyError` AND `IndexError` in a single line and prints 'Lookup Failed'.",
            "initial_code": "# Group them\n",
            "solution_code": "try:\n    # do something\n    pass\nexcept (KeyError, IndexError):\n    print('Lookup Failed')\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-error-handling-2-intermediate": {
        "title": "The Exception Hierarchy",
        "content": """# The Exception Hierarchy

## 🎯 Learning Objectives
- Understand that exceptions are classes
- Learn about the `Exception` base class
- Know why `BaseException` is different from `Exception`

## 📚 Concept Overview
Exceptions follow a family tree. `Exception` is the parent of almost everything (`ValueError`, `RuntimeError`, etc.).
`BaseException` is the grand-parent (including things like `KeyboardInterrupt` which you usually shouldn't catch).

```python
try:
    # ...
except Exception: # Catches almost all errors
    print("Something happened")
```

## ⚠️ Common Pitfalls
- Catching `Exception` too early in your list of `except` blocks. Specific errors must come first!

## 🏆 Key Takeaways
- `Exception` is the general safety net.
- `BaseException` is for system-level signals.
""",
        "questions": [
            {"text": "Which class is the parent of most common built-in exceptions?", "options": [
                {"text": "Exception", "correct": True}, {"text": "BaseException", "correct": False},
                {"text": "Error", "correct": False}, {"text": "RuntimeObject", "correct": False}]},
        ],
        "challenge": {
            "title": "Catch All",
            "description": "Read input. If it is 'crash', raise a `RuntimeError`. Catch it using the generic `Exception` class and print 'Caught'.",
            "initial_code": "s = input()\n# Logic here\n",
            "solution_code": "try:\n    if s == 'crash': raise RuntimeError()\nexcept Exception:\n    print('Caught')\n",
            "test_cases": [{"input": "crash", "expected": "Caught"}],
        },
    },

    "les-error-handling-2-pro": {
        "title": "StopIteration & Control Exceptions",
        "content": """# StopIteration & Control Exceptions

## 🎯 Learning Objectives
- Understand exceptions that aren't actually "errors"
- Use exceptions for control flow (StopIteration, GeneratorExit)
- Learn how `for` loops work under the hood

## 📚 Concept Overview
Python occasionally uses exceptions to signal the end of a process. In a `for` loop, the iterator raises `StopIteration` when it's out of items.

## 🏆 Key Takeaways
- Not every exception means something went wrong. Some are just signals.
""",
        "questions": [
            {"text": "Which exception is used by iterators to signal that there are no more items?", "options": [
                {"text": "StopIteration", "correct": True}, {"text": "EndList", "correct": False},
                {"text": "EOFError", "correct": False}, {"text": "FinishSignal", "correct": False}]},
        ],
        "challenge": {
            "title": "Manual Iterator",
            "description": "Take `it = iter([1])`. Call `next(it)` twice. Use `try...except` to catch the error when it runs out and print 'DONE'.",
            "initial_code": "it = iter([1])\n# calls and catch\n",
            "solution_code": "it = iter([1])\ntry:\n    next(it)\n    next(it)\nexcept StopIteration:\n    print('DONE')\n",
            "test_cases": [{"input": "", "expected": "DONE"}],
        },
    },

    # ── Lesson 3: Else & Finally ─────────────────────────────────────────────
    "les-error-handling-3-beginner": {
        "title": "The Finally Clause",
        "content": """# The Finally Clause

## 🎯 Learning Objectives
- Use `finally` for guaranteed cleanup
- Understand that `finally` runs NO MATTER WHAT
- Clean up resources (close files, sockets) reliably

## 📚 Concept Overview
```python
try:
    f = open("data.txt")
    # ... read ...
except:
    print("Error")
finally:
    f.close() # THIS ALWAYS RUNS
    print("File closed.")
```

## 🏆 Key Takeaways
- `finally` is the "janitor" of your code.
- If you don't use a `with` statement, `finally` is the standard way to close resources.
""",
        "questions": [
            {"text": "When does the `finally` block execute?", "options": [
                {"text": "Always, whether or not an exception occurred", "correct": True},
                {"text": "Only if an error occurred", "correct": False},
                {"text": "Only if NO error occurred", "correct": False},
                {"text": "Only if 'try' was successful", "correct": False}]},
        ],
        "challenge": {
            "title": "Cleanup Master",
            "description": "Print 'Start', 'Work', 'End'. Put 'End' in a `finally` block and the others in `try`. Trigger an error in `try`.",
            "initial_code": "# finally demo\n",
            "solution_code": "try:\n    print('Start')\n    print('Work')\n    print(1/0)\nexcept:\n    pass\nfinally:\n    print('End')\n",
            "test_cases": [{"input": "", "expected": "Start\nWork\nEnd"}],
        },
    },

    "les-error-handling-3-intermediate": {
        "title": "The Else Clause",
        "content": """# The Else Clause

## 🎯 Learning Objectives
- Use `else` for code that should only run if the `try` was successful
- Distinguish between "Try logic" and "Follow-up logic"
- Keep the `try` block minimal

## 📚 Concept Overview
```python
try:
    val = int(input())
except ValueError:
    print("Not an int")
else:
    # RUNS ONLY IF NO EXCEPTION
    print(f"Success! {val}")
```

## 🏆 Key Takeaways
- `else` is for code that should **not** be inside the `try` (to avoid catching unintended errors) but depends on the success of the `try`.
""",
        "questions": [
            {"text": "What is the condition for the `else` block to run?", "options": [
                {"text": "The try block finished without errors", "correct": True},
                {"text": "The except block finished", "correct": False},
                {"text": "The try block failed", "correct": False},
                {"text": "Finally was not called", "correct": False}]},
        ],
        "challenge": {
            "title": "Else Success",
            "description": "Read a number. If conversion to `int` works, print 'OK'. Use the `else` block.",
            "initial_code": "s = input()\n# use try/except/else\n",
            "solution_code": "try:\n    n = int(s)\nexcept:\n    pass\nelse:\n    print('OK')\n",
            "test_cases": [{"input": "5", "expected": "OK"}, {"input": "hi", "expected": ""}],
        },
    },

    "les-error-handling-3-pro": {
        "title": "Combining Try/Except/Else/Finally",
        "content": """# Combining Try/Except/Else/Finally

## 🎯 Learning Objectives
- Use the full suite of exception tools together
- Understand the exact order of execution
- Build mission-critical logic flows

## 📚 Concept Overview
1. `try`: Run main work.
2. `except`: If work failed, do this.
3. `else`: If work worked, do this extra thing.
4. `finally`: Cleanup always.

## 🏆 Key Takeaways
- This complete pattern provides maximum control over your program's flow.
""",
        "questions": [
            {"text": "What is the correct order of blocks?", "options": [
                {"text": "try, except, else, finally", "correct": True},
                {"text": "try, else, except, finally", "correct": False},
                {"text": "try, finally, except, else", "correct": False},
                {"text": "except, try, finally, else", "correct": False}]},
        ],
        "challenge": {
            "title": "Full Cycle",
            "description": "Write a snippet that prints 'A' at start of try, 'B' if successful (else), and 'C' at end (finally).",
            "initial_code": "# Combined blocks\n",
            "solution_code": "try:\n    print('A')\nexcept:\n    pass\nelse:\n    print('B')\nfinally:\n    print('C')\n",
            "test_cases": [{"input": "", "expected": "A\nB\nC"}],
        },
    },

    # ── Lesson 4: Raising Exceptions ──────────────────────────────────────────
    "les-error-handling-4-beginner": {
        "title": "Raising Exceptions",
        "content": """# Raising Exceptions

## 🎯 Learning Objectives
- Trigger errors manually using `raise`
- Enforce business rules (e.g., age must be > 0)
- Stop program execution when invalid state is reached

## 📚 Concept Overview
```python
age = -5
if age < 0:
    raise ValueError("Age cannot be negative!")
```

## 🏆 Key Takeaways
- Use `raise` when **your** code detects that something is wrong.
""",
        "questions": [
            {"text": "Which keyword is used to trigger an exception manually?", "options": [
                {"text": "raise", "correct": True}, {"text": "throw", "correct": False},
                {"text": "trigger", "correct": False}, {"text": "fail", "correct": False}]},
        ],
        "challenge": {
            "title": "Rule Enforcer",
            "description": "Read a string. If it is empty, raise `ValueError('Required')`.",
            "initial_code": "s = input()\n# check and raise\n",
            "solution_code": "s = input()\nif not s: raise ValueError('Required')\n",
            "test_cases": [{"input": "", "expected": "ValueError: Required"}],
        },
    },

    "les-error-handling-4-intermediate": {
        "title": "Re-raising Exceptions",
        "content": """# Re-raising Exceptions

## 🎯 Learning Objectives
- Log an error and then let it continue to crash or be handled elsewhere
- Use a "naked" `raise`
- Understand local vs global error handling

## 📚 Concept Overview
```python
try:
    # some work
except Exception as e:
    print(f"I logged {e}")
    raise # Passes the EXACT same error up to the caller
```

## 🏆 Key Takeaways
- `raise` without any arguments inside an `except` block re-raises the active exception.
""",
        "questions": [
            {"text": "What does a `raise` keyword without an exception name do inside an `except` block?", "options": [
                {"text": "Passes the current exception to the outer scope", "correct": True},
                {"text": "Ends the program immediately", "correct": False},
                {"text": "Clears the error", "correct": False},
                {"text": "Restarts the try block", "correct": False}]},
        ],
        "challenge": {
            "title": "Silent Logger",
            "description": "Write an `except` that prints 'Error' and then re-raises the original exception.",
            "initial_code": "try:\n    1/0\nexcept:\n    # log and reraise\n",
            "solution_code": "try:\n    1/0\nexcept:\n    print('Error')\n    raise\n",
            "test_cases": [{"input": "", "expected": "*Error*"}],
        },
    },

    "les-error-handling-4-pro": {
        "title": "Exception Chaining (from)",
        "content": """# Exception Chaining (from)

## 🎯 Learning Objectives
- Link one exception to another
- Use the `from` keyword
- Maintain the "Cause" of an error for debugging

## 📚 Concept Overview
Sometimes a database error causes a web error. You want to show BOTH.

```python
try:
    # database code
except DBError as e:
    raise AppError("App failed") from e
```

## 🏆 Key Takeaways
- Chaining creates a "The above exception was the direct cause of..." message in the console.
""",
        "questions": [
            {"text": "Which keyword links a new exception to a previous one in a chain?", "options": [
                {"text": "from", "correct": True}, {"text": "with", "correct": False},
                {"text": "using", "correct": False}, {"text": "caused_by", "correct": False}]},
        ],
        "challenge": {
            "title": "Chain Linker",
            "description": "Catch any error `e` and raise a new `RuntimeError('Ops')` from it.",
            "initial_code": "try:\n    1/0\nexcept Exception as e:\n    # Chain it\n",
            "solution_code": "try:\n    1/0\nexcept Exception as e:\n    raise RuntimeError('Ops') from e\n",
            "test_cases": [{"input": "", "expected": "*direct cause*"}],
        },
    },

    # ── Lesson 5: Assertions ──────────────────────────────────────────────────
    "les-error-handling-5-beginner": {
        "title": "Using Assert",
        "content": """# Using Assert

## 🎯 Learning Objectives
- Use `assert` for internal sanity checks
- Understand the syntax `assert condition, message`
- Learn when to use `assert` vs `if/raise`

## 📚 Concept Overview
An **Assertion** is a check that MUST be True. If it's False, Python crashes immediately with an `AssertionError`.

```python
def calc_pay(salary):
    assert salary > 0, "Salary must be positive!"
    return salary / 12
```

## ⚠️ Common Pitfalls
- **Security Check**: Never use `assert` for security (like password checking), because assertions can be DISABLED in optimized mode!

## 🏆 Key Takeaways
- `assert` is for "This should never happen" scenarios.
- For user input, use `if/raise`.
""",
        "questions": [
            {"text": "When is an AssertionError raised?", "options": [
                {"text": "When the assertion condition is False", "correct": True},
                {"text": "When the assertion condition is True", "correct": False},
                {"text": "Only when the program finishes", "correct": False},
                {"text": "Never, it just prints a warning", "correct": False}]},
            {"text": "What is the primary purpose of assertions?", "options": [
                {"text": "Debugging and internal sanity checks", "correct": True},
                {"text": "Handling user input errors", "correct": False},
                {"text": "Making the code faster", "correct": False},
                {"text": "Database connectivity", "correct": False}]},
        ],
        "challenge": {
            "title": "Positive Asserter",
            "description": "Define a function `verify(n)` that asserts `n > 0` with message 'Invalid'. Test it with 5.",
            "initial_code": "def verify(n):\n    # assert here\n",
            "solution_code": "def verify(n):\n    assert n > 0, 'Invalid'\nverify(5)\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-error-handling-5-intermediate": {
        "title": "Assertions in Testing",
        "content": """# Assertions in Testing

## 🎯 Learning Objectives
- Use assertions to build simple test suites
- Understand the role of `assert` in `pytest` and `unittest`
- Compare expected vs actual results

## 📚 Concept Overview
```python
def add(a, b): return a + b

# Basic testing
assert add(2, 2) == 4
assert add(-1, 1) == 0
```

## 🏆 Key Takeaways
- Standard Python unit test frameworks rely heavily on assertions to verify code behavior.
""",
        "questions": [
            {"text": "True or False: Assertions are the foundation of most Python testing frameworks.", "options": [
                {"text": "True", "correct": True}, {"text": "False", "correct": False}]},
        ],
        "challenge": {
            "title": "Square Tester",
            "description": "Write a function `sq(x): return x*x`. Then write an assertion that verifies `sq(4)` is 16.",
            "initial_code": "def sq(x): return x*x\n# Test it\n",
            "solution_code": "def sq(x): return x*x\nassert sq(4) == 16\n",
            "test_cases": [{"input": "", "expected": ""}],
        },
    },

    "les-error-handling-5-pro": {
        "title": "Optimized Mode (-O)",
        "content": """# Optimized Mode (-O)

## 🎯 Learning Objectives
- Understand the `-O` flag in Python
- Learn that assertions disappear in production
- Discuss the performance impact of assertions

## 📚 Concept Overview
If you run `python -O script.py`, all `assert` statements are **removed** before the code starts.
This is why you don't use them for things that MUST happen (like checking if a user is logged in).

## 🏆 Key Takeaways
- Assertions are for development and debugging.
- Use proper exception handling for production system states.
""",
        "questions": [
            {"text": "What happens to `assert` statements if you run Python with the `-O` (optimize) flag?", "options": [
                {"text": "They are ignored (removed)", "correct": True},
                {"text": "They become faster", "correct": False},
                {"text": "They always raise errors", "correct": False},
                {"text": "They are logged to a file", "correct": False}]},
        ],
        "challenge": {
            "title": "Flags Trivia",
            "description": "Which CLI flag tells the Python interpreter to ignore assertions? Print it (one letter, lowercase, with the dash).",
            "initial_code": "# code\n",
            "solution_code": "print('-o')\n",
            "test_cases": [{"input": "", "expected": "-o"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 7 (Error Handling) — Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 7 (1-5)"))
