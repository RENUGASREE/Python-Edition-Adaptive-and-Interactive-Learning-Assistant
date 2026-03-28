"""
Management command: python manage.py hydrate_module1
Populates Module 1 (Python Basics) lessons with professional content,
quizzes, and coding challenges.
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

# ---------------------------------------------------------------------------
# LESSON CONTENT DATA
# Format: lesson_id -> { title, content, questions: [...], challenge: {...} }
# ---------------------------------------------------------------------------

MODULE_ID = "mod-python-basics"

LESSONS = {
    # ── Lesson 1: Hello World ───────────────────────────────────────────────
    "les-python-basics-1-beginner": {
        "title": "Hello World — Your First Python Program",
        "content": """# Hello World — Your First Python Program

## 🎯 Learning Objectives
- Understand what Python is and why it matters
- Write and run your very first Python program
- Use the `print()` function to display output

## 📚 Concept Overview
Python is a **high-level, interpreted programming language** celebrated for its clean, readable syntax.
Unlike C or Java, you don't need to declare types, write boilerplate, or compile code before running it.
Python runs line-by-line, making it perfect for beginners and experts alike.

### How Python Works
```
Your Code (.py) → Python Interpreter → Output on Screen
```

## 💻 Code Walkthrough
```python
# This is a comment — Python ignores it
print("Hello, World!")   # Calls the built-in print() function
print("My name is Alice")
print(42)                # print() works with numbers too
```
**Expected Output:**
```
Hello, World!
My name is Alice
42
```

## ⚠️ Common Pitfalls
- **Forgetting parentheses**: `print "Hello"` is Python 2 syntax — always write `print("Hello")`
- **Mismatched quotes**: `print("Hello')` causes a `SyntaxError`
- **Indentation errors**: Python is whitespace-sensitive — keep code at the correct indent level

## 🏆 Key Takeaways
- `print()` is the primary output function in Python
- Strings must be wrapped in `"double"` or `'single'` quotes
- Python files use the `.py` extension and run via `python filename.py`
""",
        "questions": [
            {
                "text": "Which function is used to display text on the screen in Python?",
                "options": [
                    {"text": "print()", "correct": True},
                    {"text": "display()", "correct": False},
                    {"text": "echo()", "correct": False},
                    {"text": "show()", "correct": False},
                ],
            },
            {
                "text": "What will `print(\"Hello\")` output?",
                "options": [
                    {"text": "Hello", "correct": True},
                    {"text": '"Hello"', "correct": False},
                    {"text": "hello", "correct": False},
                    {"text": "HELLO", "correct": False},
                ],
            },
            {
                "text": "Which of the following is a valid Python comment?",
                "options": [
                    {"text": "# This is a comment", "correct": True},
                    {"text": "// This is a comment", "correct": False},
                    {"text": "/* comment */", "correct": False},
                    {"text": "-- comment", "correct": False},
                ],
            },
        ],
        "challenge": {
            "title": "Print a Welcome Banner",
            "description": """Print exactly these three lines:
Welcome to Python!
Let's start coding.
Have fun!""",
            "initial_code": "# Write your solution below\n",
            "solution_code": 'print("Welcome to Python!")\nprint("Let\'s start coding.")\nprint("Have fun!")\n',
            "test_cases": [{"input": "", "expected": "Welcome to Python!\nLet's start coding.\nHave fun!"}],
        },
    },

    "les-python-basics-1-intermediate": {
        "title": "Python Execution Model & print() Deep Dive",
        "content": """# Python Execution Model & print() Deep Dive

## 🎯 Learning Objectives
- Understand how the Python interpreter executes code
- Master `print()` with `sep`, `end`, and `file` parameters
- Use f-strings for inline output formatting

## 📚 Concept Overview
Python is an **interpreted language**: the CPython interpreter reads your `.py` file line-by-line,
compiles it internally to **bytecode** (`.pyc`), and executes it on the Python Virtual Machine (PVM).

### print() Full Signature
```python
print(*objects, sep=' ', end='\\n', file=sys.stdout, flush=False)
```
- `sep` — separator between multiple arguments (default: space)
- `end` — what to print at the very end (default: newline `\\n`)
- `flush` — whether to forcibly flush the output buffer

## 💻 Code Walkthrough
```python
# Multiple arguments with custom separator
print("Alice", "Bob", "Carol", sep=" | ")   # Alice | Bob | Carol

# No newline at end — cursor stays on same line
print("Loading", end="")
print("...", end="\\n")   # Loading...

# f-string formatting
name = "Renu"
score = 98
print(f"Student: {name} scored {score}%")   # Student: Renu scored 98%
```

## ⚠️ Common Pitfalls
- Using `+` to join non-strings: `print("Score: " + 98)` raises `TypeError` — use f-strings instead
- Confusing `sep` (between args) with `end` (terminator)

## 🏆 Key Takeaways
- `print()` is far more powerful than it appears — use `sep` and `end` creatively
- f-strings (`f"..."`) are the modern, preferred way to embed variables in strings
- The interpreter compiles Python to bytecode before execution for performance
""",
        "questions": [
            {
                "text": "What does `print('A', 'B', sep='-')` output?",
                "options": [
                    {"text": "A-B", "correct": True},
                    {"text": "A B", "correct": False},
                    {"text": "AB", "correct": False},
                    {"text": "A,B", "correct": False},
                ],
            },
            {
                "text": "Which parameter of print() controls what is printed at the very end?",
                "options": [
                    {"text": "end", "correct": True},
                    {"text": "sep", "correct": False},
                    {"text": "final", "correct": False},
                    {"text": "suffix", "correct": False},
                ],
            },
            {
                "text": "What is an f-string in Python?",
                "options": [
                    {"text": "A string with embedded expressions using {}", "correct": True},
                    {"text": "A string that only contains floats", "correct": False},
                    {"text": "A formatted file string", "correct": False},
                    {"text": "A function-string shortcut", "correct": False},
                ],
            },
        ],
        "challenge": {
            "title": "Custom Table Row",
            "description": "Read three words on separate lines. Print them separated by ' | ' with no trailing newline at the end of the last item.",
            "initial_code": "# Read three words and print them as a table row\n",
            "solution_code": 'a = input()\nb = input()\nc = input()\nprint(a, b, c, sep=" | ")\n',
            "test_cases": [{"input": "Name\nAge\nCity", "expected": "Name | Age | City"}],
        },
    },

    "les-python-basics-1-pro": {
        "title": "Python Internals: Bytecode, GIL & Execution Pipeline",
        "content": """# Python Internals: Bytecode, GIL & Execution Pipeline

## 🎯 Learning Objectives
- Inspect Python bytecode with the `dis` module
- Understand the Global Interpreter Lock (GIL) and its implications
- Compare CPython vs PyPy vs Jython execution models

## 📚 Concept Overview
### The CPython Execution Pipeline
```
Source (.py) → Lexer → Tokens → Parser → AST → Compiler → Bytecode → PVM
```
Each `.py` file is compiled to `.pyc` bytecode cached in `__pycache__`.

### The Global Interpreter Lock (GIL)
CPython's GIL ensures **only one thread executes Python bytecode at a time**.
This simplifies memory management (reference counting) but limits CPU-bound multi-threading.

**Workarounds:**
- CPU-bound: use `multiprocessing` (separate GIL per process)
- I/O-bound: `threading` is fine — GIL released during I/O waits
- Alternative: PyPy (JIT compiler), Jython (runs on JVM — no GIL)

## 💻 Code Walkthrough
```python
import dis

def greet(name):
    return f"Hello, {name}!"

# Disassemble to view bytecode
dis.dis(greet)
# LOAD_FAST 0 (name)
# FORMAT_VALUE ...
# RETURN_VALUE
```

## ⚠️ Common Pitfalls
- Assuming threads speed up CPU-bound Python code (they won't — the GIL prevents it)
- Treating `.pyc` files as source of truth; always edit `.py` files

## 🏆 Key Takeaways
- CPython compiles Python to bytecode before execution — `dis` lets you inspect this
- The GIL is a CPython-specific limit; PyPy and Jython don't have it
- For true parallelism in Python, use `multiprocessing` or `concurrent.futures`
""",
        "questions": [
            {
                "text": "What module can you use to inspect Python bytecode?",
                "options": [
                    {"text": "dis", "correct": True},
                    {"text": "byte", "correct": False},
                    {"text": "inspect", "correct": False},
                    {"text": "compile", "correct": False},
                ],
            },
            {
                "text": "What is the main limitation of the GIL in CPython?",
                "options": [
                    {"text": "Only one thread can execute Python bytecode at a time", "correct": True},
                    {"text": "Python cannot use multiple CPU cores at all", "correct": False},
                    {"text": "Multi-processing is disabled", "correct": False},
                    {"text": "I/O operations block all threads permanently", "correct": False},
                ],
            },
            {
                "text": "Which Python runtime does NOT have a GIL?",
                "options": [
                    {"text": "Jython", "correct": True},
                    {"text": "CPython", "correct": False},
                    {"text": "MicroPython", "correct": False},
                    {"text": "All Python runtimes have a GIL", "correct": False},
                ],
            },
        ],
        "challenge": {
            "title": "Bytecode Inspector",
            "description": "Write a function `add(a, b)` that returns `a + b`. Then use `dis.dis` to print its bytecode. Read an integer N from input and print `add(N, N)`.",
            "initial_code": "import dis\n\n# Define add function and disassemble it\n# Then read N and print add(N, N)\n",
            "solution_code": "import dis\n\ndef add(a, b):\n    return a + b\n\ndis.dis(add)\nn = int(input())\nprint(add(n, n))\n",
            "test_cases": [{"input": "5", "expected": "10"}],
        },
    },

    # ── Lesson 2: Variables ─────────────────────────────────────────────────
    "les-python-basics-2-beginner": {
        "title": "Variables & Assignment",
        "content": """# Variables & Assignment

## 🎯 Learning Objectives
- Create variables and assign values to them
- Understand Python's dynamic typing
- Follow Python naming conventions (PEP 8)

## 📚 Concept Overview
A **variable** is a name that points to a value stored in memory.
Python uses **dynamic typing** — you don't declare a type; Python infers it.

```python
x = 10          # x is an int
x = "hello"     # now x is a str — totally valid in Python!
```

### Naming Rules
- Must start with a letter or `_`
- Can contain letters, digits, `_`
- Case-sensitive: `name ≠ Name ≠ NAME`
- Use `snake_case` for variables (PEP 8 standard)

## 💻 Code Walkthrough
```python
# Assign values
first_name = "Alice"
age = 21
height = 5.6
is_student = True

# Multiple assignment
x, y, z = 1, 2, 3

# Swap without temp variable
a, b = 10, 20
a, b = b, a
print(a, b)  # 20 10
```

## ⚠️ Common Pitfalls
- `2name = "Bob"` is invalid — variable names can't start with digits
- Using reserved words: `class = 5` will cause `SyntaxError`

## 🏆 Key Takeaways
- Python variables are labels that point to objects, not boxes that hold values
- Dynamic typing means you can reassign a variable to a different type
- Follow `snake_case` naming for readability
""",
        "questions": [
            {
                "text": "Which variable name follows Python's snake_case convention?",
                "options": [
                    {"text": "user_name", "correct": True},
                    {"text": "UserName", "correct": False},
                    {"text": "username2nd", "correct": False},
                    {"text": "2user_name", "correct": False},
                ],
            },
            {
                "text": "What does `x, y = y, x` do in Python?",
                "options": [
                    {"text": "Swaps the values of x and y", "correct": True},
                    {"text": "Creates two new variables", "correct": False},
                    {"text": "Raises a SyntaxError", "correct": False},
                    {"text": "Copies x into y only", "correct": False},
                ],
            },
            {
                "text": "What type will Python assign to `score = 95.5`?",
                "options": [
                    {"text": "float", "correct": True},
                    {"text": "int", "correct": False},
                    {"text": "double", "correct": False},
                    {"text": "decimal", "correct": False},
                ],
            },
        ],
        "challenge": {
            "title": "Swap and Print",
            "description": "Read two integers, one per line. Swap their values and print the swapped result on one line separated by a space.",
            "initial_code": "# Read two integers, swap them, and print\n",
            "solution_code": "a = int(input())\nb = int(input())\na, b = b, a\nprint(a, b)\n",
            "test_cases": [
                {"input": "10\n20", "expected": "20 10"},
                {"input": "5\n99", "expected": "99 5"},
            ],
        },
    },

    "les-python-basics-2-intermediate": {
        "title": "Variable Scope, References & Memory",
        "content": """# Variable Scope, References & Memory

## 🎯 Learning Objectives
- Understand how Python stores objects in memory
- Distinguish between mutable and immutable objects
- Grasp LEGB scope rules

## 📚 Concept Overview
In Python, variables are **references** (pointers) to objects on the heap.

```python
a = [1, 2, 3]
b = a            # b points to the SAME list!
b.append(4)
print(a)         # [1, 2, 3, 4]  ← a also changed!
```
This is called **aliasing**. For a true copy: `b = a.copy()` or `b = a[:]`.

### LEGB Scope Resolution
Python looks up names in this order:
1. **L**ocal — inside the current function
2. **E**nclosing — outer function (closures)
3. **G**lobal — module level
4. **B**uilt-in — e.g., `print`, `len`

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        print(x)   # → "enclosing" (E before G)
    inner()
outer()
```

## 💻 Code Walkthrough
```python
import sys

x = 42
y = 42
print(x is y)        # True — Python caches small ints (-5 to 256)
print(sys.getrefcount(x))  # reference count

# Mutable vs immutable
s = "hello"
# s[0] = "H"  ← TypeError: strings are immutable
lst = [1, 2]
lst[0] = 9   # ✓ lists are mutable
```

## ⚠️ Common Pitfalls
- Treating `is` and `==` as the same: `is` checks identity, `==` checks equality
- Accidentally mutating a shared list via aliasing

## 🏆 Key Takeaways
- Variables are references; assignment binds a name to an object
- Immutable objects (int, str, tuple) cannot be changed in place
- LEGB defines the order Python searches for variable names
""",
        "questions": [
            {
                "text": "What does `b = a` do when `a` is a list?",
                "options": [
                    {"text": "Both a and b point to the same list object", "correct": True},
                    {"text": "Creates a separate copy of the list", "correct": False},
                    {"text": "Raises a TypeError", "correct": False},
                    {"text": "Freezes the list", "correct": False},
                ],
            },
            {
                "text": "What is the LEGB rule in Python?",
                "options": [
                    {"text": "The order Python searches for variable names: Local, Enclosing, Global, Built-in", "correct": True},
                    {"text": "A memory allocation strategy", "correct": False},
                    {"text": "A list comprehension syntax rule", "correct": False},
                    {"text": "A loop execution order", "correct": False},
                ],
            },
            {
                "text": "Which of the following is immutable in Python?",
                "options": [
                    {"text": "tuple", "correct": True},
                    {"text": "list", "correct": False},
                    {"text": "dict", "correct": False},
                    {"text": "set", "correct": False},
                ],
            },
        ],
        "challenge": {
            "title": "Aliasing Detector",
            "description": "Read a number N. Create list `a = [N, N*2, N*3]`. Create `b = a.copy()`. Append N*4 to b. Print a on one line and b on another.",
            "initial_code": "# Read N, create a, copy to b, append to b, print both\n",
            "solution_code": "n = int(input())\na = [n, n*2, n*3]\nb = a.copy()\nb.append(n*4)\nprint(a)\nprint(b)\n",
            "test_cases": [{"input": "2", "expected": "[2, 4, 6]\n[2, 4, 6, 8]"}],
        },
    },

    "les-python-basics-2-pro": {
        "title": "Dynamic Typing, Type Interning & Descriptors",
        "content": """# Dynamic Typing, Type Interning & Descriptors

## 🎯 Learning Objectives
- Understand CPython's type system and `__class__` internals
- Explore string and integer interning
- Use descriptors to control attribute access

## 📚 Concept Overview
Python objects carry their type with them at runtime via `ob_type` in the C struct.
This is what makes Python dynamically typed — the type lives in the object, not the variable.

### String Interning
CPython interns short strings that look like identifiers:
```python
a = "hello"
b = "hello"
print(a is b)   # True — same interned object

a = "hello world"  # has a space
b = "hello world"
print(a is b)   # False — NOT guaranteed to intern
```
Force interning: `sys.intern(string)`

### Descriptors (Advanced)
Descriptors are objects implementing `__get__`, `__set__`, `__delete__`.
They power Python's property system, slots, and ORM fields.

```python
class Validator:
    def __set_name__(self, owner, name):
        self.name = name
    def __get__(self, obj, objtype=None):
        return obj.__dict__.get(self.name)
    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError(f"{self.name} must be int")
        obj.__dict__[self.name] = value

class Player:
    score = Validator()

p = Player()
p.score = 100   # OK
p.score = "a"   # TypeError
```

## 🏆 Key Takeaways
- Types in Python are first-class objects; everything has `__class__`
- CPython interns short identifier-like strings for memory efficiency
- Descriptors are the mechanism behind `@property`, `classmethod`, Django fields
""",
        "questions": [
            {
                "text": "Which function forces string interning in Python?",
                "options": [
                    {"text": "sys.intern()", "correct": True},
                    {"text": "str.intern()", "correct": False},
                    {"text": "intern()", "correct": False},
                    {"text": "cache()", "correct": False},
                ],
            },
            {
                "text": "What method must a descriptor implement to support attribute reads?",
                "options": [
                    {"text": "__get__", "correct": True},
                    {"text": "__read__", "correct": False},
                    {"text": "__access__", "correct": False},
                    {"text": "__fetch__", "correct": False},
                ],
            },
            {
                "text": "Why does CPython intern short strings?",
                "options": [
                    {"text": "To save memory and speed up equality checks", "correct": True},
                    {"text": "To make them immutable", "correct": False},
                    {"text": "To prevent garbage collection", "correct": False},
                    {"text": "To enable multi-threading", "correct": False},
                ],
            },
        ],
        "challenge": {
            "title": "Type-Safe Attribute",
            "description": "Read an integer score from input. Create a Player with a `score` descriptor that only accepts integers. Print the score. If input is not an integer, print 'TypeError'.",
            "initial_code": "# Implement a descriptor-based Player class\n",
            "solution_code": "class Validator:\n    def __set_name__(self, owner, name):\n        self.name = name\n    def __get__(self, obj, objtype=None):\n        if obj is None: return self\n        return obj.__dict__.get(self.name)\n    def __set__(self, obj, value):\n        if not isinstance(value, int):\n            raise TypeError\n        obj.__dict__[self.name] = value\n\nclass Player:\n    score = Validator()\n\ntry:\n    val = int(input())\n    p = Player()\n    p.score = val\n    print(p.score)\nexcept (TypeError, ValueError):\n    print('TypeError')\n",
            "test_cases": [{"input": "100", "expected": "100"}, {"input": "50", "expected": "50"}],
        },
    },
}


class Command(BaseCommand):
    help = "Hydrate Module 1 (Python Basics) lessons with professional content"

    def handle(self, *args, **options):
        count = 0
        with transaction.atomic():
            for lesson_id, data in LESSONS.items():
                # Update lesson title and content
                updated = Lesson.objects.filter(id=lesson_id).update(
                    title=data["title"],
                    content=data["content"],
                )
                if not updated:
                    self.stdout.write(self.style.WARNING(f"  ⚠  Lesson not found: {lesson_id}"))
                    continue

                # Create/update quiz
                quiz, _ = Quiz.objects.get_or_create(
                    id=f"quiz-{lesson_id}",
                    defaults={"lesson_id": lesson_id, "title": f"Quiz: {data['title']}"},
                )

                # Create questions
                Question.objects.filter(quiz_id=quiz.id).delete()
                for i, q in enumerate(data["questions"]):
                    Question.objects.create(
                        id=f"q-{lesson_id}-{i+1}",
                        quiz_id=quiz.id,
                        text=q["text"],
                        type="mcq",
                        options=q["options"],
                        points=5,
                    )

                # Create challenge
                ch = data["challenge"]
                Challenge.objects.filter(lesson_id=lesson_id).delete()
                Challenge.objects.create(
                    lesson_id=lesson_id,
                    title=ch["title"],
                    description=ch["description"],
                    initial_code=ch["initial_code"],
                    solution_code=ch["solution_code"],
                    test_cases=ch["test_cases"],
                    points=20,
                )
                count += 1
                self.stdout.write(f"  ✅ {lesson_id}")

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 1"))
