"""python manage.py hydrate_module3 -- Module 3 Control Flow Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: If Statements ──────────────────────────────────────────────
    "les-control-flow-1-beginner": {
        "title": "Basic If Statements",
        "content": """# Basic If Statements

## 🎯 Learning Objectives
- Understand the syntax and purpose of `if` statements
- Use comparison operators in conditions
- Grasp the importance of indentation in Python

## 📚 Concept Overview
The `if` statement is used to execute a block of code only if a specified condition is true.

```python
x = 10
if x > 5:
    print("x is greater than 5")
```

### Indentation is Key
In Python, indentation (usually 4 spaces) defines the scope of the code block. If you forget to indent, Python will raise an `IndentationError`.

## 💻 Code Walkthrough
```python
age = int(input("Enter your age: "))
if age >= 18:
    print("You are an adult.")
    print("You can vote.")
print("This line always runs.")
```

## ⚠️ Common Pitfalls
- Forgetting the colon `:` at the end of the `if` line.
- Inconsistent indentation (mixing tabs and spaces).
- Using `=` (assignment) instead of `==` (equality) in conditions.

## 🏆 Key Takeaways
- `if` statements control the flow of execution based on logic.
- The condition must evaluate to a boolean (`True` or `False`).
- Always use a colon and proper indentation.
""",
        "questions": [
            {"text": "What character must end an `if` statement line?", "options": [
                {"text": ":", "correct": True}, {"text": ";", "correct": False},
                {"text": "{", "correct": False}, {"text": ".", "correct": False}]},
            {"text": "What happens if you forget to indent the code inside an `if` block?", "options": [
                {"text": "IndentationError is raised", "correct": True}, {"text": "Code runs anyway", "correct": False},
                {"text": "Code is ignored", "correct": False}, {"text": "Python auto-indents it", "correct": False}]},
            {"text": "Which operator check if two values are equal?", "options": [
                {"text": "==", "correct": True}, {"text": "=", "correct": False},
                {"text": "===", "correct": False}, {"text": "is", "correct": False}]},
        ],
        "challenge": {
            "title": "Positive Check",
            "description": "Read an integer. If it is positive (greater than 0), print 'Positive'.",
            "initial_code": "# Read number and check if positive\n",
            "solution_code": "n = int(input())\nif n > 0:\n    print('Positive')\n",
            "test_cases": [{"input": "5", "expected": "Positive"}, {"input": "-2", "expected": ""}],
        },
    },

    "les-control-flow-1-intermediate": {
        "title": "Nested If Statements & Scope",
        "content": """# Nested If Statements & Scope

## 🎯 Learning Objectives
- Use nested `if` statements for complex logic
- Understand how variable scope works within blocks
- Avoid "Arrow Code" (deep nesting)

## 📚 Concept Overview
Nested `if` statements allow you to check multiple layers of conditions.

```python
x = 10
y = 20
if x > 5:
    if y > 15:
        print("Both conditions are met")
```

### Guard Clauses
Sometimes, it's cleaner to check for negative conditions early and exit, rather than nesting deep.

## ⚠️ Common Pitfalls
- Over-nesting makes code hard to read and debug.
- Variables defined inside an `if` block are still accessible outside it in Python (no block scope for variables), but only if the block actually ran!

## 🏆 Key Takeaways
- Nesting is powerful but should be used sparingly.
- Indentation helps visualize the layers of logic.
""",
        "questions": [
            {"text": "What is 'Arrow Code'?", "options": [
                {"text": "Code with too many nested levels", "correct": True}, {"text": "Code that uses arrows (->)", "correct": False},
                {"text": "Highly optimized code", "correct": False}, {"text": "Code that runs in one direction", "correct": False}]},
            {"text": "Are variables created inside an `if` block restricted to that block in Python?", "options": [
                {"text": "No, Python has function/module scope, not block scope", "correct": True},
                {"text": "Yes, they are deleted after the block", "correct": False},
                {"text": "Only if they are integers", "correct": False},
                {"text": "Only if using the 'let' keyword", "correct": False}]},
        ],
        "challenge": {
            "title": "Even Positive",
            "description": "Read an integer. If it is positive AND even, print 'Even Positive'. Use nested if statements.",
            "initial_code": "# Use nested if to check positive and even\n",
            "solution_code": "n = int(input())\nif n > 0:\n    if n % 2 == 0:\n        print('Even Positive')\n",
            "test_cases": [{"input": "4", "expected": "Even Positive"}, {"input": "3", "expected": ""}, {"input": "-4", "expected": ""}],
        },
    },

    "les-control-flow-1-pro": {
        "title": "Conditional Expressions (Ternary)",
        "content": """# Conditional Expressions (Ternary)

## 🎯 Learning Objectives
- Write concise one-line `if/else` expressions
- Understand the syntax difference between ternary and standard `if` blocks
- Know when to use (and when to avoid) one-liners

## 📚 Concept Overview
In Python, you can write a conditional in a single line. This is often called a **ternary operator**.

```python
# Standard
if x > 10:
    status = "High"
else:
    status = "Low"

# Ternary
status = "High" if x > 10 else "Low"
```

### Syntax
`value_if_true if condition else value_if_false`

## ⚠️ Common Pitfalls
- Trying to cram too much logic into one line makes it unreadable.
- Forgetting the `else` part — it is required in a ternary expression.

## 🏆 Key Takeaways
- Use ternary expressions for simple assignments.
- Readability should always come before conciseness.
""",
        "questions": [
            {"text": "Which is the correct syntax for a Python ternary expression?", "options": [
                {"text": "x if condition else y", "correct": True}, {"text": "condition ? x : y", "correct": False},
                {"text": "if condition x else y", "correct": False}, {"text": "x if condition", "correct": False}]},
            {"text": "Is the `else` part mandatory in a Python conditional expression?", "options": [
                {"text": "Yes", "correct": True}, {"text": "No", "correct": False},
                {"text": "Only for integers", "correct": False}, {"text": "Only in functions", "correct": False}]},
        ],
        "challenge": {
            "title": "Short Sign Check",
            "description": "Read an integer. Using a single line conditional expression, print 'Positive' if > 0, else print 'Not Positive'.",
            "initial_code": "# One-line condition\n",
            "solution_code": "n = int(input())\nprint('Positive' if n > 0 else 'Not Positive')\n",
            "test_cases": [{"input": "10", "expected": "Positive"}, {"input": "-5", "expected": "Not Positive"}, {"input": "0", "expected": "Not Positive"}],
        },
    },

    # ── Lesson 2: Else & Elif ──────────────────────────────────────────────
    "les-control-flow-2-beginner": {
        "title": "The Else & Elif Clauses",
        "content": """# The Else & Elif Clauses

## 🎯 Learning Objectives
- Use `else` to handle the alternative case
- Use `elif` to check multiple mutually exclusive conditions
- Chain conditions together logically

## 📚 Concept Overview
When you have more than one possibility, `elif` (else if) and `else` come into play.

```python
score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
else:
    print("Grade: C")
```

### Mutually Exclusive
Only **one** block in an `if...elif...else` chain will ever run — the first one where the condition is True.

## ⚠️ Common Pitfalls
- Reordering `elif` blocks incorrectly (e.g., checking `score >= 80` before `score >= 90`).
- Forgetting that `else` doesn't take a condition.

## 🏆 Key Takeaways
- Use `elif` for multiple choices.
- Use `else` for a catch-all fallback.
- Order matters: put the most specific conditions first.
""",
        "questions": [
            {"text": "What does `elif` stand for?", "options": [
                {"text": "else if", "correct": True}, {"text": "each if", "correct": False},
                {"text": "every if", "correct": False}, {"text": "extra if", "correct": False}]},
            {"text": "How many `elif` blocks can you have in one chain?", "options": [
                {"text": "As many as you want", "correct": True}, {"text": "Only one", "correct": False},
                {"text": "Maximum of 5", "correct": False}, {"text": "It depends on the variables", "correct": False}]},
            {"text": "Can an `else` block have a condition like `else x > 5:`?", "options": [
                {"text": "No, else is a catch-all without a condition", "correct": True},
                {"text": "Yes", "correct": False},
                {"text": "Only if it follows an elif", "correct": False},
                {"text": "Only for float values", "correct": False}]},
        ],
        "challenge": {
            "title": "Age Category",
            "description": "Read an age. Print 'Child' if < 13, 'Teen' if < 20, else 'Adult'.",
            "initial_code": "# Use if-elif-else\n",
            "solution_code": "age = int(input())\nif age < 13:\n    print('Child')\nelif age < 20:\n    print('Teen')\nelse:\n    print('Adult')\n",
            "test_cases": [{"input": "10", "expected": "Child"}, {"input": "15", "expected": "Teen"}, {"input": "25", "expected": "Adult"}],
        },
    },

    "les-control-flow-2-intermediate": {
        "title": "Optimizing Conditional Chains",
        "content": """# Optimizing Conditional Chains

## 🎯 Learning Objectives
- Order conditions for maximum performance
- Use dictionaries as 'Switch' statement alternatives
- Understand truthy and falsy evaluation in chains

## 📚 Concept Overview
### Efficiency
In an `elif` chain, Python stops as soon as it finds a match. For performance, place the most likely conditions at the top.

### The Dictionary Mapping Pattern
Since Python didn't have a `switch` statement (until 3.10), many developers use dictionaries.

```python
# Instead of many elifs:
def get_status(code):
    return {
        200: "OK",
        404: "Not Found",
        500: "Server Error"
    }.get(code, "Unknown")
```

## 🏆 Key Takeaways
- Performance matters in tight loops; order your chains!
- Maps/Dictionaries can be cleaner than long `if-elif` blocks.
""",
        "questions": [
            {"text": "Why order conditions by probability?", "options": [
                {"text": "To reduce the number of checks on average (efficiency)", "correct": True},
                {"text": "It is required by PEP 8", "correct": False},
                {"text": "To make the code look better", "correct": False},
                {"text": "To avoid syntax errors", "correct": False}]},
        ],
        "challenge": {
            "title": "Day of the Week",
            "description": "Read an integer (1-7). Print the corresponding day ('Monday', 'Tuesday', etc.). If out of range, print 'Invalid'. Use a dictionary for mapping.",
            "initial_code": "days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}\n# Implement lookup\n",
            "solution_code": "days = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}\nn = int(input())\nprint(days.get(n, 'Invalid'))\n",
            "test_cases": [{"input": "1", "expected": "Monday"}, {"input": "5", "expected": "Friday"}, {"input": "8", "expected": "Invalid"}],
        },
    },

    "les-control-flow-2-pro": {
        "title": "Structural Pattern Matching (match/case)",
        "content": """# Structural Pattern Matching (match/case)

## 🎯 Learning Objectives
- Use the `match` and `case` keywords introduced in Python 3.10
- Distinguish between simple values and pattern matching
- Use 'Guards' in case statements

## 📚 Concept Overview
Python 3.10 introduced `match/case`, which is similar to `switch` in other languages but much more powerful.

```python
match status_code:
    case 200:
        print("Success")
    case 400 | 404: # Pipe for "or"
        print("Client Error")
    case 500:
        print("Server Error")
    case _: # Underscore for wildcard (catch-all)
        print("Other Error")
```

### Pattern Guards
```python
match x:
    case n if n > 0:
        print(f"Positive number: {n}")
    case 0:
        print("Zero")
```

## 🏆 Key Takeaways
- `match` is not just for values; it can match structures (lists, dicts).
- Use `_` as the default case.
- Available only in Python 3.10+.
""",
        "questions": [
            {"text": "Which Python version introduced `match/case`?", "options": [
                {"text": "3.10", "correct": True}, {"text": "3.8", "correct": False},
                {"text": "3.9", "correct": False}, {"text": "3.12", "correct": False}]},
            {"text": "What does the `_` (underscore) represent in a `match` block?", "options": [
                {"text": "A wildcard / default case", "correct": True}, {"text": "A required variable", "correct": False},
                {"text": "An error", "correct": False}, {"text": "A private value", "correct": False}]},
        ],
        "challenge": {
            "title": "Shape Describer",
            "description": "Read a string. Use match/case: 'circle' -> 'Round', 'square' -> 'Angular', anything else -> 'Unknown'.",
            "initial_code": "# Use match-case\n",
            "solution_code": "shape = input().strip().lower()\nmatch shape:\n    case 'circle':\n        print('Round')\n    case 'square':\n        print('Angular')\n    case _:\n        print('Unknown')\n",
            "test_cases": [{"input": "circle", "expected": "Round"}, {"input": "triangle", "expected": "Unknown"}],
        },
    },

    # ── Lesson 3: Logical Operators in Conditions ──────────────────────────────
    "les-control-flow-3-beginner": {
        "title": "Combining Conditions (and, or, not)",
        "content": """# Combining Conditions (and, or, not)

## 🎯 Learning Objectives
- Use `and`, `or`, and `not` to combine logic
- Understand short-circuit evaluation
- Handle complex requirements in a single `if` line

## 📚 Concept Overview
| Operator | Description | Result |
|----------|-------------|--------|
| `and` | Both must be True | True if both are True |
| `or` | Any one must be True | True if at least one is True |
| `not` | Invert logic | True if operand is False |

```python
age = 25
has_ticket = True

if age >= 18 and has_ticket:
    print("Welcome to the show!")
```

### Short-circuiting
Python skips the second part of an `and` if the first is False. It skips the second part of an `or` if the first is True.

## 🏆 Key Takeaways
- `and` / `or` make code more compact than nested `if`s.
- `not` is great for checking emptiness: `if not my_list:`.
""",
        "questions": [
            {"text": "If `X` is False, does Python check `Y` in the expression `X and Y`?", "options": [
                {"text": "No (Short-circuiting)", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only if X is an integer", "correct": False}, {"text": "Only in functions", "correct": False}]},
            {"text": "What is the result of `not (10 > 5)`?", "options": [
                {"text": "False", "correct": True}, {"text": "True", "correct": False},
                {"text": "None", "correct": False}, {"text": "Error", "correct": False}]},
        ],
        "challenge": {
            "title": "Access Control",
            "description": "Read an age and 'Yes'/'No' for parent permission. Print 'Access Granted' if age >= 13 OR permission is 'Yes', else 'Access Denied'.",
            "initial_code": "# Use boolean logic\n",
            "solution_code": "age = int(input())\nperm = input().strip()\nif age >= 13 or perm == 'Yes':\n    print('Access Granted')\nelse:\n    print('Access Denied')\n",
            "test_cases": [{"input": "12\nYes", "expected": "Access Granted"}, {"input": "12\nNo", "expected": "Access Denied"}, {"input": "15\nNo", "expected": "Access Granted"}],
        },
    },

    "les-control-flow-3-intermediate": {
        "title": "Truthiness and Falsiness",
        "content": """# Truthiness and Falsiness

## 🎯 Learning Objectives
- Learn that every Python object has a boolean value
- Write "Pythonic" conditions (e.g., `if items:` instead of `if len(items) > 0:`)
- Avoid common truth-checking bugs

## 📚 Concept Overview
In Python, you don't always need `<` or `==`. Objects themselves can be used in conditions.

### Falsy Values
- `None`
- `False`
- `0`, `0.0`
- `""` (empty string)
- `[]`, `{}`, `()` (empty collections)

Everything else is **Truthy**.

```python
names = []
if not names:
    print("The list is empty!")
```

## 🏆 Key Takeaways
- Use truthiness for cleaner, more idiomatic code.
- Be careful with `0` — it is falsy! `if x:` will fail even if `x` is zero.
""",
        "questions": [
            {"text": "Is the number `0` Truthy or Falsy?", "options": [
                {"text": "Falsy", "correct": True}, {"text": "Truthy", "correct": False},
                {"text": "Neither", "correct": False}, {"text": "It depends on context", "correct": False}]},
            {"text": "Which of these is a Pythonic way to check if a string `s` is not empty?", "options": [
                {"text": "if s:", "correct": True}, {"text": "if len(s) > 0:", "correct": False},
                {"text": "if s != '':", "correct": False}, {"text": "if bool(s) == True:", "correct": False}]},
        ],
        "challenge": {
            "title": "Content Filter",
            "description": "Read a string. If it is NOT empty, print 'Valid Content', otherwise print 'Empty'. Use truthiness.",
            "initial_code": "# Use truthiness logic\n",
            "solution_code": "text = input().strip()\nif text:\n    print('Valid Content')\nelse:\n    print('Empty')\n",
            "test_cases": [{"input": "Hello", "expected": "Valid Content"}, {"input": "", "expected": "Empty"}],
        },
    },

    "les-control-flow-3-pro": {
        "title": "De Morgan's Law & Logical Simplification",
        "content": """# De Morgan's Law & Logical Simplification

## 🎯 Learning Objectives
- Simplify complex boolean expressions
- Apply De Morgan's Laws to nested `not` conditions
- Write maintainable complex logic

## 📚 Concept Overview
De Morgan's Laws state:
1. `not (A and B)` is the same as `(not A) or (not B)`
2. `not (A or B)` is the same as `(not A) and (not B)`

### Why use it?
It helps turn complex, negated conditions into readable logic.

```python
# Harder to read:
if not (is_admin and active):
    print("Refused")

# Easier:
if not is_admin or not active:
    print("Refused")
```

## 🏆 Key Takeaways
- Distribute the `not` across brackets to simplify logic.
- Long logic lines should be broken up for clarity.
""",
        "questions": [
            {"text": "According to De Morgan's Law, `not (A or B)` is equal to:", "options": [
                {"text": "(not A) and (not B)", "correct": True}, {"text": "(not A) or (not B)", "correct": False},
                {"text": "not A not B", "correct": False}, {"text": "A and B", "correct": False}]},
        ],
        "challenge": {
            "title": "Logic Simplifier",
            "description": "Read A and B as 'True'/'False'. Print the result of `not (A and B)` using De Morgan's Law expression style.",
            "initial_code": "# Implement simplified logic\n",
            "solution_code": "a_str = input()\nb_str = input()\na = a_str == 'True'\nb = b_str == 'True'\n# not (A and B) => not A or not B\nprint(not a or not b)\n",
            "test_cases": [{"input": "True\nTrue", "expected": "False"}, {"input": "True\nFalse", "expected": "True"}],
        },
    },

    # ── Lesson 4: While Loops ──────────────────────────────────────────────
    "les-control-flow-4-beginner": {
        "title": "Into the While Loop",
        "content": """# Into the While Loop

## 🎯 Learning Objectives
- Create loops that run while a condition is True
- Use counter variables to control iterations
- Avoid the "Infinite Loop" trap

## 📚 Concept Overview
A `while` loop continues as long as its condition is True.

```python
count = 1
while count <= 5:
    print(count)
    count += 1
```

### The Infinite Loop
If the condition **never** becomes False, the loop runs forever!
```python
# WARNING: INFINITE LOOP
while True:
    print("Help!")
```

## ⚠️ Common Pitfalls
- Forgetting to update the counter (results in infinite loop).
- "Off-by-one" errors (looping 4 times when you meant 5).

## 🏆 Key Takeaways
- Use `while` when you don't know exactly how many times you'll need to repeat.
- Always ensure the loop has an "exit strategy".
""",
        "questions": [
            {"text": "When does a `while` loop stop?", "options": [
                {"text": "When its condition becomes False", "correct": True}, {"text": "After 10 times", "correct": False},
                {"text": "When you call stop()", "correct": False}, {"text": "When the program ends", "correct": False}]},
            {"text": "What happens in an infinite loop?", "options": [
                {"text": "The program runs forever and may hang", "correct": True}, {"text": "Python shuts down", "correct": False},
                {"text": "It runs 1,000,000 times then stops", "correct": False}, {"text": "It turns into a for loop", "correct": False}]},
        ],
        "challenge": {
            "title": "Count to N",
            "description": "Read an integer N. Using a while loop, print numbers from 1 up to N (inclusive) each on a new line.",
            "initial_code": "# Use while loop\n",
            "solution_code": "n = int(input())\nc = 1\nwhile c <= n:\n    print(c)\n    c += 1\n",
            "test_cases": [{"input": "3", "expected": "1\n2\n3"}, {"input": "1", "expected": "1"}],
        },
    },

    "les-control-flow-4-intermediate": {
        "title": "Sentinel Values & User Interaction",
        "content": """# Sentinel Values & User Interaction

## 🎯 Learning Objectives
- Use sentinel values to break out of loops
- Validate user input repeatedly
- Implement interactive menu systems

## 📚 Concept Overview
A **sentinel** is a special value that tells the loop to stop (like typing 'quit').

```python
user_input = ""
while user_input.lower() != "quit":
    user_input = input("Enter command: ")
    print(f"Executing {user_input}")
```

### Input Validation
```python
age = -1
while age < 0:
    age = int(input("Enter valid age: "))
```

## 🏆 Key Takeaways
- Sentinel loops are great for interactive CLI apps.
- `while True` combined with `break` is a common pattern for "loop once and check".
""",
        "questions": [
            {"text": "What is a 'sentinel value'?", "options": [
                {"text": "A value used to signal the end of a loop", "correct": True}, {"text": "The first value in a list", "correct": False},
                {"text": "A variable that counts iterations", "correct": False}, {"text": "A secret password", "correct": False}]},
        ],
        "challenge": {
            "title": "Sum Until Zero",
            "description": "Read integers one by one until the user enters 0. Print the sum of all numbers entered.",
            "initial_code": "total = 0\n# Loop until 0\n",
            "solution_code": "total = 0\nwhile True:\n    n = int(input())\n    if n == 0:\n        break\n    total += n\nprint(total)\n",
            "test_cases": [{"input": "10\n20\n0", "expected": "30"}, {"input": "0", "expected": "0"}],
        },
    },

    "les-control-flow-4-pro": {
        "title": "Complexity & Loop Invariants",
        "content": """# Complexity & Loop Invariants

## 🎯 Learning Objectives
- Analyze the time complexity (Big O) of while loops
- Understand Loop Invariants for formal verification
- Use `while` loops for efficient mathematical algorithms

## 📚 Concept Overview
### Efficiency
A while loop that splits the search space in half each time (like binary search) has **O(log N)** complexity.

### Binary Search Example
```python
low = 0
high = len(arr) - 1
while low <= high:
    mid = (low + high) // 2
    if arr[mid] == target:
        return mid
    # ... adjustment logic
```

## 🏆 Key Takeaways
- `while` is fundamental for algorithms where the space changes dynamically.
- Always evaluate how the condition changes to ensure progress.
""",
        "questions": [
            {"text": "What is the time complexity of a loop that halves the input every step?", "options": [
                {"text": "O(log N)", "correct": True}, {"text": "O(N)", "correct": False},
                {"text": "O(1)", "correct": False}, {"text": "O(N^2)", "correct": False}]},
        ],
        "challenge": {
            "title": "Power of Two",
            "description": "Read an integer N. Using a while loop, find the highest power of 2 that is less than or equal to N. Print that power.",
            "initial_code": "# Use while loop to find power of 2\n",
            "solution_code": "n = int(input())\np = 1\nwhile p * 2 <= n:\n    p *= 2\nprint(p)\n",
            "test_cases": [{"input": "31", "expected": "16"}, {"input": "8", "expected": "8"}, {"input": "1", "expected": "1"}],
        },
    },

    # ── Lesson 5: For Loops ──────────────────────────────────────────────
    "les-control-flow-5-beginner": {
        "title": "Mastering the For Loop",
        "content": """# Mastering the For Loop

## 🎯 Learning Objectives
- Iterate over sequences (lists, strings, tuples)
- Use `range()` to loop a specific number of times
- Grasp the 'variable in sequence' syntax

## 📚 Concept Overview
The `for` loop in Python is used to iterate over a sequence of items.

```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

### range() — The Number Generator
```python
# range(start, stop, step)
for i in range(5): # 0, 1, 2, 3, 4
    print(i)
```

## ⚠️ Common Pitfalls
- `range(5)` stops at 4, not 5.
- Modifying a list while you are looping through it can cause skipped items.

## 🏆 Key Takeaways
- Use `for` loops when you have a sequence or know exactly how many times to repeat.
- `range` is extremely memory efficient.
""",
        "questions": [
            {"text": "Which of these is used to iterate over a list in Python?", "options": [
                {"text": "for item in my_list:", "correct": True}, {"text": "foreach(my_list):", "correct": False},
                {"text": "while item in my_list:", "correct": False}, {"text": "loop my_list:", "correct": False}]},
            {"text": "What does `range(1, 4)` produce?", "options": [
                {"text": "1, 2, 3", "correct": True}, {"text": "1, 2, 3, 4", "correct": False},
                {"text": "0, 1, 2, 3, 4", "correct": False}, {"text": "1, 4", "correct": False}]},
        ],
        "challenge": {
            "title": "Square Numbers",
            "description": "Read an integer N. Print the squares of all numbers from 1 up to N (inclusive), each on a new line.",
            "initial_code": "# Use for loop and range\n",
            "solution_code": "n = int(input())\nfor i in range(1, n + 1):\n    print(i * i)\n",
            "test_cases": [{"input": "3", "expected": "1\n4\n9"}, {"input": "2", "expected": "1\n4"}],
        },
    },

    "les-control-flow-5-intermediate": {
        "title": "Iterating Sets & Dictionaries",
        "content": """# Iterating Sets & Dictionaries

## 🎯 Learning Objectives
- Loop through dictionary keys, values, and items
- Understand iteration order in Python 3.7+
- Use unpacking in for loops

## 📚 Concept Overview
### Dictionary Iteration
```python
data = {"A": 1, "B": 2}

# Just keys
for key in data: print(key)

# Keys and values
for key, value in data.items():
    print(f"{key} is {value}")
```

### Tuple Unpacking in Loops
```python
pairs = [(1, 'a'), (2, 'b')]
for num, char in pairs:
    print(num, char)
```

## 🏆 Key Takeaways
- `.items()` is the best way to get both key and value.
- Since Python 3.7, dictionary iteration follows insertion order.
""",
        "questions": [
            {"text": "Which method should you call on a dictionary to loop through both keys and values?", "options": [
                {"text": ".items()", "correct": True}, {"text": ".all()", "correct": False},
                {"text": ".values()", "correct": False}, {"text": ".keys()", "correct": False}]},
        ],
        "challenge": {
            "title": "Sum Dictionary",
            "description": "You are given a dictionary string representation (e.g., 'A=10 B=20'). Read N pairs like this and print the total sum of the numbers.",
            "initial_code": "# Use split() and a loop\n",
            "solution_code": "line = input().split()\ntotal = 0\nfor pair in line:\n    _, val = pair.split('=')\n    total += int(val)\nprint(total)\n",
            "test_cases": [{"input": "X=10 Y=20 Z=30", "expected": "60"}, {"input": "item=5", "expected": "5"}],
        },
    },

    "les-control-flow-5-pro": {
        "title": "Custom Iterators & Generators Intro",
        "content": """# Custom Iterators & Generators Intro

## 🎯 Learning Objectives
- Learn the Iterator Protocol (`__iter__` and `__next__`)
- Understand how `for` loops work under the hood
- Introduction to memory-efficient Generators

## 📚 Concept Overview
### The Iterator Protocol
When you write `for x in my_list:`, Python does this:
1. Calls `iter(my_list)` to get an iterator.
2. Calls `next(iterator)` repeatedly until `StopIteration` is raised.

### Why does this matter?
You can build objects that produce values on the fly without storing them in memory!

## 🏆 Key Takeaways
- `for` loops are syntactic sugar for the iterator protocol.
- Iterators allow for "Lazy Evaluation" (calculating values only when needed).
""",
        "questions": [
            {"text": "What exception is raised when an iterator has no more items?", "options": [
                {"text": "StopIteration", "correct": True}, {"text": "EndofLoop", "correct": False},
                {"text": "IndexError", "correct": False}, {"text": "FinishedError", "correct": False}]},
            {"text": "What are the two dunder methods required for the iterator protocol?", "options": [
                {"text": "__iter__ and __next__", "correct": True}, {"text": "__start__ and __end__", "correct": False},
                {"text": "__for__ and __in__", "correct": False}, {"text": "__list__ and __tuple__", "correct": False}]},
        ],
        "challenge": {
            "title": "Factorial Loop",
            "description": "Read an integer N. Calculate N! (factorial) using a for loop and range. Print the result.",
            "initial_code": "# Calculate factorial\n",
            "solution_code": "n = int(input())\nres = 1\nfor i in range(1, n + 1):\n    res *= i\nprint(res)\n",
            "test_cases": [{"input": "5", "expected": "120"}, {"input": "3", "expected": "6"}, {"input": "0", "expected": "1"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 3 (Control Flow) — Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 3 (1-5)"))
