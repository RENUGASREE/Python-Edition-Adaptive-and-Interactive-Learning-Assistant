"""python manage.py hydrate_module3_b -- Module 3 Control Flow Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: Range & Enumerate ──────────────────────────────────────────
    "les-control-flow-6-beginner": {
        "title": "Range & Enumerate Basics",
        "content": """# Range & Enumerate Basics

## 🎯 Learning Objectives
- Use `range()` to create sequence of numbers
- Use `enumerate()` to get both index and value in a loop
- Understand the benefits of these built-in functions

## 📚 Concept Overview
### range()
`range()` generates a sequence of numbers, which is very common in for-loops.

```python
# range(start, stop, step)
for i in range(1, 10, 2):
    print(i) # 1, 3, 5, 7, 9
```

### enumerate()
`enumerate()` adds a counter to an iterable and returns it as an enumerate object.

```python
fruits = ["apple", "banana", "cherry"]
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
```

## 🏆 Key Takeaways
- `range()` is memory efficient (it's a generator-like object).
- `enumerate()` is the Pythonic way to track the index in a loop.
""",
        "questions": [
            {"text": "What is the default start value for `range(5)`?", "options": [
                {"text": "0", "correct": True}, {"text": "1", "correct": False},
                {"text": "None", "correct": False}, {"text": "-1", "correct": False}]},
            {"text": "Which function allows you to get both index and value from a list?", "options": [
                {"text": "enumerate()", "correct": True}, {"text": "range()", "correct": False},
                {"text": "zip()", "correct": False}, {"text": "map()", "correct": False}]},
        ],
        "challenge": {
            "title": "Index Printer",
            "description": "Read a line of words. Print each word with its index in the format 'index: word'.",
            "initial_code": "# Use enumerate\n",
            "solution_code": "words = input().split()\nfor i, w in enumerate(words):\n    print(f'{i}: {w}')\n",
            "test_cases": [{"input": "python is fun", "expected": "0: python\n1: is\n2: fun"}],
        },
    },

    "les-control-flow-6-intermediate": {
        "title": "Reverse Range & Custom Starts",
        "content": """# Reverse Range & Custom Starts

## 🎯 Learning Objectives
- Loop backwards using `range()`
- Use custom start and step values
- Implement specialized iteration patterns

## 📚 Concept Overview
To loop backwards, you can use a negative step in `range()`.

```python
# Count down from 5 to 1
for i in range(5, 0, -1):
    print(i)
```

### enumerate(start=N)
You can choose a custom starting number for the enumerate index.
```python
fruits = ["apple", "banana"]
for count, fruit in enumerate(fruits, start=1):
    print(f"Item {count}: {fruit}")
```

## 🏆 Key Takeaways
- `range(stop)` stops AT the value (exclusive).
- `range(start, stop, -1)` lets you decrement.
""",
        "questions": [
            {"text": "How do you start an `enumerate` index from 1 instead of 0?", "options": [
                {"text": "enumerate(list, start=1)", "correct": True}, {"text": "enumerate(list, 1)", "correct": False},
                {"text": "enumerate(list)[1:]", "correct": False}, {"text": "It is not possible", "correct": False}]},
            {"text": "What does `range(5, 0, -1)` produce?", "options": [
                {"text": "5, 4, 3, 2, 1", "correct": True}, {"text": "5, 4, 3, 2, 1, 0", "correct": False},
                {"text": "0, 1, 2, 3, 4, 5", "correct": False}, {"text": "Error", "correct": False}]},
        ],
        "challenge": {
            "title": "Countdown",
            "description": "Read an integer N. Print a countdown from N down to 1 space-separated.",
            "initial_code": "# Use range for countdown\n",
            "solution_code": "n = int(input())\nres = [str(i) for i in range(n, 0, -1)]\nprint(' '.join(res))\n",
            "test_cases": [{"input": "5", "expected": "5 4 3 2 1"}],
        },
    },

    "les-control-flow-6-pro": {
        "title": "Range Internals & Step Optimization",
        "content": """# Range Internals & Step Optimization

## 🎯 Learning Objectives
- Understand that `range` is a sequence type, not a generator
- Analyze memory usage of large ranges
- Use constant time membership testing in ranges

## 📚 Concept Overview
Unlike generators, `range` objects in Python 3 support **O(1)** membership testing and indexing. They are lazy but they are sequences.

```python
r = range(0, 1000000, 2)
print(999998 in r) # O(1) - Fast!
print(r[5]) # O(1) - Fast!
```

Python calculates if a number *would* be in the range without iterating over it.

## 🏆 Key Takeaways
- `range` is an immutable sequence.
- It is much more powerful than a simple list of numbers or a standard generator.
""",
        "questions": [
            {"text": "Is `range` in Python 3 a generator?", "options": [
                {"text": "No, it is a separate immutable sequence type", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only for ranges larger than 1000", "correct": False}, {"text": "It is a list", "correct": False}]},
            {"text": "What is the time complexity of checking `x in range(1000000)`?", "options": [
                {"text": "O(1)", "correct": True}, {"text": "O(N)", "correct": False},
                {"text": "O(log N)", "correct": False}, {"text": "O(N log N)", "correct": False}]},
        ],
        "challenge": {
            "title": "Range Checker",
            "description": "Read A, B, C, and X. Print 'In Range' if X would be produced by `range(A, B, C)`, otherwise print 'Out'. (Don't build the list!)",
            "initial_code": "# Use efficiently\n",
            "solution_code": "a, b, c, x = map(int, input().split())\nr = range(a, b, c)\nprint('In Range' if x in r else 'Out')\n",
            "test_cases": [{"input": "0 10 2 4", "expected": "In Range"}, {"input": "0 10 2 5", "expected": "Out"}],
        },
    },

    # ── Lesson 7: Break, Continue, Pass ──────────────────────────────────────
    "les-control-flow-7-beginner": {
        "title": "Altering Loop Flow (Break & Continue)",
        "content": """# Altering Loop Flow (Break & Continue)

## 🎯 Learning Objectives
- Exit a loop early with `break`
- Skip the rest of an iteration with `continue`
- Use `pass` as a placeholder

## 📚 Concept Overview
| Keyword | Effect |
|---------|--------|
| `break` | Terminate the loop immediately |
| `continue` | Skip the current iteration and move to the next |
| `pass` | Do nothing (syntactic placeholder) |

```python
for i in range(10):
    if i == 5:
        break # Stops completely
    print(i)

for i in range(5):
    if i == 2:
        continue # Skips '2'
    print(i)
```

## 🏆 Key Takeaways
- `break` exits the **entire** loop.
- `continue` skips only the **current** turn.
- `pass` is useful when you need a block of code for syntax but haven't written the logic yet.
""",
        "questions": [
            {"text": "Which keyword skips just the current turn of a loop?", "options": [
                {"text": "continue", "correct": True}, {"text": "break", "correct": False},
                {"text": "pass", "correct": False}, {"text": "exit", "correct": False}]},
            {"text": "What does `pass` do in Python?", "options": [
                {"text": "Nothing at all", "correct": True}, {"text": "Increments the counter", "correct": False},
                {"text": "Exits the loop", "correct": False}, {"text": "Returns None", "correct": False}]},
        ],
        "challenge": {
            "title": "Selective Sum",
            "description": "Read integers one by one. Sum them up, but SKIP negative numbers. Stop and print the sum if you encounter the number 999.",
            "initial_code": "total = 0\n# Use continue and break\n",
            "solution_code": "total = 0\nwhile True:\n    n = int(input())\n    if n == 999:\n        break\n    if n < 0:\n        continue\n    total += n\nprint(total)\n",
            "test_cases": [{"input": "10\n-5\n20\n999", "expected": "30"}],
        },
    },

    "les-control-flow-7-intermediate": {
        "title": "Nested Control Flow",
        "content": """# Nested Control Flow

## 🎯 Learning Objectives
- Use `break` and `continue` inside nested loops
- Predict which loop is affected by which keyword
- Understand the scope of loop control

## 📚 Concept Overview
A `break` or `continue` only affects the **innermost** loop it is located in.

```python
for outer in range(3):
    print(f"Outer: {outer}")
    for inner in range(3):
        if inner == 1:
            break # ONLY breaks the inner loop
        print(f"  Inner: {inner}")
```

## ️🏆 Key Takeaways
- Be careful with nesting; it's easy to break the wrong loop.
- If you need to break all loops, you may need a flag variable or an exception.
""",
        "questions": [
            {"text": "In a nested loop, what does `break` do?", "options": [
                {"text": "Exits only the innermost loop", "correct": True}, {"text": "Exits all loops", "correct": False},
                {"text": "Exits the outermost loop", "correct": False}, {"text": "Moves to the next iteration of the outer loop", "correct": False}]},
        ],
        "challenge": {
            "title": "First Vowel",
            "description": "Read words one by one. For each word, print its first vowel. If a word has no vowels, skip it. If you read 'quit', stop everything.",
            "initial_code": "vowels = 'aeiou'\n# Nested loops with control\n",
            "solution_code": "vowels = 'aeiou'\nwhile True:\n    word = input().strip().lower()\n    if word == 'quit':\n        break\n    for char in word:\n        if char in vowels:\n            print(char)\n            break\n",
            "test_cases": [{"input": "sky\nhello\nquit", "expected": "e"}],
        },
    },

    "les-control-flow-7-pro": {
        "title": "The 'goto' controversy in Python",
        "content": """# The 'goto' controversy in Python

## 🎯 Learning Objectives
- Understand why Python does not have a native `goto`
- Explore legitimate use cases for non-linear control flow
- Learn about the `exception` pattern for multi-level break

## 📚 Concept Overview
Python purposely lacks a `goto` keyword to prevent "Spaghetti Code".

### The Multi-level Break Pattern
Instead of `goto`, Python developers use custom exceptions for deep exits.

```python
class BreakAllLoops(Exception): pass

try:
    for i in range(100):
        for j in range(100):
            if i * j > 2500:
                raise BreakAllLoops
except BreakAllLoops:
    print("Cleanly exited multiple levels")
```

## 🏆 Key Takeaways
- Structured control flow leads to safer code.
- Exceptions can act as a structured "long jump" if needed.
""",
        "questions": [
            {"text": "Does Python have a `goto` keyword?", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only in version 2", "correct": False}, {"text": "Only in the standard library", "correct": False}]},
            {"text": "What is a safe way to exit from deep nested loops in Python?", "options": [
                {"text": "Using a custom Exception", "correct": True}, {"text": "Using many break statements", "correct": False},
                {"text": "Calling exit()", "correct": False}, {"text": "restarting the computer", "correct": False}]},
        ],
        "challenge": {
            "title": "Matrix Search",
            "description": "Find if the number 7 appears in a 3x3 matrix (given as 3 lines of 3 numbers). If you find it, print 'Found' and STOP scanning. Otherwise print 'Not Found' at the very end.",
            "initial_code": "# Search for 7\n",
            "solution_code": "found = False\nfor _ in range(3):\n    row = list(map(int, input().split()))\n    if 7 in row:\n        found = True\n        break\nprint('Found' if found else 'Not Found')\n",
            "test_cases": [{"input": "1 2 3\n4 7 6\n8 9 0", "expected": "Found"}, {"input": "1 2 3\n4 5 6\n8 9 0", "expected": "Not Found"}],
        },
    },

    # ── Lesson 8: The Loop Else Clause ──────────────────────────────────────
    "les-control-flow-8-beginner": {
        "title": "The Else Clause in Loops",
        "content": """# The Else Clause in Loops

## 🎯 Learning Objectives
- Understand the unique Python `for...else` and `while...else` syntax
- Use `else` for search-and-verify logic
- Distinguish between a completion and a break

## 📚 Concept Overview
In Python, loops can have an `else` block. It runs **only if the loop completes normally** (without hitting a `break`).

```python
for i in range(5):
    print(i)
else:
    print("Loop finished successfully!")
```

If you `break`, the `else` is skipped.

```python
for i in range(5):
    if i == 3:
        break
else:
    print("You won't see this.")
```

## 🏆 Key Takeaways
- `else` in a loop means "no break occurred".
- It's perfect for scanning a list and only doing something if the item was **not** found.
""",
        "questions": [
            {"text": "When does the `else` block of a loop run?", "options": [
                {"text": "When the loop finishes without hitting a `break`", "correct": True}, {"text": "Every time the loop finishes", "correct": False},
                {"text": "When an error occurs", "correct": False}, {"text": "Only if the loop never runs at all", "correct": False}]},
        ],
        "challenge": {
            "title": "Prime Number Check",
            "description": "Read an integer N > 1. Using a `for...else` block, check if it's prime. Print 'Prime' or 'Not Prime'.",
            "initial_code": "# Check if N is prime\n",
            "solution_code": "n = int(input())\nfor i in range(2, int(n**0.5) + 1):\n    if n % i == 0:\n        print('Not Prime')\n        break\nelse:\n    print('Prime')\n",
            "test_cases": [{"input": "7", "expected": "Prime"}, {"input": "9", "expected": "Not Prime"}],
        },
    },

    "les-control-flow-8-intermediate": {
        "title": "Searching with for-else",
        "content": """# Searching with for-else

## 🎯 Learning Objectives
- Replace flag variables with the `else` clause
- Write cleaner look-up logic
- Apply `for-else` in real datasets

## 📚 Concept Overview
### Before (using flags):
```python
found = False
for x in data:
    if x == target:
        found = True
        break
if not found:
    print("Missing")
```

### After (Pythonic):
```python
for x in data:
    if x == target:
        break
else:
    print("Missing")
```

## 🏆 Key Takeaways
- The `else` clause eliminates the need for `found = True/False` manual tracking.
- It's a hallmark of high-quality Python code.
""",
        "questions": [
            {"text": "Which traditional coding pattern does the loop `else` replace?", "options": [
                {"text": "The Flag Variable pattern", "correct": True}, {"text": "The Infinite Loop pattern", "correct": False},
                {"text": "The Counter pattern", "correct": False}, {"text": "The Singleton pattern", "correct": False}]},
        ],
        "challenge": {
            "title": "Fruit Search",
            "description": "Read a list of fruits and a search term. If the fruit exists, print 'Available'. If the loop completes without finding it, print 'Out of Stock'. Use for-else.",
            "initial_code": "# Use for-else\n",
            "solution_code": "fruits = input().split()\ntarget = input().strip()\nfor f in fruits:\n    if f == target:\n        print('Available')\n        break\nelse:\n    print('Out of Stock')\n",
            "test_cases": [{"input": "apple banana cherry\nbanana", "expected": "Available"}, {"input": "apple banana\ncherry", "expected": "Out of Stock"}],
        },
    },

    "les-control-flow-8-pro": {
        "title": "Logic Paradox of For-Else",
        "content": """# Logic Paradox of For-Else

## 🎯 Learning Objectives
- Discuss the readability controversies around `for...else`
- Explore how other languages solve this problem
- Learn how to structure code so the `else` logic is intuitive

## 📚 Concept Overview
Many developers find `for...else` confusing because `else` usually means "or else" (binary choice). In loops, it basically means "then" (completion).

### Suggested Mental Map:
Think of the loop `else` as **the "Completion" block**.

## 🏆 Key Takeaways
- Some argue that `for...else` is less readable than flags for beginners.
- Only use it when it clearly simplifies the logic of a search.
""",
        "questions": [
            {"text": "Why do some developers avoid `for...else`?", "options": [
                {"text": "They find the name 'else' confusing for completion", "correct": True}, {"text": "It is slow", "correct": False},
                {"text": "It breaks the debugger", "correct": False}, {"text": "It is being removed in 4.0", "correct": False}]},
        ],
        "challenge": {
            "title": "Divisibility Watcher",
            "description": "Read a number N. Check numbers from 2 up to N-1. If any divide N, print 'Has Divisor' AND STOP. If none divide N, print 'No Divisors'. Use for-else.",
            "initial_code": "# Implement for-else\n",
            "solution_code": "n = int(input())\nfor i in range(2, n):\n    if n % i == 0:\n        print('Has Divisor')\n        break\nelse:\n    print('No Divisors')\n",
            "test_cases": [{"input": "15", "expected": "Has Divisor"}, {"input": "7", "expected": "No Divisors"}],
        },
    },

    # ── Lesson 9: Truthiness in Control Flow ─────────────────────────────────
    "les-control-flow-9-beginner": {
        "title": "Boolean Logic and Control",
        "content": """# Boolean Logic and Control

## 🎯 Learning Objectives
- Learn about the `bool` type in detail
- Understand truth tables for multi-step logic
- Apply complex boolean conditions to control flow

## 📚 Concept Overview
In many programs, the decision to run code depends on a complex web of conditions.

```python
is_weekend = True
is_holiday = False
weather_ok = True

if (is_weekend or is_holiday) and weather_ok:
    print("Let's go hiking!")
```

## 🏆 Key Takeaways
- Parentheses `()` are vital to ensure the order of operations in logic.
- `or` has lower precedence than `and`.
""",
        "questions": [
            {"text": "Which logical operator is evaluated first if no parentheses are used?", "options": [
                {"text": "and", "correct": True}, {"text": "or", "correct": False},
                {"text": "not", "correct": False}, {"text": "They are level", "correct": False}]},
        ],
        "challenge": {
            "title": "Complex Permission",
            "description": "Read: age, is_vip ('True'/'False'), and has_ticket ('True'/'False'). Return 'Allowed' if (age >= 18 OR is_vip) AND has_ticket.",
            "initial_code": "# Use complex logic\n",
            "solution_code": "age = int(input())\nvip = input() == 'True'\nticket = input() == 'True'\nif (age >= 18 or vip) and ticket:\n    print('Allowed')\nelse:\n    print('Denied')\n",
            "test_cases": [{"input": "15\nTrue\nTrue", "expected": "Allowed"}, {"input": "20\nFalse\nFalse", "expected": "Denied"}],
        },
    },

    "les-control-flow-9-intermediate": {
        "title": "Optimization with Laziness",
        "content": """# Optimization with Laziness

## 🎯 Learning Objectives
- Master the `any()` and `all()` built-in functions
- Use lazy generators for massive performance gains
- Write code that processes data only when needed

## 📚 Concept Overview
### any() vs all()
- `any(list)`: True if ONE item is True.
- `all(list)`: True if ALL items are True.

```python
results = [True, True, False]
print(any(results)) # True
print(all(results)) # False
```

### Lazy processing
```python
# Stops as soon as it finds a hit!
if any(is_prime(n) for n in large_list):
    print("Found a prime")
```

## 🏆 Key Takeaways
- `any()` and `all()` are much cleaner than manual for-loops.
- Using them with generator expressions makes them "Lazy" (efficient).
""",
        "questions": [
            {"text": "What does `any([False, False, True])` return?", "options": [
                {"text": "True", "correct": True}, {"text": "False", "correct": False},
                {"text": "Error", "correct": False}, {"text": "None", "correct": False}]},
            {"text": "What does `all([])` (empty list) return in Python?", "options": [
                {"text": "True (Vacuous Truth)", "correct": True}, {"text": "False", "correct": False},
                {"text": "Error", "correct": False}, {"text": "None", "correct": False}]},
        ],
        "challenge": {
            "title": "Security Check",
            "description": "Read a sentence. Print 'Safe' if all words are shorter than 10 characters, else 'Warning'. Use all().",
            "initial_code": "# Use all()\n",
            "solution_code": "words = input().split()\nif all(len(w) < 10 for w in words):\n    print('Safe')\nelse:\n    print('Warning')\n",
            "test_cases": [{"input": "python is a wonderful language", "expected": "Safe"}, {"input": "thisisalongwordtocheck", "expected": "Warning"}],
        },
    },

    "les-control-flow-9-pro": {
        "title": "Truthiness of Custom Objects (__bool__)",
        "content": """# Truthiness of Custom Objects (__bool__)

## 🎯 Learning Objectives
- Customize the truth value of your own classes
- Use `__bool__` and `__len__` dunders
- Understand how Python decides if an object is "True"

## 📚 Concept Overview
You can control how your objects behave in an `if` statement.

```python
class MyContainer:
    def __init__(self, data):
        self.data = data
    def __bool__(self):
        return len(self.data) > 0

c = MyContainer([])
if not c:
    print("Container is considered empty")
```

If `__bool__` is not defined, Python looks for `__len__`. If neither exist, the object is always True.

## 🏆 Key Takeaways
- `__bool__` allows you to define "Emptiness" for your domain objects.
- It is better to use truthiness than manual checks.
""",
        "questions": [
            {"text": "Which dunder method determines the boolean value of an object?", "options": [
                {"text": "__bool__", "correct": True}, {"text": "__true__", "correct": False},
                {"text": "__logical__", "correct": False}, {"text": "__check__", "correct": False}]},
            {"text": "What happens if a class has no `__bool__` but has `__len__`?", "options": [
                {"text": "Python uses __len__ > 0 as the truth value", "correct": True}, {"text": "The object is always True", "correct": False},
                {"text": "An error is raised", "correct": False}, {"text": "The object is always False", "correct": False}]},
        ],
        "challenge": {
            "title": "Custom Truth",
            "description": "Read a string. Create a class that stores this string. Implement `__bool__` so it returns True if the string is exactly 'SECRET'. Print if the object is True/False for the given input.",
            "initial_code": "# Implement __bool__\n",
            "solution_code": "class Sec:\n    def __init__(self, s): self.s = s\n    def __bool__(self): return self.s == 'SECRET'\n\nobj = Sec(input().strip())\nprint(bool(obj))\n",
            "test_cases": [{"input": "SECRET", "expected": "True"}, {"input": "NOPE", "expected": "False"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-control-flow-10-beginner": {
        "title": "Project: Guess the Number",
        "content": """# Project: Guess the Number

## 🎯 Goal
Create an interactive game where the user guesses a secret number.

## 📝 Features
- Repeat until the user gets it right.
- Give "Higher" or "Lower" hints.
- Count the number of attempts.

```python
secret = 42
guess = -1
while guess != secret:
    guess = int(input("Guess: "))
    if guess < secret: print("Higher")
    elif guess > secret: print("Lower")
print("Win!")
```
""",
        "questions": [
            {"text": "Which loop is best for a game where the number of turns is unknown?", "options": [
                {"text": "while", "correct": True}, {"text": "for", "correct": False},
                {"text": "if", "correct": False}, {"text": "foreach", "correct": False}]},
        ],
        "challenge": {
            "title": "Hint Bot",
            "description": "Read a secret number and a guess. Print 'Higher', 'Lower', or 'Correct'.",
            "initial_code": "# Base logic\n",
            "solution_code": "s = int(input())\ng = int(input())\nif g < s: print('Higher')\nelif g > s: print('Lower')\nelse: print('Correct')\n",
            "test_cases": [{"input": "50\n25", "expected": "Higher"}, {"input": "50\n75", "expected": "Lower"}, {"input": "50\n50", "expected": "Correct"}],
        },
    },

    "les-control-flow-10-intermediate": {
        "title": "Project: Command-Line Menu",
        "content": """# Project: Command-Line Menu

## 🎯 Goal
Build a logic-driven menu system for a CLI application.

## 📝 Features
- Support commands like LIST, ADD, DELETE, and QUIT.
- Use `match/case` or `if/elif` for command processing.
- Handle invalid commands gracefully.
""",
        "questions": [],
        "challenge": {
            "title": "Menu Logic",
            "description": "Read commands one per line. 'add X' -> print 'Added X', 'list' -> print 'Listing...', 'exit' -> print 'Goodbye' and STOP. Ignore anything else.",
            "initial_code": "# Menu loop\n",
            "solution_code": "while True:\n    cmd = input().split()\n    if not cmd: continue\n    if cmd[0] == 'add': print(f'Added {cmd[1]}')\n    elif cmd[0] == 'list': print('Listing...')\n    elif cmd[0] == 'exit':\n        print('Goodbye')\n        break\n",
            "test_cases": [{"input": "add Apple\nlist\nexit", "expected": "Added Apple\nListing...\nGoodbye"}],
        },
    },

    "les-control-flow-10-pro": {
        "title": "Project: Simple Interpreter",
        "content": """# Project: Simple Interpreter

## 🎯 Goal
Build a tiny command interpreter that supports mathematical operations.

## 📝 Features
- Parse "ADD num" or "SUB num" commands.
- Maintain a running state.
- Exit on "END".
""",
        "questions": [],
        "challenge": {
            "title": "Stateful Bot",
            "description": "Start with total = 0. Read commands: 'add X', 'sub X', 'mul X'. On 'end', print total and stop.",
            "initial_code": "total = 0\n# Logic here\n",
            "solution_code": "total = 0\nwhile True:\n    try:\n        line = input().split()\n        if not line: continue\n        if line[0] == 'end':\n            print(total)\n            break\n        cmd = line[0]\n        val = int(line[1])\n        if cmd == 'add': total += val\n        elif cmd == 'sub': total -= val\n        elif cmd == 'mul': total *= val\n    except EOFError:\n        break\n",
            "test_cases": [{"input": "add 10\nmul 3\nsub 5\nend", "expected": "25"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 3 (Control Flow) — Lessons 6-10"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 3 (6-10)"))
