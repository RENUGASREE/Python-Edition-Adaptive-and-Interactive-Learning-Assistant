"""
Management command: python manage.py hydrate_module1_extra
Adds lessons 3-10 for Module 1 (Python Basics).
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 3: Strings ────────────────────────────────────────────────────
    "les-python-basics-3-beginner": {
        "title": "String Basics — Working with Text",
        "content": """# String Basics — Working with Text

## 🎯 Learning Objectives
- Create and manipulate strings in Python
- Use indexing and slicing to access characters
- Apply common string methods

## 📚 Concept Overview
A **string** is a sequence of characters enclosed in quotes.
Strings are **immutable** — you cannot change characters in place.

```python
s = "Python"
print(s[0])    # P  (indexing starts at 0)
print(s[-1])   # n  (negative index = from end)
print(s[1:4])  # yth (slicing: start:stop, stop excluded)
```

### Common String Methods
| Method | Description |
|--------|-------------|
| `.upper()` | Converts to uppercase |
| `.lower()` | Converts to lowercase |
| `.strip()` | Removes leading/trailing whitespace |
| `.replace(old, new)` | Replaces substring |
| `.split(sep)` | Splits into a list |
| `.len()` | Use `len(s)` — it's a function, not method |

## 💻 Code Walkthrough
```python
name = "  alice  "
print(name.strip())         # alice
print(name.strip().title()) # Alice
print("hello".upper())      # HELLO
print("Hello World".split()) # ['Hello', 'World']
```

## ⚠️ Common Pitfalls
- `s[0] = "A"` raises `TypeError` — strings are immutable
- `len` is a built-in function: `len(s)` not `s.len()`

## 🏆 Key Takeaways
- Strings support indexing `[i]`, slicing `[start:stop:step]`
- Strings are immutable; methods return new strings
- Use `.strip()` to sanitize user input
""",
        "questions": [
            {"text": "What does `'Python'[0]` return?", "options": [
                {"text": "P", "correct": True}, {"text": "y", "correct": False},
                {"text": "Python", "correct": False}, {"text": "0", "correct": False}]},
            {"text": "What does `'hello'.upper()` return?", "options": [
                {"text": "HELLO", "correct": True}, {"text": "Hello", "correct": False},
                {"text": "hello", "correct": False}, {"text": "hELLO", "correct": False}]},
            {"text": "Which function returns the length of a string?", "options": [
                {"text": "len()", "correct": True}, {"text": ".length()", "correct": False},
                {"text": ".size()", "correct": False}, {"text": "count()", "correct": False}]},
        ],
        "challenge": {
            "title": "Reverse and Uppercase",
            "description": "Read a string. Print it reversed and in uppercase.",
            "initial_code": "# Read a string, print reversed uppercase version\n",
            "solution_code": "s = input()\nprint(s[::-1].upper())\n",
            "test_cases": [{"input": "hello", "expected": "OLLEH"}, {"input": "python", "expected": "NOHTYP"}],
        },
    },

    "les-python-basics-3-intermediate": {
        "title": "String Methods, Formatting & Regex Intro",
        "content": """# String Methods, Formatting & Regex Intro

## 🎯 Learning Objectives
- Master advanced string methods (join, find, count, startswith)
- Compare .format(), f-strings, and % formatting
- Use basic regex with the `re` module

## 📚 Concept Overview
### String Formatting Comparison
```python
name, score = "Alice", 98

# %-style (legacy)
print("Name: %s, Score: %d" % (name, score))

# .format() (Python 3.0+)
print("Name: {}, Score: {}".format(name, score))

# f-string (Python 3.6+ — preferred)
print(f"Name: {name}, Score: {score}")
print(f"Score: {score:.2f}")  # format spec
```

### Regex Basics
```python
import re

email = "user@example.com"
pattern = r"[\\w.]+@[\\w.]+\\.[a-z]{2,}"
if re.match(pattern, email):
    print("Valid email")

# Find all numbers in a string
text = "I have 3 cats and 12 dogs"
nums = re.findall(r"\\d+", text)  # ['3', '12']
```

## ⚠️ Common Pitfalls
- f-strings evaluate expressions immediately — `f"{x}"` uses x's current value
- Regex patterns need raw strings `r"..."` to avoid backslash escaping issues

## 🏆 Key Takeaways
- f-strings are the fastest and most readable formatting option
- `re.findall` returns all matches; `re.match` checks from the start
""",
        "questions": [
            {"text": "Which string formatting method is preferred in Python 3.6+?", "options": [
                {"text": "f-strings", "correct": True}, {"text": "%-style", "correct": False},
                {"text": ".format()", "correct": False}, {"text": "template strings", "correct": False}]},
            {"text": "What does `re.findall(r'\\d+', 'I have 3 cats')` return?", "options": [
                {"text": "['3']", "correct": True}, {"text": "['I', 'have', 'cats']", "correct": False},
                {"text": "3", "correct": False}, {"text": "None", "correct": False}]},
            {"text": "Why use raw strings `r'...'` in regex?", "options": [
                {"text": "To avoid Python processing backslashes before regex sees them", "correct": True},
                {"text": "To make strings immutable", "correct": False},
                {"text": "To improve performance", "correct": False},
                {"text": "It has no special meaning", "correct": False}]},
        ],
        "challenge": {
            "title": "Word Counter",
            "description": "Read a sentence. Print the number of words it contains.",
            "initial_code": "# Read a sentence and count its words\n",
            "solution_code": "s = input()\nprint(len(s.split()))\n",
            "test_cases": [{"input": "Hello World from Python", "expected": "4"}],
        },
    },

    "les-python-basics-3-pro": {
        "title": "String Internals, Unicode & Custom String Protocol",
        "content": """# String Internals, Unicode & Custom String Protocol

## 🎯 Learning Objectives
- Understand CPython's string memory optimization (PEP 393)
- Work correctly with Unicode and encoding/decoding
- Implement `__str__` and `__repr__` in custom classes

## 📚 Concept Overview
### CPython Compact String Representation (PEP 393)
Strings in CPython use different internal layouts based on their content:
- **Latin-1** (1 byte/char) for ASCII-only strings
- **UCS-2** (2 bytes/char) for BMP Unicode
- **UCS-4** (4 bytes/char) for full Unicode

This saves memory — the internal kind is chosen automatically.

### Unicode & Encoding
```python
s = "café"
encoded = s.encode("utf-8")   # b'caf\\xc3\\xa9'
decoded = encoded.decode("utf-8")  # café

# Check codepoints
for ch in "café":
    print(f"{ch} → U+{ord(ch):04X}")
```

### Custom __str__ and __repr__
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"   # for devs
    def __str__(self):
        return f"({self.x}, {self.y})"          # for users

v = Vector(3, 4)
print(v)       # (3, 4)
print(repr(v)) # Vector(3, 4)
```

## 🏆 Key Takeaways
- Python 3 strings are Unicode by default; use `.encode()` / `.decode()` for bytes
- `__repr__` should be unambiguous (used in REPL); `__str__` should be human-readable
- CPython optimizes string memory automatically based on character range
""",
        "questions": [
            {"text": "What encoding does `'café'.encode('utf-8')` use?", "options": [
                {"text": "UTF-8", "correct": True}, {"text": "ASCII", "correct": False},
                {"text": "Latin-1", "correct": False}, {"text": "UTF-16", "correct": False}]},
            {"text": "What is the purpose of `__repr__`?", "options": [
                {"text": "Provide an unambiguous developer-friendly representation", "correct": True},
                {"text": "Print a message on screen", "correct": False},
                {"text": "Encode the object to bytes", "correct": False},
                {"text": "Compare two objects", "correct": False}]},
            {"text": "What does `ord('A')` return?", "options": [
                {"text": "65", "correct": True}, {"text": "A", "correct": False},
                {"text": "0x41 as string", "correct": False}, {"text": "1", "correct": False}]},
        ],
        "challenge": {
            "title": "Encode and Count",
            "description": "Read a string. Print the number of bytes it takes when encoded in UTF-8.",
            "initial_code": "# Read string, encode to UTF-8, print byte count\n",
            "solution_code": "s = input()\nprint(len(s.encode('utf-8')))\n",
            "test_cases": [{"input": "hello", "expected": "5"}, {"input": "café", "expected": "5"}],
        },
    },

    # ── Lesson 4: Numbers & Math ─────────────────────────────────────────────
    "les-python-basics-4-beginner": {
        "title": "Numbers & Math Operators",
        "content": """# Numbers & Math Operators

## 🎯 Learning Objectives
- Work with integers and floats in Python
- Use arithmetic operators including floor division and modulo
- Understand operator precedence

## 📚 Concept Overview
Python has three numeric types: `int`, `float`, and `complex`.

### Arithmetic Operators
| Operator | Name | Example | Result |
|----------|------|---------|--------|
| `+` | Addition | `5 + 3` | `8` |
| `-` | Subtraction | `5 - 3` | `2` |
| `*` | Multiplication | `5 * 3` | `15` |
| `/` | Division | `7 / 2` | `3.5` |
| `//` | Floor Division | `7 // 2` | `3` |
| `%` | Modulo (remainder) | `7 % 2` | `1` |
| `**` | Exponentiation | `2 ** 8` | `256` |

### Operator Precedence (PEMDAS)
`**` → `*`, `/`, `//`, `%` → `+`, `-`

## 💻 Code Walkthrough
```python
print(10 / 3)    # 3.3333...  (float division)
print(10 // 3)   # 3          (floor division)
print(10 % 3)    # 1          (remainder)
print(2 ** 10)   # 1024       (exponent)

# abs and round
print(abs(-42))      # 42
print(round(3.567, 2))  # 3.57
```

## ⚠️ Common Pitfalls
- `7 / 2` gives `3.5` in Python 3 (use `//` for integer division)
- Floating point imprecision: `0.1 + 0.2 != 0.3` — use `round()` or `decimal` module

## 🏆 Key Takeaways
- Use `//` for integer (floor) division, `/` for float division
- `%` (modulo) is great for checking divisibility: `n % 2 == 0` means n is even
- Python integers have **unlimited precision** — no integer overflow
""",
        "questions": [
            {"text": "What does `10 // 3` evaluate to?", "options": [
                {"text": "3", "correct": True}, {"text": "3.33", "correct": False},
                {"text": "4", "correct": False}, {"text": "1", "correct": False}]},
            {"text": "What operator is used for exponentiation in Python?", "options": [
                {"text": "**", "correct": True}, {"text": "^", "correct": False},
                {"text": "exp()", "correct": False}, {"text": "pow", "correct": False}]},
            {"text": "What does `7 % 3` return?", "options": [
                {"text": "1", "correct": True}, {"text": "2", "correct": False},
                {"text": "0", "correct": False}, {"text": "3", "correct": False}]},
        ],
        "challenge": {
            "title": "Digit Sum",
            "description": "Read an integer N. Print the sum of its digits.",
            "initial_code": "# Read N and print sum of its digits\n",
            "solution_code": "n = int(input())\nprint(sum(int(d) for d in str(abs(n))))\n",
            "test_cases": [{"input": "123", "expected": "6"}, {"input": "9999", "expected": "36"}],
        },
    },

    "les-python-basics-4-intermediate": {
        "title": "Numeric Precision, math Module & Bitwise Ops",
        "content": """# Numeric Precision, math Module & Bitwise Ops

## 🎯 Learning Objectives
- Use the `math` module for advanced calculations
- Work with bitwise operators
- Handle floating-point precision with `decimal`

## 📚 Concept Overview
### The math Module
```python
import math
print(math.sqrt(144))    # 12.0
print(math.floor(3.9))   # 3
print(math.ceil(3.1))    # 4
print(math.pi)           # 3.14159...
print(math.log(100, 10)) # 2.0
```

### Bitwise Operators
| Op | Name | Example | Result |
|----|------|---------|--------|
| `&` | AND | `5 & 3` | `1` |
| `|` | OR | `5 | 3` | `7` |
| `^` | XOR | `5 ^ 3` | `6` |
| `~` | NOT | `~5` | `-6` |
| `<<` | Left shift | `1 << 3` | `8` |
| `>>` | Right shift | `8 >> 2` | `2` |

### Decimal Precision
```python
from decimal import Decimal
print(0.1 + 0.2)               # 0.30000000000000004
print(Decimal("0.1") + Decimal("0.2"))  # 0.3
```

## 🏆 Key Takeaways
- Use `math` for sqrt, trig, log, floor, ceil
- Bitwise operations work on the binary representation of integers
- Use `decimal.Decimal` for financial or precision-critical calculations
""",
        "questions": [
            {"text": "What does `math.ceil(3.1)` return?", "options": [
                {"text": "4", "correct": True}, {"text": "3", "correct": False},
                {"text": "3.1", "correct": False}, {"text": "3.0", "correct": False}]},
            {"text": "What is `5 & 3` in binary?", "options": [
                {"text": "1", "correct": True}, {"text": "7", "correct": False},
                {"text": "15", "correct": False}, {"text": "0", "correct": False}]},
            {"text": "Which module provides Decimal for precise arithmetic?", "options": [
                {"text": "decimal", "correct": True}, {"text": "math", "correct": False},
                {"text": "numbers", "correct": False}, {"text": "fractions", "correct": False}]},
        ],
        "challenge": {
            "title": "Power of Two Checker",
            "description": "Read an integer N. Print 'Yes' if N is a power of 2, else 'No'. Hint: use bitwise AND.",
            "initial_code": "# Use bitwise trick: N & (N-1) == 0 for powers of 2\n",
            "solution_code": "n = int(input())\nprint('Yes' if n > 0 and (n & (n - 1)) == 0 else 'No')\n",
            "test_cases": [{"input": "8", "expected": "Yes"}, {"input": "10", "expected": "No"}],
        },
    },

    "les-python-basics-4-pro": {
        "title": "Numeric Tower, Arbitrary Precision & Complex Numbers",
        "content": """# Numeric Tower, Arbitrary Precision & Complex Numbers

## 🎯 Learning Objectives
- Understand Python's numeric tower (numbers ABC hierarchy)
- Use fractions and complex numbers correctly
- Implement custom numeric types

## 📚 Concept Overview
### Python's Numeric Tower (PEP 3141)
```
Complex > Real > Rational > Integral
```
```python
from numbers import Complex, Real, Rational, Integral
isinstance(42, Integral)   # True
isinstance(3.14, Real)     # True
isinstance(1+2j, Complex)  # True
```

### Arbitrary Precision Integers
Python `int` is arbitrary-precision (no overflow):
```python
print(2 ** 1000)  # exact — a 302-digit number!
```

### Fractions
```python
from fractions import Fraction
f = Fraction(1, 3) + Fraction(1, 6)
print(f)   # 1/2  (exact, no floating error)
```

### Complex Numbers
```python
z = 3 + 4j
print(abs(z))      # 5.0  (magnitude)
print(z.real)      # 3.0
print(z.conjugate()) # (3-4j)
```

## 🏆 Key Takeaways
- Python's numeric tower uses ABCs for duck-typed numeric programming
- `fractions.Fraction` provides exact rational arithmetic
- Python integers never overflow — they grow automatically
""",
        "questions": [
            {"text": "What does `Fraction(1,3) + Fraction(1,6)` return exactly?", "options": [
                {"text": "Fraction(1, 2)", "correct": True}, {"text": "0.5", "correct": False},
                {"text": "Fraction(2, 9)", "correct": False}, {"text": "0.333", "correct": False}]},
            {"text": "What is `abs(3 + 4j)`?", "options": [
                {"text": "5.0", "correct": True}, {"text": "7.0", "correct": False},
                {"text": "1.0", "correct": False}, {"text": "12.0", "correct": False}]},
            {"text": "Which numeric ABC is at the base (most general) of Python's numeric tower?", "options": [
                {"text": "Complex", "correct": True}, {"text": "Integral", "correct": False},
                {"text": "Real", "correct": False}, {"text": "Number", "correct": False}]},
        ],
        "challenge": {
            "title": "Fraction Calculator",
            "description": "Read two fractions as 'a/b' format on separate lines. Print their sum as a fraction.",
            "initial_code": "from fractions import Fraction\n# Read two fractions, print their sum\n",
            "solution_code": "from fractions import Fraction\na = Fraction(input().strip())\nb = Fraction(input().strip())\nprint(a + b)\n",
            "test_cases": [{"input": "1/3\n1/6", "expected": "1/2"}, {"input": "1/4\n1/4", "expected": "1/2"}],
        },
    },

    # ── Lesson 5: User Input ─────────────────────────────────────────────────
    "les-python-basics-5-beginner": {
        "title": "User Input & Type Conversion",
        "content": """# User Input & Type Conversion

## 🎯 Learning Objectives
- Read user input with `input()`
- Convert strings to numbers with `int()` and `float()`
- Handle basic input validation

## 📚 Concept Overview
`input()` **always returns a string**, even if the user types a number.
You must explicitly convert it to the type you need.

```python
name = input("Enter your name: ")   # always a str
age = int(input("Enter your age: "))  # convert to int
price = float(input("Enter price: ")) # convert to float
```

### Type Conversion (Casting) Functions
| Function | Description |
|----------|-------------|
| `int(x)` | String/float → integer |
| `float(x)` | String/int → float |
| `str(x)` | Anything → string |
| `bool(x)` | Anything → True/False |

## 💻 Code Walkthrough
```python
x = input()          # "42"  (string)
n = int(x)           # 42   (integer)
f = float(x)         # 42.0 (float)
s = str(n)           # "42"  (string again)
print(n + 8)         # 50
print("Age: " + s)   # Age: 42
```

## ⚠️ Common Pitfalls
- `int("3.5")` raises `ValueError` — use `int(float("3.5"))` instead
- Forgetting to convert: `input() + 5` raises `TypeError`

## 🏆 Key Takeaways
- `input()` always returns a string
- Use `int()`, `float()` to convert before arithmetic
- Wrap conversions in `try/except` to handle invalid input gracefully
""",
        "questions": [
            {"text": "What type does `input()` always return?", "options": [
                {"text": "str", "correct": True}, {"text": "int", "correct": False},
                {"text": "float", "correct": False}, {"text": "depends on what user types", "correct": False}]},
            {"text": "How do you convert the string '42' to an integer?", "options": [
                {"text": "int('42')", "correct": True}, {"text": "str(42)", "correct": False},
                {"text": "'42'.toInt()", "correct": False}, {"text": "integer('42')", "correct": False}]},
            {"text": "What happens if you run `int('3.5')`?", "options": [
                {"text": "Raises ValueError", "correct": True}, {"text": "Returns 3", "correct": False},
                {"text": "Returns 3.5", "correct": False}, {"text": "Returns '3'", "correct": False}]},
        ],
        "challenge": {
            "title": "BMI Calculator",
            "description": "Read weight (kg) as float and height (m) as float on separate lines. Print BMI rounded to 2 decimal places. BMI = weight / (height ** 2).",
            "initial_code": "# Read weight and height, compute and print BMI\n",
            "solution_code": "w = float(input())\nh = float(input())\nprint(round(w / h**2, 2))\n",
            "test_cases": [{"input": "70\n1.75", "expected": "22.86"}],
        },
    },

    "les-python-basics-5-intermediate": {
        "title": "Input Validation, Error Handling & Multiple Inputs",
        "content": """# Input Validation, Error Handling & Multiple Inputs

## 🎯 Learning Objectives
- Validate user input using try/except
- Parse multiple values from a single line
- Use `sys.stdin` for reading multiple lines efficiently

## 📚 Concept Overview
### Robust Input with try/except
```python
while True:
    try:
        n = int(input("Enter a number: "))
        break
    except ValueError:
        print("Please enter a valid integer.")
```

### Multiple Values on One Line
```python
# Read "3 4 5" as three ints
a, b, c = map(int, input().split())
# Read a list of N integers
nums = list(map(int, input().split()))
```

### Reading from stdin efficiently
```python
import sys
data = sys.stdin.read().split()
n = int(data[0])
nums = list(map(int, data[1:n+1]))
```

## ⚠️ Common Pitfalls
- `input().split()` returns strings — always `map(int, ...)` for numbers
- Competitive programming inputs often have all data on one read

## 🏆 Key Takeaways
- Use `try/except ValueError` for safe numeric input parsing
- `map(int, input().split())` is the idiomatic way to read multiple ints
- `sys.stdin.read()` is faster for large inputs
""",
        "questions": [
            {"text": "How do you read two integers from a single line '3 7'?", "options": [
                {"text": "a, b = map(int, input().split())", "correct": True},
                {"text": "a = int(input()); b = int(input())", "correct": False},
                {"text": "a, b = input().split()", "correct": False},
                {"text": "a, b = input(int)", "correct": False}]},
            {"text": "Which exception is raised when `int('abc')` is called?", "options": [
                {"text": "ValueError", "correct": True}, {"text": "TypeError", "correct": False},
                {"text": "InputError", "correct": False}, {"text": "ParseError", "correct": False}]},
            {"text": "Why is `sys.stdin.read()` faster than multiple `input()` calls?", "options": [
                {"text": "Reads all input at once, reducing system call overhead", "correct": True},
                {"text": "Bypasses the Python interpreter", "correct": False},
                {"text": "Uses C instead of Python", "correct": False},
                {"text": "Compresses the data", "correct": False}]},
        ],
        "challenge": {
            "title": "Safe Average",
            "description": "Read N integers on one line separated by spaces. Print their average rounded to 2 decimal places. Handle empty input by printing 0.",
            "initial_code": "# Read space-separated integers and print their average\n",
            "solution_code": "nums = list(map(int, input().split()))\nprint(round(sum(nums)/len(nums), 2) if nums else 0)\n",
            "test_cases": [{"input": "10 20 30", "expected": "20.0"}, {"input": "4 5 6 7", "expected": "5.5"}],
        },
    },

    "les-python-basics-5-pro": {
        "title": "Custom Input Parsers & Context Protocol",
        "content": """# Custom Input Parsers & Context Protocol

## 🎯 Learning Objectives
- Build reusable input parser utilities
- Use `io.StringIO` for testing input-dependent code
- Implement the context manager protocol for resource handling

## 📚 Concept Overview
### io.StringIO — Mock stdin for Testing
```python
import io, sys

def solve():
    n = int(input())
    print(n * 2)

# Test without real keyboard input
sys.stdin = io.StringIO("21\\n")
solve()   # prints 42
sys.stdin = sys.__stdin__   # restore
```

### Context Manager Protocol
Implement `__enter__` and `__exit__` to create `with`-compatible classes:
```python
class Timer:
    import time
    def __enter__(self):
        self.start = self.time.time()
        return self
    def __exit__(self, *args):
        elapsed = self.time.time() - self.start
        print(f"Elapsed: {elapsed:.4f}s")

with Timer():
    sum(range(10_000_000))
```

### dataclasses for Clean Input Structs
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    @classmethod
    def from_input(cls):
        x, y = map(float, input().split())
        return cls(x, y)

p = Point.from_input()
print(p.x, p.y)
```

## 🏆 Key Takeaways
- `io.StringIO` lets you mock stdin — essential for unit-testing input-driven code
- Context managers (`with`) guarantee cleanup even if exceptions occur
- `@dataclass` + `from_input()` classmethod is a clean pattern for structured input
""",
        "questions": [
            {"text": "What is `io.StringIO` primarily used for?", "options": [
                {"text": "Simulating file/stdin input in tests", "correct": True},
                {"text": "Writing binary files", "correct": False},
                {"text": "Compressing strings", "correct": False},
                {"text": "Reading from a network socket", "correct": False}]},
            {"text": "What method marks the entry of a `with` block?", "options": [
                {"text": "__enter__", "correct": True}, {"text": "__start__", "correct": False},
                {"text": "__open__", "correct": False}, {"text": "__init__", "correct": False}]},
            {"text": "What decorator creates a class with auto-generated __init__, __repr__?", "options": [
                {"text": "@dataclass", "correct": True}, {"text": "@classmethod", "correct": False},
                {"text": "@property", "correct": False}, {"text": "@staticmethod", "correct": False}]},
        ],
        "challenge": {
            "title": "Timed Computation",
            "description": "Read N from input. Use a context manager Timer (with time.time()) to time the computation of sum(range(N)). Print the sum.",
            "initial_code": "import time\n# Implement Timer context manager, read N, print sum\n",
            "solution_code": "import time\n\nclass Timer:\n    def __enter__(self):\n        self.start = time.time()\n        return self\n    def __exit__(self, *args):\n        pass\n\nn = int(input())\nwith Timer():\n    result = sum(range(n))\nprint(result)\n",
            "test_cases": [{"input": "10", "expected": "45"}, {"input": "100", "expected": "4950"}],
        },
    },
}


class Command(BaseCommand):
    help = "Add lessons 3-5 for Module 1 (Python Basics) — Strings, Numbers, Input"

    def handle(self, *args, **options):
        count = 0
        with transaction.atomic():
            for lesson_id, data in LESSONS.items():
                updated = Lesson.objects.filter(id=lesson_id).update(
                    title=data["title"],
                    content=data["content"],
                )
                if not updated:
                    self.stdout.write(self.style.WARNING(f"  ⚠  Not found: {lesson_id}"))
                    continue

                quiz, _ = Quiz.objects.get_or_create(
                    id=f"quiz-{lesson_id}",
                    defaults={"lesson_id": lesson_id, "title": f"Quiz: {data['title']}"},
                )
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

        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons (3-5) in Module 1"))
