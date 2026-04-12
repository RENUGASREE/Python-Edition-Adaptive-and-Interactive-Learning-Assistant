"""python manage.py hydrate_module1_b -- Lessons 6-10 for Python Basics"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    "m1-8-comments-style-beginner-beginner": {
        "title": "Comments & Code Style (PEP 8)",
        "content": """# Comments & Code Style (PEP 8)

## 🎯 Learning Objectives
- Write single-line and multi-line comments
- Understand PEP 8: Python's official style guide
- Use docstrings to document functions

## 📚 Concept Overview
Clean, readable code is the foundation of good Python programming. PEP 8 is the agreed-upon style guide.

### Comments
```python
# Single line comment

# Use triple quotes as multi-line comments:
# Line one
# Line two
# Line three

def greet(name):
    'Return a greeting for the given name.'  # simple docstring
    return f"Hello, {name}!"
```

### Key PEP 8 Rules
| Rule | Good | Bad |
|------|------|-----|
| Indentation | 4 spaces | tabs or 2 spaces |
| Max line length | 79 chars | 120+ chars |
| Blank lines | 2 between functions | 0 or 5 |
| Variable names | `user_age` | `userAge`, `ua` |
| Constants | `MAX_SIZE = 100` | `maxSize` |

## ⚠️ Common Pitfalls
- Over-commenting obvious code: `x = x + 1  # adds 1 to x` — unnecessary
- Under-commenting complex logic — comment the WHY, not the WHAT

## 🏆 Key Takeaways
- Comments explain intent; good code explains itself
- Docstrings are accessible via `help()` — they are documentation
- Follow PEP 8: tools like `flake8` and `black` enforce it automatically
""",
        "questions": [
            {"text": "What character starts a single-line comment in Python?", "options": [
                {"text": "#", "correct": True}, {"text": "//", "correct": False},
                {"text": "--", "correct": False}, {"text": "/*", "correct": False}]},
            {"text": "How many spaces does PEP 8 recommend for indentation?", "options": [
                {"text": "4", "correct": True}, {"text": "2", "correct": False},
                {"text": "8", "correct": False}, {"text": "tab", "correct": False}]},
            {"text": "What is a docstring?", "options": [
                {"text": "A string literal at the start of a function that documents it", "correct": True},
                {"text": "A string used for printing", "correct": False},
                {"text": "A comment inside a loop", "correct": False},
                {"text": "A special variable type", "correct": False}]},
        ],
        "challenge": {
            "title": "PEP 8 Fixer",
            "description": "Read two numbers on separate lines. Print their sum. Your code must use snake_case variables and follow PEP 8.",
            "initial_code": "# Read two numbers and print their sum (use PEP 8 style)\n",
            "solution_code": "first_number = int(input())\nsecond_number = int(input())\nprint(first_number + second_number)\n",
            "test_cases": [{"input": "5\n7", "expected": "12"}, {"input": "100\n200", "expected": "300"}],
        },
    },

    "m1-8-comments-style-intermediate-intermediate": {
        "title": "Type Hints, Annotations & linting Tools",
        "content": """# Type Hints, Annotations & Linting Tools

## 🎯 Learning Objectives
- Add type hints to functions and variables
- Use `mypy` for static type checking
- Automate style enforcement with `black` and `flake8`

## 📚 Concept Overview
### Type Hints (PEP 484, 526)
```python
def add(a: int, b: int) -> int:
    return a + b

name: str = "Alice"
scores: list[int] = [90, 85, 78]

from typing import Optional
def find(name: str) -> Optional[str]:
    return name if name else None
```
Type hints don't enforce types at runtime — they're for static tools and documentation.

### Linting Tools
| Tool | Purpose |
|------|---------|
| `flake8` | Style & error checker (PEP 8) |
| `black` | Auto-formatter |
| `mypy` | Static type checker |
| `pylint` | Comprehensive linter |

```bash
# Install and run
pip install black flake8
black my_file.py        # auto-format
flake8 my_file.py       # check style errors
```

## 🏆 Key Takeaways
- Type hints make code self-documenting and catch bugs before runtime
- `black` enforces a consistent style automatically — no debates about formatting
- Type hints are completely optional but highly recommended for larger projects
""",
        "questions": [
            {"text": "What does `def greet(name: str) -> str:` indicate?", "options": [
                {"text": "name should be a str; the function returns a str", "correct": True},
                {"text": "Forces name to be a string at runtime", "correct": False},
                {"text": "Creates a new string type", "correct": False},
                {"text": "Is invalid Python syntax", "correct": False}]},
            {"text": "Which tool auto-formats Python code to follow PEP 8?", "options": [
                {"text": "black", "correct": True}, {"text": "mypy", "correct": False},
                {"text": "flake8", "correct": False}, {"text": "pylint", "correct": False}]},
            {"text": "Which typing hint represents an optional value (could be None)?", "options": [
                {"text": "Optional[str]", "correct": True}, {"text": "Nullable[str]", "correct": False},
                {"text": "Maybe[str]", "correct": False}, {"text": "str | Required", "correct": False}]},
        ],
        "challenge": {
            "title": "Typed Calculator",
            "description": "Write an `add(a: int, b: int) -> int` function. Read two integers and print their sum using this function.",
            "initial_code": "# Write typed add function and use it\n",
            "solution_code": "def add(a: int, b: int) -> int:\n    return a + b\n\na = int(input())\nb = int(input())\nprint(add(a, b))\n",
            "test_cases": [{"input": "3\n4", "expected": "7"}, {"input": "10\n90", "expected": "100"}],
        },
    },

    "m1-8-comments-style-pro-pro": {
        "title": "AST Inspection, Code Generation & Metaprogramming",
        "content": """# AST Inspection, Code Generation & Metaprogramming

## 🎯 Learning Objectives
- Inspect and modify Python's Abstract Syntax Tree (AST)
- Use `ast.parse` and `ast.NodeVisitor`
- Understand how decorators and metaclasses work as metaprogramming tools

## 📚 Concept Overview
### Abstract Syntax Tree
```python
import ast

code = "x = 1 + 2"
tree = ast.parse(code)
print(ast.dump(tree, indent=2))
```

### Custom AST Visitor
```python
class NameFinder(ast.NodeVisitor):
    def visit_Name(self, node):
        print(f"Found name: {node.id}")
        self.generic_visit(node)

tree = ast.parse("x = y + z")
NameFinder().visit(tree)
# Found name: y
# Found name: z
```

### Decorator as Metaprogramming
```python
import functools

def trace(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}({args})")
        result = func(*args, **kwargs)
        print(f"  → {result}")
        return result
    return wrapper

@trace
def add(a, b):
    return a + b

add(3, 4)
# Calling add((3, 4))
#   → 7
```

## 🏆 Key Takeaways
- Python compiles source to AST before bytecode — you can inspect and transform it
- `ast.NodeVisitor` lets you walk the tree and react to any node type
- Decorators are a clean form of metaprogramming — modify behavior without changing source
""",
        "questions": [
            {"text": "What does `ast.parse('x = 1')` return?", "options": [
                {"text": "An AST Module object representing the code", "correct": True},
                {"text": "A list of tokens", "correct": False},
                {"text": "Bytecode", "correct": False},
                {"text": "A dictionary of variables", "correct": False}]},
            {"text": "What does `@functools.wraps(func)` do inside a decorator?", "options": [
                {"text": "Preserves the original function's name and docstring", "correct": True},
                {"text": "Caches the function result", "correct": False},
                {"text": "Makes the function run faster", "correct": False},
                {"text": "Converts the function to a class", "correct": False}]},
            {"text": "Which class allows you to walk and react to AST nodes?", "options": [
                {"text": "ast.NodeVisitor", "correct": True}, {"text": "ast.Walker", "correct": False},
                {"text": "ast.TreeReader", "correct": False}, {"text": "ast.Inspector", "correct": False}]},
        ],
        "challenge": {
            "title": "Name Counter",
            "description": "Read a single-line Python expression from input. Count and print how many Name nodes (variable references) are in its AST.",
            "initial_code": "import ast\n# Parse input expression and count Name nodes\n",
            "solution_code": "import ast\n\ncode = input()\ntree = ast.parse(code, mode='eval')\ncount = sum(1 for node in ast.walk(tree) if isinstance(node, ast.Name))\nprint(count)\n",
            "test_cases": [{"input": "x + y + z", "expected": "3"}, {"input": "a * b", "expected": "2"}],
        },
    },

    # ── Lesson 7: Comparison Operators ──────────────────────────────────────
    "les-python-basics-7-beginner": {
        "title": "Comparison Operators",
        "content": """# Comparison Operators

## 🎯 Learning Objectives
- Use comparison operators to compare values
- Understand the difference between `==` and `is`
- Chain comparisons Python-style

## 📚 Concept Overview
Comparison operators return `True` or `False`.

| Operator | Meaning | Example |
|----------|---------|---------|
| `==` | Equal | `5 == 5` → True |
| `!=` | Not Equal | `5 != 3` → True |
| `>` | Greater than | `7 > 3` → True |
| `<` | Less than | `3 < 7` → True |
| `>=` | Greater or equal | `5 >= 5` → True |
| `<=` | Less or equal | `4 <= 5` → True |

### Python Chaining (unique feature!)
```python
x = 5
print(1 < x < 10)   # True — like math notation!
print(1 < x < 4)    # False
```

### `==` vs `is`
```python
a = [1, 2]
b = [1, 2]
print(a == b)   # True  — values are equal
print(a is b)   # False — different objects in memory
```

## ⚠️ Common Pitfalls
- Using `=` instead of `==` in conditions: `if x = 5:` is a SyntaxError
- Using `is` to compare strings/numbers (works by accident for cached values)

## 🏆 Key Takeaways
- `==` compares values; `is` compares identity (memory address)
- Python supports chained comparisons: `0 <= x < 100`
- All comparison operators return `bool` (`True` or `False`)
""",
        "questions": [
            {"text": "What does `3 == 3.0` evaluate to?", "options": [
                {"text": "True", "correct": True}, {"text": "False", "correct": False},
                {"text": "TypeError", "correct": False}, {"text": "3", "correct": False}]},
            {"text": "Which operator checks if two objects are the same in memory?", "options": [
                {"text": "is", "correct": True}, {"text": "==", "correct": False},
                {"text": "===", "correct": False}, {"text": "eq", "correct": False}]},
            {"text": "What does `1 < 5 < 10` return?", "options": [
                {"text": "True", "correct": True}, {"text": "False", "correct": False},
                {"text": "SyntaxError", "correct": False}, {"text": "1", "correct": False}]},
        ],
        "challenge": {
            "title": "Grade Classifier",
            "description": "Read a score (integer). Print 'A' if >=90, 'B' if >=80, 'C' if >=70, 'F' otherwise.",
            "initial_code": "# Read score and classify grade\n",
            "solution_code": "s = int(input())\nif s >= 90: print('A')\nelif s >= 80: print('B')\nelif s >= 70: print('C')\nelse: print('F')\n",
            "test_cases": [{"input": "95", "expected": "A"}, {"input": "75", "expected": "C"}, {"input": "50", "expected": "F"}],
        },
    },

    "les-python-basics-7-intermediate": {
        "title": "Rich Comparisons & __eq__ Protocol",
        "content": """# Rich Comparisons & __eq__ Protocol

## 🎯 Learning Objectives
- Implement custom comparison methods in classes
- Use `functools.total_ordering` to auto-generate missing comparisons
- Understand comparison with `None` and type coercion

## 📚 Concept Overview
### Dunder Comparison Methods
| Method | Operator |
|--------|----------|
| `__eq__` | `==` |
| `__ne__` | `!=` |
| `__lt__` | `<` |
| `__le__` | `<=` |
| `__gt__` | `>` |
| `__ge__` | `>=` |

```python
from functools import total_ordering

@total_ordering
class Score:
    def __init__(self, value):
        self.value = value
    def __eq__(self, other):
        return self.value == other.value
    def __lt__(self, other):
        return self.value < other.value

s1, s2 = Score(80), Score(90)
print(s1 < s2)   # True
print(s1 >= s2)  # False (auto-generated by total_ordering)
```

### Comparing with None
```python
x = None
print(x is None)    # ✓ Correct idiom
print(x == None)    # Works but less Pythonic
```

## 🏆 Key Takeaways
- Implement `__eq__` and `__lt__`, then use `@total_ordering` for all six
- Always use `is None` / `is not None` to check for None
- Type coercion (3 == 3.0 is True) is handled by `int.__eq__` checking float types
""",
        "questions": [
            {"text": "What does `@total_ordering` require you to define?", "options": [
                {"text": "__eq__ and one of __lt__, __le__, __gt__, __ge__", "correct": True},
                {"text": "All six comparison methods", "correct": False},
                {"text": "Only __eq__", "correct": False},
                {"text": "Only __lt__", "correct": False}]},
            {"text": "Which is the Pythonic way to check if x is None?", "options": [
                {"text": "x is None", "correct": True}, {"text": "x == None", "correct": False},
                {"text": "x === None", "correct": False}, {"text": "x.isNone()", "correct": False}]},
            {"text": "Which dunder method is called when you use `<`?", "options": [
                {"text": "__lt__", "correct": True}, {"text": "__less__", "correct": False},
                {"text": "__cmp__", "correct": False}, {"text": "__compare__", "correct": False}]},
        ],
        "challenge": {
            "title": "Sortable Student",
            "description": "Create a Student class with name and gpa. Make it comparable by gpa. Read two students (name gpa per line), print the one with higher gpa.",
            "initial_code": "from functools import total_ordering\n# Create sortable Student class\n",
            "solution_code": "from functools import total_ordering\n@total_ordering\nclass Student:\n    def __init__(self, name, gpa):\n        self.name, self.gpa = name, float(gpa)\n    def __eq__(self, o): return self.gpa == o.gpa\n    def __lt__(self, o): return self.gpa < o.gpa\n\na = Student(*input().split())\nb = Student(*input().split())\nprint((a if a > b else b).name)\n",
            "test_cases": [{"input": "Alice 3.8\nBob 3.5", "expected": "Alice"}, {"input": "Tom 2.9\nJane 3.9", "expected": "Jane"}],
        },
    },

    "les-python-basics-7-pro": {
        "title": "Spaceship Operator, Sorting Protocol & Bisect",
        "content": """# Sorting Protocol, Key Functions & Bisect

## 🎯 Learning Objectives
- Master Python's sorting key protocol
- Use `bisect` for binary search on sorted lists
- Understand sort stability and Timsort

## 📚 Concept Overview
### Key Functions for Sort
```python
students = [("Alice", 3.8), ("Bob", 3.5), ("Carol", 3.9)]
students.sort(key=lambda s: s[1], reverse=True)
# → [('Carol', 3.9), ('Alice', 3.8), ('Bob', 3.5)]

from operator import itemgetter, attrgetter
students.sort(key=itemgetter(1))  # equivalent, faster
```

### Timsort: Python's Sort Algorithm
Python uses **Timsort** — adaptive merge sort, O(n log n) worst case.
It's **stable**: equal elements keep their original relative order.

### bisect — Binary Search
```python
import bisect
a = [1, 3, 5, 7, 9]
bisect.insort(a, 4)   # inserts 4 in sorted position → [1,3,4,5,7,9]
idx = bisect.bisect_left(a, 5)  # → 3 (index where 5 is)
```

## 🏆 Key Takeaways
- Use `key=` parameter, not `cmp=` (removed in Python 3)
- Timsort is stable — use multi-key sort by sorting multiple times (least significant first)
- `bisect` gives O(log n) insertion point finding in sorted lists
""",
        "questions": [
            {"text": "What does Python's Timsort guarantee about equal elements?", "options": [
                {"text": "They maintain their original relative order (stable sort)", "correct": True},
                {"text": "They are sorted alphabetically", "correct": False},
                {"text": "They are moved to the front", "correct": False},
                {"text": "Nothing is guaranteed", "correct": False}]},
            {"text": "What does `bisect.insort(a, x)` do?", "options": [
                {"text": "Inserts x into sorted list a at the correct position", "correct": True},
                {"text": "Binary searches for x in a", "correct": False},
                {"text": "Removes x from a", "correct": False},
                {"text": "Splits a at index x", "correct": False}]},
            {"text": "Which module provides `attrgetter` for sort keys?", "options": [
                {"text": "operator", "correct": True}, {"text": "functools", "correct": False},
                {"text": "itertools", "correct": False}, {"text": "collections", "correct": False}]},
        ],
        "challenge": {
            "title": "Top K Students",
            "description": "Read N (number of students). Then read N lines of 'name score'. Print the top 3 students by score (descending).",
            "initial_code": "# Read N students, print top 3 by score\n",
            "solution_code": "n = int(input())\nstudents = [input().split() for _ in range(n)]\nstudents.sort(key=lambda x: int(x[1]), reverse=True)\nfor name, score in students[:3]:\n    print(name, score)\n",
            "test_cases": [{"input": "4\nAlice 90\nBob 85\nCarol 95\nDave 88", "expected": "Carol 95\nAlice 90\nDave 88"}],
        },
    },

    # ── Lesson 8: Logical Operators ──────────────────────────────────────────
    "les-python-basics-8-beginner": {
        "title": "Logical Operators — and, or, not",
        "content": """# Logical Operators — and, or, not

## 🎯 Learning Objectives
- Combine conditions with `and`, `or`, `not`
- Understand short-circuit evaluation
- Use logical operators in real-world conditions

## 📚 Concept Overview
| Operator | Description | Example |
|----------|-------------|---------|
| `and` | Both must be True | `True and False` → False |
| `or` | At least one True | `True or False` → True |
| `not` | Inverts boolean | `not True` → False |

### Truth Tables
```
A=T, B=T → A and B = T, A or B = T
A=T, B=F → A and B = F, A or B = T
A=F, B=F → A and B = F, A or B = F
```

### Real-world Example
```python
age = 20
has_id = True
if age >= 18 and has_id:
    print("Entry allowed")

username = ""
display = username or "Guest"   # "Guest" if username is empty
print(display)
```

## ⚠️ Common Pitfalls
- `not x == y` is `not (x == y)` — use `x != y` for clarity
- `0`, `""`, `[]`, `None` are all falsy in Python

## 🏆 Key Takeaways
- `and` / `or` use short-circuit evaluation (stops early when result is determined)
- `or` can provide defaults: `value = x or "default"`
- Falsy values: `0`, `0.0`, `""`, `[]`, `{}`, `None`, `False`
""",
        "questions": [
            {"text": "What does `True and False` evaluate to?", "options": [
                {"text": "False", "correct": True}, {"text": "True", "correct": False},
                {"text": "None", "correct": False}, {"text": "Error", "correct": False}]},
            {"text": "What is short-circuit evaluation in `and`?", "options": [
                {"text": "If first operand is False, skip evaluating the second", "correct": True},
                {"text": "Both operands always evaluated", "correct": False},
                {"text": "Returns the first operand only", "correct": False},
                {"text": "Converts to integers before comparing", "correct": False}]},
            {"text": "Which of the following is a falsy value?", "options": [
                {"text": "[]", "correct": True}, {"text": "1", "correct": False},
                {"text": "'False'", "correct": False}, {"text": "[0]", "correct": False}]},
        ],
        "challenge": {
            "title": "Login Validator",
            "description": "Read username and password on separate lines. Print 'Access Granted' if username is 'admin' AND password is 'secret123', else 'Access Denied'.",
            "initial_code": "# Read username and password, validate login\n",
            "solution_code": "u = input()\np = input()\nprint('Access Granted' if u == 'admin' and p == 'secret123' else 'Access Denied')\n",
            "test_cases": [{"input": "admin\nsecret123", "expected": "Access Granted"}, {"input": "admin\nwrong", "expected": "Access Denied"}],
        },
    },

    "les-python-basics-8-intermediate": {
        "title": "Boolean Algebra, De Morgan's Laws & Truthiness",
        "content": """# Boolean Algebra, De Morgan's Laws & Truthiness

## 🎯 Learning Objectives
- Apply De Morgan's Laws to simplify conditions
- Understand Python's `__bool__` and `__len__` truthiness protocol
- Use `any()` and `all()` for collection-wide logic

## 📚 Concept Overview
### De Morgan's Laws
```
not (A and B)  ==  (not A) or (not B)
not (A or B)   ==  (not A) and (not B)
```
```python
# Instead of: not (x > 0 and y > 0)
# Write:       x <= 0 or y <= 0  (cleaner!)
```

### any() and all()
```python
scores = [85, 92, 78, 96, 45]
print(all(s >= 50 for s in scores))   # False (45 fails)
print(any(s >= 95 for s in scores))   # True  (96 passes)
```

### Custom Truthiness with __bool__
```python
class Cart:
    def __init__(self, items):
        self.items = items
    def __bool__(self):
        return len(self.items) > 0

cart = Cart([])
if not cart:
    print("Cart is empty!")   # prints this
```

## 🏆 Key Takeaways
- De Morgan's Laws help simplify complex boolean expressions
- `any()` / `all()` are lazy — stop evaluating once result is known
- Define `__bool__` to control how objects behave in boolean context
""",
        "questions": [
            {"text": "What is De Morgan's law for `not (A and B)`?", "options": [
                {"text": "not A or not B", "correct": True},
                {"text": "not A and not B", "correct": False},
                {"text": "A or B", "correct": False},
                {"text": "not A and B", "correct": False}]},
            {"text": "What does `all([True, True, False])` return?", "options": [
                {"text": "False", "correct": True}, {"text": "True", "correct": False},
                {"text": "[True, True]", "correct": False}, {"text": "None", "correct": False}]},
            {"text": "Which dunder method controls an object's truthiness?", "options": [
                {"text": "__bool__", "correct": True}, {"text": "__true__", "correct": False},
                {"text": "__truthy__", "correct": False}, {"text": "__is_true__", "correct": False}]},
        ],
        "challenge": {
            "title": "All Pass Checker",
            "description": "Read N then N integers. Print 'All Pass' if all are >= 50, 'Some Fail' if any < 50.",
            "initial_code": "# Use all() to check if every score >= 50\n",
            "solution_code": "n = int(input())\nscores = [int(input()) for _ in range(n)]\nprint('All Pass' if all(s >= 50 for s in scores) else 'Some Fail')\n",
            "test_cases": [{"input": "3\n60\n70\n80", "expected": "All Pass"}, {"input": "3\n60\n40\n80", "expected": "Some Fail"}],
        },
    },

    "les-python-basics-8-pro": {
        "title": "SAT Solving & Constraint Programming with Python",
        "content": """# Boolean Logic: SAT, Constraint Programming & Z3

## 🎯 Learning Objectives
- Model real problems as boolean satisfiability (SAT) problems
- Use Python to brute-force SAT instances
- Understand constraint propagation basics

## 📚 Concept Overview
### Brute-force SAT Solver
```python
from itertools import product

def sat(clauses, variables):
    for assignment in product([False, True], repeat=len(variables)):
        values = dict(zip(variables, assignment))
        if all(
            any(values[v] if not neg else not values[v] for v, neg in clause)
            for clause in clauses
        ):
            return values
    return None

# Solve: (A or B) and (not A or C) and (not B or not C)
result = sat(
    clauses=[[('A', False), ('B', False)], [('A', True), ('C', False)], [('B', True), ('C', True)]],
    variables=['A', 'B', 'C']
)
print(result)
```

### Real Applications
- Package dependency resolution (pip, apt use SAT solvers)
- Circuit verification
- Test case generation

## 🏆 Key Takeaways
- Any logical constraint can be expressed as conjunctive normal form (CNF)
- Brute-force works for small instances; industrial solvers (Z3, MiniSat) scale to millions of vars
- Python's `itertools.product` generates all boolean combinations efficiently
""",
        "questions": [
            {"text": "What does a SAT solver determine?", "options": [
                {"text": "Whether a boolean formula can be satisfied", "correct": True},
                {"text": "The fastest sorting algorithm", "correct": False},
                {"text": "Memory usage of a program", "correct": False},
                {"text": "Syntax errors in Python", "correct": False}]},
            {"text": "What does `itertools.product([F,T], repeat=3)` generate?", "options": [
                {"text": "All 8 combinations of True/False for 3 variables", "correct": True},
                {"text": "3 True values and 3 False values", "correct": False},
                {"text": "A sorted list of booleans", "correct": False},
                {"text": "3 repetitions of [False, True]", "correct": False}]},
            {"text": "SAT solvers are used in which real-world application?", "options": [
                {"text": "Package dependency resolution", "correct": True},
                {"text": "Image rendering", "correct": False},
                {"text": "Network routing", "correct": False},
                {"text": "Database indexing", "correct": False}]},
        ],
        "challenge": {
            "title": "Satisfiability Check",
            "description": "Read A and B as 'True'/'False'. Print 'SAT' if (A or B) and (not A or not B) is satisfiable with the given values, else 'UNSAT'.",
            "initial_code": "# Read A and B, evaluate (A or B) and (not A or not B)\n",
            "solution_code": "A = input().strip() == 'True'\nB = input().strip() == 'True'\nresult = (A or B) and (not A or not B)\nprint('SAT' if result else 'UNSAT')\n",
            "test_cases": [{"input": "True\nFalse", "expected": "SAT"}, {"input": "True\nTrue", "expected": "UNSAT"}],
        },
    },

    # ── Lesson 9: String Formatting ──────────────────────────────────────────
    "m1-9-debugging-basics-beginner-beginner": {
        "title": "String Formatting with f-strings",
        "content": """# String Formatting with f-strings

## 🎯 Learning Objectives
- Format strings using f-strings (PEP 498)
- Apply format specifiers for numbers and alignment
- Use multi-line f-strings

## 📚 Concept Overview
f-strings (formatted string literals) let you embed Python expressions directly in strings.

```python
name = "Alice"
score = 98.567

# Basic embedding
print(f"Name: {name}, Score: {score}")

# Format specifiers: {value:format_spec}
print(f"Score: {score:.2f}")        # 98.57 (2 decimal places)
print(f"Score: {score:8.2f}")       # "   98.57" (8 wide, right-aligned)
print(f"{'Left':<10}|{'Right':>10}") # Left      |     Right
print(f"{42:05d}")                   # 00042 (zero-padded)
```

### Expression Support
```python
print(f"{2 ** 10}")           # 1024
print(f"{'hello'.upper()}")   # HELLO
print(f"{10 > 5}")            # True
```

## ⚠️ Common Pitfalls
- Backslashes not allowed inside f-string expressions: use a variable instead
- f-strings are evaluated at definition time (not lazily)

## 🏆 Key Takeaways
- f-strings are the fastest string formatting method in Python
- Format spec syntax: `{value:[[fill]align][width][.precision][type]}`
- Any valid Python expression can go inside `{...}`
""",
        "questions": [
            {"text": "What does `f'{3.14159:.2f}'` produce?", "options": [
                {"text": "'3.14'", "correct": True}, {"text": "'3.14159'", "correct": False},
                {"text": "3.14", "correct": False}, {"text": "'3'", "correct": False}]},
            {"text": "What does `{value:<10}` do in an f-string?", "options": [
                {"text": "Left-aligns value in a field of width 10", "correct": True},
                {"text": "Right-aligns value in a field of width 10", "correct": False},
                {"text": "Centers value in a field of width 10", "correct": False},
                {"text": "Truncates value to 10 characters", "correct": False}]},
            {"text": "Which Python version introduced f-strings?", "options": [
                {"text": "3.6", "correct": True}, {"text": "3.0", "correct": False},
                {"text": "2.7", "correct": False}, {"text": "3.9", "correct": False}]},
        ],
        "challenge": {
            "title": "Receipt Formatter",
            "description": "Read item name and price (float). Print a formatted receipt line: name left-aligned in 20 chars, price right-aligned in 8 chars with 2 decimal places.",
            "initial_code": "# Format a receipt line\n",
            "solution_code": "name = input()\nprice = float(input())\nprint(f'{name:<20}{price:>8.2f}')\n",
            "test_cases": [{"input": "Apple\n1.5", "expected": "Apple                    1.50"}],
        },
    },

    "m1-9-debugging-basics-intermediate-intermediate": {
        "title": "Template Strings, .format() & Format Mini-Language",
        "content": """# Template Strings, .format() & Format Mini-Language

## 🎯 Learning Objectives
- Compare all string formatting approaches
- Master the format mini-language for numbers, dates, and alignment
- Use `string.Template` for safe untrusted formatting

## 📚 Concept Overview
### Formatting Approaches Compared
```python
name, val = "Sales", 1234567.89

# f-string (preferred)
print(f"{name}: {val:,.2f}")          # Sales: 1,234,567.89

# .format()
print("{}: {:,.2f}".format(name, val))  # Same output

# % style (legacy)
print("%s: %,.2f" % (name, val))       # Not supported in % style!
```

### Format Mini-Language
```python
# Number formats
print(f"{255:b}")    # 11111111  (binary)
print(f"{255:o}")    # 377       (octal)
print(f"{255:x}")    # ff        (hex)
print(f"{1e-4:.2e}") # 1.00e-04  (scientific)
print(f"{0.75:.0%}") # 75%       (percentage)
```

### string.Template (Safe for User Input)
```python
from string import Template
t = Template("Hello, $name! Your score is $score.")
print(t.substitute(name="Alice", score=95))
# Prevents injection — $ vars only, no expressions
```

## 🏆 Key Takeaways
- Use f-strings for internal code; `Template` for user-provided format strings
- Format mini-language: `b`=binary, `o`=octal, `x`=hex, `e`=scientific, `%`=percentage
- `,` in format spec inserts thousand separators
""",
        "questions": [
            {"text": "What does `f'{255:x}'` produce?", "options": [
                {"text": "'ff'", "correct": True}, {"text": "'255'", "correct": False},
                {"text": "'0xff'", "correct": False}, {"text": "'11111111'", "correct": False}]},
            {"text": "When should you use `string.Template` over f-strings?", "options": [
                {"text": "When the format string comes from untrusted user input", "correct": True},
                {"text": "When you need faster performance", "correct": False},
                {"text": "When formatting floats", "correct": False},
                {"text": "Always — it's newer", "correct": False}]},
            {"text": "What does `f'{0.75:.0%}'` output?", "options": [
                {"text": "'75%'", "correct": True}, {"text": "'0.75%'", "correct": False},
                {"text": "'75.0%'", "correct": False}, {"text": "'0.75'", "correct": False}]},
        ],
        "challenge": {
            "title": "Number Converter",
            "description": "Read an integer. Print it in decimal, binary, octal, and hex on separate lines with labels.",
            "initial_code": "# Read integer and print in 4 numeral systems\n",
            "solution_code": "n = int(input())\nprint(f'Dec: {n}')\nprint(f'Bin: {n:b}')\nprint(f'Oct: {n:o}')\nprint(f'Hex: {n:x}')\n",
            "test_cases": [{"input": "255", "expected": "Dec: 255\nBin: 11111111\nOct: 377\nHex: ff"}],
        },
    },

    "m1-9-debugging-basics-pro-pro": {
        "title": "Custom __format__, PEP 701 & Lazy String Interpolation",
        "content": """# Custom __format__, f-string Debugging & Lazy Interpolation

## 🎯 Learning Objectives
- Implement `__format__` in custom classes
- Use f-string `=` debugging specifier (Python 3.8+)
- Implement lazy string interpolation with `__str__` deferral

## 📚 Concept Overview
### __format__ Protocol
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __format__(self, spec):
        if spec == 'polar':
            r = (self.x**2 + self.y**2) ** 0.5
            return f"({r:.2f} at angle)"
        return f"({self.x}, {self.y})"

v = Vector(3, 4)
print(f"{v}")          # (3, 4)
print(f"{v:polar}")    # (5.00 at angle)
```

### f-string Debugging (Python 3.8+)
```python
x = 42
print(f"{x=}")     # x=42  (variable name + value)
print(f"{x*2=}")   # x*2=84
```

### Lazy Interpolation Pattern
```python
class Lazy:
    def __init__(self, func):
        self._func = func
    def __str__(self):
        return self._func()   # evaluated only when converted to string

msg = Lazy(lambda: f"Current time: {__import__('time').ctime()}")
# msg is NOT evaluated yet
print(msg)   # evaluated NOW
```

## 🏆 Key Takeaways
- `__format__` lets objects define their own format spec language
- `f"{var=}"` is a powerful debugging shortcut (Python 3.8+)
- Lazy interpolation defers expensive string construction until actually needed
""",
        "questions": [
            {"text": "What does `f'{x=}'` print when x=10?", "options": [
                {"text": "x=10", "correct": True}, {"text": "10", "correct": False},
                {"text": "x", "correct": False}, {"text": "SyntaxError", "correct": False}]},
            {"text": "Which dunder method lets a class control its f-string formatting?", "options": [
                {"text": "__format__", "correct": True}, {"text": "__str__", "correct": False},
                {"text": "__repr__", "correct": False}, {"text": "__display__", "correct": False}]},
            {"text": "Lazy interpolation is useful when:", "options": [
                {"text": "String construction is expensive and may not be needed", "correct": True},
                {"text": "You want faster f-strings", "correct": False},
                {"text": "You need to format binary numbers", "correct": False},
                {"text": "You want to format dates automatically", "correct": False}]},
        ],
        "challenge": {
            "title": "Custom Currency Format",
            "description": "Create a Money class with `__format__` that formats as '$X.XX' when spec is 'usd'. Read a float, create Money, print it with usd format.",
            "initial_code": "class Money:\n    def __init__(self, amount):\n        self.amount = amount\n    def __format__(self, spec):\n        pass  # implement this\n",
            "solution_code": "class Money:\n    def __init__(self, amount):\n        self.amount = amount\n    def __format__(self, spec):\n        if spec == 'usd':\n            return f'${self.amount:.2f}'\n        return str(self.amount)\n\nm = Money(float(input()))\nprint(f'{m:usd}')\n",
            "test_cases": [{"input": "19.99", "expected": "$19.99"}, {"input": "100", "expected": "$100.00"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "m1-10-mini-project-greeting-app-beginner-beginner": {
        "title": "Mini Project: Command-Line Calculator",
        "content": """# Mini Project: Command-Line Calculator

## 🎯 Learning Objectives
- Combine variables, input, operators, and conditionals into a real program
- Build a complete interactive calculator
- Handle invalid input gracefully

## 📚 Project Overview
You will build a simple calculator that:
1. Reads two numbers from the user
2. Asks for the operator (+, -, *, /)
3. Computes and prints the result
4. Handles division by zero

## 💻 Implementation
```python
def calculate(a, operator, b):
    if operator == '+': return a + b
    elif operator == '-': return a - b
    elif operator == '*': return a * b
    elif operator == '/':
        if b == 0:
            return "Error: Division by zero"
        return a / b
    else:
        return "Error: Unknown operator"

# Get input
a = float(input("Enter first number: "))
op = input("Enter operator (+, -, *, /): ").strip()
b = float(input("Enter second number: "))

result = calculate(a, op, b)
print(f"Result: {result}")
```

## 🏆 What You Learned
- Combining all Python Basics concepts into one working program
- Function design: single responsibility principle
- Defensive programming (checking for division by zero)
- User input sanitization with `.strip()`
""",
        "questions": [
            {"text": "Why do we call `.strip()` on the operator input?", "options": [
                {"text": "To remove accidental whitespace", "correct": True},
                {"text": "To convert it to uppercase", "correct": False},
                {"text": "To validate it is a number", "correct": False},
                {"text": "To limit it to one character", "correct": False}]},
            {"text": "What should happen when dividing by zero?", "options": [
                {"text": "Return an error message, not crash", "correct": True},
                {"text": "Return 0", "correct": False},
                {"text": "Return infinity", "correct": False},
                {"text": "The program should exit", "correct": False}]},
            {"text": "What does the 'single responsibility principle' mean for functions?", "options": [
                {"text": "Each function should do one thing well", "correct": True},
                {"text": "Each program should have one function", "correct": False},
                {"text": "Functions must return a single value", "correct": False},
                {"text": "Functions must have a single parameter", "correct": False}]},
        ],
        "challenge": {
            "title": "Full Calculator",
            "description": "Read: first number, operator (+,-,*,/), second number on separate lines. Print the result (2 decimal places for division). If dividing by zero print 'Error: Division by zero'.",
            "initial_code": "# Build a complete calculator\n",
            "solution_code": "a = float(input())\nop = input().strip()\nb = float(input())\nif op == '+': print(a + b)\nelif op == '-': print(a - b)\nelif op == '*': print(a * b)\nelif op == '/':\n    if b == 0: print('Error: Division by zero')\n    else: print(round(a / b, 2))\n",
            "test_cases": [
                {"input": "10\n+\n5", "expected": "15.0"},
                {"input": "10\n/\n0", "expected": "Error: Division by zero"},
                {"input": "9\n/\n2", "expected": "4.5"},
            ],
        },
    },

    "m1-10-mini-project-greeting-app-intermediate-intermediate": {
        "title": "Mini Project: Expression Evaluator",
        "content": """# Mini Project: Expression Evaluator

## 🎯 Learning Objectives
- Parse and evaluate mathematical expressions from strings
- Implement operator precedence manually
- Use Python's `ast.literal_eval` safely

## 📚 Project Overview
Build an expression evaluator that handles `+`, `-`, `*`, `/`, and parentheses.

## 💻 Implementation (Safe eval)
```python
import re
import operator

OPERATORS = {'+': operator.add, '-': operator.sub,
             '*': operator.mul, '/': operator.truediv}

def safe_calc(expr):
    # Remove spaces
    expr = expr.replace(" ", "")
    # Only allow digits, operators, parentheses, and dots
    if not re.match(r'^[\\d+\\-*/().]+$', expr):
        return "Invalid expression"
    try:
        # Safe: only literal math, no function calls
        return eval(compile(expr, "<string>", "eval"))
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: {e}"

expr = input("Enter expression: ")
print(f"Result: {safe_calc(expr)}")
```

## 🏆 What You Learned
- Input sanitization with regex before eval
- Operator module for cleaner code
- Safe usage of `eval` with input validation
""",
        "questions": [
            {"text": "Why must you validate input before using `eval()`?", "options": [
                {"text": "eval() can execute arbitrary code — input must be sanitized", "correct": True},
                {"text": "eval() is slow without validation", "correct": False},
                {"text": "eval() only works with integers", "correct": False},
                {"text": "eval() cannot handle float results", "correct": False}]},
            {"text": "What does `operator.add(3, 4)` return?", "options": [
                {"text": "7", "correct": True}, {"text": "'3+4'", "correct": False},
                {"text": "None", "correct": False}, {"text": "operator", "correct": False}]},
            {"text": "What regex character class allows only digits and operators?", "options": [
                {"text": r"[\\d+\\-*/().]", "correct": True}, {"text": r"[a-z]", "correct": False},
                {"text": r"\\w+", "correct": False}, {"text": r"[0-9a-zA-Z]", "correct": False}]},
        ],
        "challenge": {
            "title": "Safe Expression Evaluator",
            "description": "Read a math expression. Evaluate it and print the result rounded to 2 decimal places. If the expression is invalid or divides by zero, print 'Error'.",
            "initial_code": "import re\n# Safely evaluate the math expression\n",
            "solution_code": "import re\nexpr = input().strip()\nif not re.match(r'^[0-9+\\-*/().\\s]+$', expr):\n    print('Error')\nelse:\n    try:\n        result = eval(expr)\n        print(round(result, 2))\n    except:\n        print('Error')\n",
            "test_cases": [{"input": "3 + 4 * 2", "expected": "11"}, {"input": "10 / 0", "expected": "Error"}],
        },
    },

    "m1-10-mini-project-greeting-app-pro-pro": {
        "title": "Mini Project: Recursive Descent Parser",
        "content": """# Mini Project: Recursive Descent Parser

## 🎯 Learning Objectives
- Build a hand-written recursive descent parser for math expressions
- Implement operator precedence grammar
- Understand tokenization and parsing theory

## 📚 Grammar Definition
```
expr   := term (('+' | '-') term)*
term   := factor (('*' | '/') factor)*
factor := NUMBER | '(' expr ')'
```

## 💻 Implementation
```python
class Parser:
    def __init__(self, text):
        self.tokens = iter(self._tokenize(text))
        self.current = None
        self._advance()

    def _tokenize(self, text):
        import re
        return re.findall(r'\\d+\\.?\\d*|[+\\-*/()]', text.replace(' ',''))

    def _advance(self):
        try:
            self.current = next(self.tokens)
        except StopIteration:
            self.current = None

    def parse(self):
        return self._expr()

    def _expr(self):
        result = self._term()
        while self.current in ('+', '-'):
            op = self.current; self._advance()
            result = result + self._term() if op == '+' else result - self._term()
        return result

    def _term(self):
        result = self._factor()
        while self.current in ('*', '/'):
            op = self.current; self._advance()
            result = result * self._factor() if op == '*' else result / self._factor()
        return result

    def _factor(self):
        if self.current == '(':
            self._advance()
            result = self._expr()
            self._advance()  # consume ')'
            return result
        val = float(self.current); self._advance()
        return val

expr = input()
print(round(Parser(expr).parse(), 2))
```

## 🏆 What You Learned
- Recursive descent parsing implements grammar rules directly as functions
- Operator precedence falls naturally from the grammar hierarchy (term before expr)
- Tokenization separates lexing from parsing — two distinct phases
""",
        "questions": [
            {"text": "In recursive descent parsing, what does each grammar rule become?", "options": [
                {"text": "A function", "correct": True}, {"text": "A class", "correct": False},
                {"text": "A loop", "correct": False}, {"text": "A dictionary", "correct": False}]},
            {"text": "How is operator precedence handled in a recursive descent parser?", "options": [
                {"text": "Higher-precedence operators are in deeper grammar rules", "correct": True},
                {"text": "Using Python's built-in precedence rules", "correct": False},
                {"text": "With a priority queue", "correct": False},
                {"text": "By sorting operators before parsing", "correct": False}]},
            {"text": "What does tokenization do?", "options": [
                {"text": "Breaks input text into meaningful units (tokens)", "correct": True},
                {"text": "Evaluates the expression", "correct": False},
                {"text": "Checks grammar rules", "correct": False},
                {"text": "Compiles to bytecode", "correct": False}]},
        ],
        "challenge": {
            "title": "Parser Test",
            "description": "Read a math expression with +, -, *, /, and parentheses. Evaluate and print the result rounded to 2 decimal places using a recursive descent parser.",
            "initial_code": "# Implement recursive descent parser and evaluate expression\n",
            "solution_code": "import re\n\nclass Parser:\n    def __init__(self, text):\n        self.tokens = re.findall(r'\\d+\\.?\\d*|[+\\-*/()', text.replace(' ','')]\n        self.pos = 0\n    @property\n    def cur(self):\n        return self.tokens[self.pos] if self.pos < len(self.tokens) else None\n    def eat(self): t=self.cur; self.pos+=1; return t\n    def parse(self): return self._expr()\n    def _expr(self):\n        v=self._term()\n        while self.cur in('+','-'): op=self.eat(); v=v+self._term() if op=='+' else v-self._term()\n        return v\n    def _term(self):\n        v=self._factor()\n        while self.cur in('*','/'): op=self.eat(); v=v*self._factor() if op=='*' else v/self._factor()\n        return v\n    def _factor(self):\n        if self.cur=='(': self.eat(); v=self._expr(); self.eat(); return v\n        return float(self.eat())\n\nexpr=input()\nprint(round(Parser(expr).parse(),2))\n",
            "test_cases": [{"input": "(3 + 4) * 2", "expected": "14.0"}, {"input": "10 - 2 * 3", "expected": "4.0"}],
        },
    },
}


class Command(BaseCommand):
    help = "Hydrate Module 1 Python Basics — Lessons 6-10"

    def handle(self, *args, **options):
        count = 0
        with transaction.atomic():
            for lesson_id, data in LESSONS.items():
                updated = Lesson.objects.filter(id=lesson_id).update(
                    title=data["title"],
                    content=data["content"],
                )
                if not updated:
                    self.stdout.write(self.style.WARNING(f"  [WARN]  Not found: {lesson_id}"))
                    continue

                quiz, _ = Quiz.objects.get_or_create(
                    id=f"quiz-{lesson_id}",
                    defaults={"lesson_id": lesson_id, "title": f"Quiz: {data['title']}"},
                )
                Question.objects.filter(quiz_id=quiz.id).delete()
                for i, q in enumerate(data["questions"]):
                    Question.objects.create(
                        id=f"q-{lesson_id}-{i+1}", quiz_id=quiz.id,
                        text=q["text"], type="mcq", options=q["options"], points=5,
                    )

                ch = data["challenge"]
                Challenge.objects.filter(lesson_id=lesson_id).delete()
                Challenge.objects.create(
                    id=f"ch-{lesson_id}",
                    lesson_id=lesson_id, title=ch["title"], description=ch["description"],
                    initial_code=ch["initial_code"], solution_code=ch["solution_code"],
                    test_cases=ch["test_cases"], points=20,
                )
                count += 1
                self.stdout.write(f"  OK {lesson_id}")

        self.stdout.write(self.style.SUCCESS(f"\nDONE Hydrated {count} lessons (6-10) in Module 1"))
