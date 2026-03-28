"""python manage.py hydrate_module2 -- Module 2 Data Types Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    "les-data-types-1-beginner": {
        "title": "Integers & Floats",
        "content": """# Integers & Floats

## 🎯 Learning Objectives
- Distinguish between `int` and `float` types
- Perform arithmetic with both types
- Understand automatic type promotion

## 📚 Concept Overview
Python has two primary numeric types:
- **`int`** — whole numbers, unlimited precision: `42`, `-7`, `1_000_000`
- **`float`** — decimal numbers (64-bit): `3.14`, `-0.5`, `1.2e10`

When you mix `int` and `float` in an expression, the result is always `float`.

```python
print(type(7))       # <class 'int'>
print(type(7.0))     # <class 'float'>
print(7 / 2)         # 3.5  (float — always)
print(7 // 2)        # 3    (int  — floor division)
print(3 + 1.5)       # 4.5  (int + float = float)
```

### Useful Built-ins
```python
print(abs(-42))          # 42
print(round(3.567, 1))   # 3.6
print(int(3.9))          # 3  (truncates, not rounds)
print(float(5))          # 5.0
```

## ⚠️ Common Pitfalls
- `0.1 + 0.2` produces `0.30000000000000004` — floating point is imprecise
- `int(3.9)` gives `3`, not `4` — use `round()` if you want rounding

## 🏆 Key Takeaways
- `int` is exact; `float` has rounding errors from binary representation
- Division `/` always returns `float`; floor division `//` returns `int`
- Use `round(value, ndigits)` for controlled precision
""",
        "questions": [
            {"text": "What type does `7 / 2` return in Python 3?", "options": [
                {"text": "float", "correct": True}, {"text": "int", "correct": False},
                {"text": "double", "correct": False}, {"text": "decimal", "correct": False}]},
            {"text": "What does `int(3.9)` return?", "options": [
                {"text": "3", "correct": True}, {"text": "4", "correct": False},
                {"text": "3.9", "correct": False}, {"text": "TypeError", "correct": False}]},
            {"text": "Which statement about Python integers is true?", "options": [
                {"text": "They have unlimited precision (no overflow)", "correct": True},
                {"text": "They are limited to 32 bits", "correct": False},
                {"text": "They cannot be negative", "correct": False},
                {"text": "They are the same as C long", "correct": False}]},
        ],
        "challenge": {
            "title": "Temperature Converter",
            "description": "Read a temperature in Celsius (float). Print it in Fahrenheit rounded to 2 decimal places. Formula: F = C * 9/5 + 32",
            "initial_code": "# Read Celsius, print Fahrenheit\n",
            "solution_code": "c = float(input())\nprint(round(c * 9/5 + 32, 2))\n",
            "test_cases": [{"input": "0", "expected": "32.0"}, {"input": "100", "expected": "212.0"}, {"input": "37", "expected": "98.6"}],
        },
    },

    "les-data-types-1-intermediate": {
        "title": "Numeric Types: complex, Decimal & Fraction",
        "content": """# Numeric Types: complex, Decimal & Fraction

## 🎯 Learning Objectives
- Work with complex numbers in Python
- Use `decimal.Decimal` for precision arithmetic
- Use `fractions.Fraction` for exact rational math

## 📚 Concept Overview
### Complex Numbers
```python
z = 3 + 4j
print(z.real, z.imag)    # 3.0  4.0
print(abs(z))             # 5.0 (magnitude)
print(z.conjugate())      # (3-4j)
```

### Decimal — Exact Decimal Arithmetic
```python
from decimal import Decimal, getcontext
getcontext().prec = 10  # set precision

a = Decimal("1.1") + Decimal("2.2")
print(a)          # 3.3 (exact!)
print(0.1 + 0.2)  # 0.30000000000000004 (imprecise)
```

### Fraction — Exact Rational Arithmetic
```python
from fractions import Fraction
f = Fraction(1, 3) + Fraction(1, 6)
print(f)          # 1/2  (exact fraction)
print(float(f))   # 0.5
```

## ⚠️ Common Pitfalls
- Never mix `Decimal` and `float` — `Decimal(1.1)` inherits float imprecision; use `Decimal("1.1")`

## 🏆 Key Takeaways
- Use `Decimal` for financial calculations
- Use `Fraction` for exact rational math (music, geometry)
- Complex numbers support all arithmetic operations natively
""",
        "questions": [
            {"text": "What does `(3+4j).real` return?", "options": [
                {"text": "3.0", "correct": True}, {"text": "4.0", "correct": False},
                {"text": "5.0", "correct": False}, {"text": "(3+4j)", "correct": False}]},
            {"text": "Why should you use `Decimal('1.1')` instead of `Decimal(1.1)`?", "options": [
                {"text": "Decimal(1.1) inherits the float imprecision; string avoids it", "correct": True},
                {"text": "Decimal(1.1) raises a TypeError", "correct": False},
                {"text": "String version is faster", "correct": False},
                {"text": "They are identical", "correct": False}]},
            {"text": "What does `Fraction(1,3) + Fraction(1,6)` return?", "options": [
                {"text": "Fraction(1, 2)", "correct": True}, {"text": "0.5", "correct": False},
                {"text": "Fraction(2, 9)", "correct": False}, {"text": "0.333", "correct": False}]},
        ],
        "challenge": {
            "title": "Precise Bill Splitter",
            "description": "Read a bill amount and number of people as strings. Use Decimal for exact division. Print each person's share with 2 decimal places.",
            "initial_code": "from decimal import Decimal\n# Read bill and people count, print exact share\n",
            "solution_code": "from decimal import Decimal\nbill = Decimal(input())\npeople = int(input())\nshare = bill / people\nprint(f'{share:.2f}')\n",
            "test_cases": [{"input": "100\n3", "expected": "33.33"}, {"input": "50\n4", "expected": "12.50"}],
        },
    },

    "les-data-types-1-pro": {
        "title": "Numeric Protocols, __index__ & Number Theory",
        "content": """# Numeric Protocols, __index__ & Number Theory

## 🎯 Learning Objectives
- Understand Python's numeric protocol (`__int__`, `__float__`, `__index__`)
- Implement custom numeric types
- Apply number theory algorithms in Python

## 📚 Concept Overview
### __index__ Protocol
`__index__` is required for objects used as sequence indices or slice bounds.
```python
class Modular:
    def __init__(self, n, mod):
        self.n = n % mod
        self.mod = mod
    def __index__(self):
        return self.n
    def __int__(self):
        return self.n

m = Modular(7, 5)  # 7 mod 5 = 2
lst = [10, 20, 30, 40, 50]
print(lst[m])   # 30  (__index__ called)
```

### GCD, LCM, and modular arithmetic
```python
import math
print(math.gcd(48, 18))    # 6
print(math.lcm(4, 6))      # 12  (Python 3.9+)

# Modular exponentiation (fast)
print(pow(2, 100, 1000))  # 2^100 mod 1000 = 376
```

## 🏆 Key Takeaways
- `__index__` must return an integer — it's called when an object is used as a list index
- `math.gcd` and `math.lcm` are built-in since Python 3.5/3.9
- `pow(base, exp, mod)` uses fast modular exponentiation — much faster than `(base**exp) % mod`
""",
        "questions": [
            {"text": "What does `math.gcd(48, 18)` return?", "options": [
                {"text": "6", "correct": True}, {"text": "12", "correct": False},
                {"text": "864", "correct": False}, {"text": "3", "correct": False}]},
            {"text": "What is `__index__` used for?", "options": [
                {"text": "Allowing an object to be used as a list index", "correct": True},
                {"text": "Printing the object's index", "correct": False},
                {"text": "Hashing the object", "correct": False},
                {"text": "Sorting objects numerically", "correct": False}]},
            {"text": "Why is `pow(b, e, m)` preferred over `(b**e) % m`?", "options": [
                {"text": "Uses fast modular exponentiation, avoiding huge intermediate values", "correct": True},
                {"text": "It is more readable", "correct": False},
                {"text": "It returns a Fraction", "correct": False},
                {"text": "It handles floats better", "correct": False}]},
        ],
        "challenge": {
            "title": "LCM Calculator",
            "description": "Read N integers (one per line, N given first). Print their LCM.",
            "initial_code": "import math\n# Read N numbers, compute LCM of all\n",
            "solution_code": "import math\nfrom functools import reduce\nn = int(input())\nnums = [int(input()) for _ in range(n)]\nprint(reduce(math.lcm, nums))\n",
            "test_cases": [{"input": "3\n4\n6\n8", "expected": "24"}, {"input": "2\n5\n7", "expected": "35"}],
        },
    },

    # ── Lesson 2: Strings Deep Dive ──────────────────────────────────────────
    "les-data-types-2-beginner": {
        "title": "Strings — Slicing, Methods & Immutability",
        "content": """# Strings — Slicing, Methods & Immutability

## 🎯 Learning Objectives
- Use indexing and slicing to access string parts
- Apply essential string methods
- Understand string immutability

## 📚 Concept Overview
Strings are **ordered sequences of characters**, zero-indexed, and **immutable**.

### Indexing & Slicing
```python
s = "Python"
print(s[0])      # P
print(s[-1])     # n   (last char)
print(s[1:4])    # yth (chars 1,2,3)
print(s[::2])    # Pto (every 2nd char)
print(s[::-1])   # nohtyP (reversed)
```

### Essential Methods
```python
s = "  Hello, World!  "
print(s.strip())          # "Hello, World!"
print(s.strip().lower())  # "hello, world!"
print(s.strip().split(",")) # ['Hello', ' World!']
print("ab" * 3)           # "ababab"
print("World" in s)       # True
```

## ⚠️ Common Pitfalls
- `s[1:4]` gives characters at indices 1, 2, 3 (NOT 4)
- Strings cannot be modified: `s[0] = 'J'` raises `TypeError`

## 🏆 Key Takeaways
- Slice `[start:stop:step]` — stop is excluded, step defaults to 1
- `s[::-1]` is the Pythonic way to reverse a string
- String methods always return new strings — the original is unchanged
""",
        "questions": [
            {"text": "What does `'Python'[1:4]` return?", "options": [
                {"text": "'yth'", "correct": True}, {"text": "'Pyt'", "correct": False},
                {"text": "'ytho'", "correct": False}, {"text": "'ython'", "correct": False}]},
            {"text": "How do you reverse a string `s` in Python?", "options": [
                {"text": "s[::-1]", "correct": True}, {"text": "s.reverse()", "correct": False},
                {"text": "reversed(s)", "correct": False}, {"text": "s[-1:0]", "correct": False}]},
            {"text": "What does `'hello'.strip()` do?", "options": [
                {"text": "Removes leading and trailing whitespace", "correct": True},
                {"text": "Removes all spaces", "correct": False},
                {"text": "Converts to uppercase", "correct": False},
                {"text": "Splits into characters", "correct": False}]},
        ],
        "challenge": {
            "title": "Palindrome Checker",
            "description": "Read a string. Print 'Yes' if it is a palindrome (reads same forwards and backwards, case-insensitive), else 'No'.",
            "initial_code": "# Check if string is a palindrome\n",
            "solution_code": "s = input().strip().lower()\nprint('Yes' if s == s[::-1] else 'No')\n",
            "test_cases": [{"input": "Racecar", "expected": "Yes"}, {"input": "hello", "expected": "No"}, {"input": "madam", "expected": "Yes"}],
        },
    },

    "les-data-types-2-intermediate": {
        "title": "String Processing — join, split, search & regex",
        "content": """# String Processing — join, split, search & regex

## 🎯 Learning Objectives
- Use `split`, `join`, `find`, `replace`, `startswith`, `endswith`
- Apply regex with the `re` module
- Build efficient string-processing pipelines

## 📚 Concept Overview
### Key Methods
```python
words = "one,two,three"
lst = words.split(",")          # ['one', 'two', 'three']
joined = " | ".join(lst)        # 'one | two | three'

s = "Hello, World!"
print(s.find("World"))          # 7 (index, -1 if not found)
print(s.replace("World", "Python"))  # Hello, Python!
print(s.startswith("Hello"))    # True
print(s.endswith("!"))          # True
print(s.count("l"))             # 3
```

### Regex for Pattern Matching
```python
import re
text = "Call 555-1234 or 555-5678"
nums = re.findall(r'\\d{3}-\\d{4}', text)
print(nums)   # ['555-1234', '555-5678']

clean = re.sub(r'\\s+', ' ', "too  many   spaces")
print(clean)  # 'too many spaces'
```

## 🏆 Key Takeaways
- `",".join(list)` is the correct way to join — NOT string concatenation in a loop
- `re.findall` returns all matches; `re.sub` replaces
- Build string pipelines: `text.strip().lower().split()`
""",
        "questions": [
            {"text": "What does `','.join(['a','b','c'])` return?", "options": [
                {"text": "'a,b,c'", "correct": True}, {"text": "['a,b,c']", "correct": False},
                {"text": "'abc'", "correct": False}, {"text": "('a','b','c')", "correct": False}]},
            {"text": "What does `'hello'.find('ell')` return?", "options": [
                {"text": "1", "correct": True}, {"text": "0", "correct": False},
                {"text": "True", "correct": False}, {"text": "-1", "correct": False}]},
            {"text": "What does `re.sub(r'\\s+', ' ', text)` do?", "options": [
                {"text": "Replaces multiple whitespace with a single space", "correct": True},
                {"text": "Removes all spaces", "correct": False},
                {"text": "Splits text into words", "correct": False},
                {"text": "Counts whitespace characters", "correct": False}]},
        ],
        "challenge": {
            "title": "CSV Row Parser",
            "description": "Read a CSV line (comma-separated values). Print each value on a separate line, stripped of leading/trailing spaces.",
            "initial_code": "# Parse CSV line and print each value\n",
            "solution_code": "line = input()\nfor val in line.split(','):\n    print(val.strip())\n",
            "test_cases": [{"input": "Alice, 25, NYC", "expected": "Alice\n25\nNYC"}, {"input": "one,two,three", "expected": "one\ntwo\nthree"}],
        },
    },

    "les-data-types-2-pro": {
        "title": "String Internals, StringIO & Text Protocols",
        "content": """# String Internals, StringIO & Text Protocols

## 🎯 Learning Objectives
- Understand CPython's flexible string representation (PEP 393)
- Use `io.StringIO` as an in-memory text stream
- Implement `__str__`, `__repr__`, and `__format__`

## 📚 Concept Overview
### PEP 393: Compact String Representation
Python automatically chooses the most memory-efficient string storage:
- ASCII strings: 1 byte per character
- BMP Unicode: 2 bytes per character
- Full Unicode: 4 bytes per character

```python
import sys
a = "hello"           # ASCII
b = "café"            # needs Latin-1
c = "你好"             # needs UCS-2
print(sys.getsizeof(a), sys.getsizeof(b), sys.getsizeof(c))
```

### io.StringIO — In-Memory Text Buffer
```python
import io

buf = io.StringIO()
buf.write("Line 1\\n")
buf.write("Line 2\\n")
content = buf.getvalue()   # "Line 1\\nLine 2\\n"
buf.seek(0)
for line in buf:
    print(line.strip())
```

### Text Protocol Dunders
```python
class Color:
    def __init__(self, r, g, b):
        self.r, self.g, self.b = r, g, b
    def __str__(self):    return f"rgb({self.r},{self.g},{self.b})"
    def __repr__(self):   return f"Color({self.r},{self.g},{self.b})"
    def __format__(self, spec):
        if spec == 'hex': return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
        return str(self)
```

## 🏆 Key Takeaways
- CPython's PEP 393 strings adapt their internal storage to save memory
- `io.StringIO` is perfect for building strings incrementally or testing I/O code
- Implement all three text dunders: `__str__`,  `__repr__`, `__format__`
""",
        "questions": [
            {"text": "What is the key advantage of io.StringIO?", "options": [
                {"text": "An in-memory text stream — no file I/O needed", "correct": True},
                {"text": "Faster than regular strings", "correct": False},
                {"text": "Supports binary data", "correct": False},
                {"text": "Thread-safe string access", "correct": False}]},
            {"text": "According to PEP 393, how does CPython store ASCII-only strings?", "options": [
                {"text": "1 byte per character", "correct": True},
                {"text": "4 bytes per character (always)", "correct": False},
                {"text": "2 bytes per character", "correct": False},
                {"text": "Compressed with zlib", "correct": False}]},
            {"text": "Which dunder method is called by `repr(obj)`?", "options": [
                {"text": "__repr__", "correct": True}, {"text": "__str__", "correct": False},
                {"text": "__format__", "correct": False}, {"text": "__display__", "correct": False}]},
        ],
        "challenge": {
            "title": "String Builder",
            "description": "Read N strings. Use io.StringIO to build them into one string separated by ' | '. Print the final string.",
            "initial_code": "import io\n# Build joined string using StringIO\n",
            "solution_code": "import io\nn = int(input())\nbuf = io.StringIO()\nwords = [input() for _ in range(n)]\nbuf.write(' | '.join(words))\nprint(buf.getvalue())\n",
            "test_cases": [{"input": "3\nHello\nWorld\nPython", "expected": "Hello | World | Python"}],
        },
    },

    # ── Lesson 3: Booleans ───────────────────────────────────────────────────
    "les-data-types-3-beginner": {
        "title": "Booleans & Truthiness",
        "content": """# Booleans & Truthiness

## 🎯 Learning Objectives
- Understand Python's `bool` type and its values
- Know which values are truthy and which are falsy
- Use bool in conditions and conversions

## 📚 Concept Overview
`bool` is a subclass of `int` in Python. `True == 1` and `False == 0`.

### Truthy vs Falsy
| Falsy | Truthy |
|-------|--------|
| `False` | `True` |
| `0`, `0.0` | any non-zero number |
| `""` (empty string) | any non-empty string |
| `[]`, `{}`, `()`, `set()` | any non-empty collection |
| `None` | any object not in the Falsy column |

```python
print(bool(0))       # False
print(bool(""))      # False
print(bool([]))      # False
print(bool(42))      # True
print(bool("hi"))    # True
print(bool([1]))     # True
print(True + True)   # 2 (bool is subclass of int!)
```

## ⚠️ Common Pitfalls
- `bool("False")` is `True`! — any non-empty string is truthy
- `if x == True:` is wrong — use `if x:` instead

## 🏆 Key Takeaways
- In Python, many values are implicitly truthy or falsy
- `True == 1` and `False == 0` — bools are ints
- Use `if x:` not `if x == True:` for Pythonic code
""",
        "questions": [
            {"text": "What is `bool('False')` in Python?", "options": [
                {"text": "True (non-empty string is truthy)", "correct": True},
                {"text": "False", "correct": False},
                {"text": "None", "correct": False},
                {"text": "ValueError", "correct": False}]},
            {"text": "What does `True + True` evaluate to?", "options": [
                {"text": "2", "correct": True}, {"text": "True", "correct": False},
                {"text": "TrueTrue", "correct": False}, {"text": "TypeError", "correct": False}]},
            {"text": "Which value is falsy in Python?", "options": [
                {"text": "[]", "correct": True}, {"text": "[0]", "correct": False},
                {"text": "'0'", "correct": False}, {"text": "0.1", "correct": False}]},
        ],
        "challenge": {
            "title": "Truthy Counter",
            "description": "Read N values on separate lines. Count how many are truthy when converted with bool(). Print the count. Values: '0', '', 'None', 'False' are falsy strings (treat them as their actual Python meaning by checking the string).",
            "initial_code": "# Read N values, count truthy ones\n",
            "solution_code": "FALSY = {'0', '', 'None', 'False', '[]', '{}', '()'}\nn = int(input())\ncount = sum(1 for _ in range(n) if input().strip() not in FALSY)\nprint(count)\n",
            "test_cases": [{"input": "4\nhello\n0\nPython\nNone", "expected": "2"}],
        },
    },

    "les-data-types-3-intermediate": {
        "title": "Boolean Algebra & Short-circuit Tricks",
        "content": """# Boolean Algebra & Short-circuit Tricks

## 🎯 Learning Objectives
- Leverage short-circuit evaluation for clean conditional logic
- Use boolean operators as control flow tools
- Apply any()/all() with generators

## 📚 Concept Overview
### Short-circuit Patterns
```python
# Default values with 'or'
config = {}
timeout = config.get("timeout") or 30   # 30 if not set

# Guard with 'and'
user = get_user()
name = user and user.name    # None-safe access

# Conditional assignment (ternary equivalent)
x = 10
result = "even" if x % 2 == 0 else "odd"
```

### Generator-based any() / all()
```python
nums = range(1, 1000001)

# Stops at first True found — O(1) best case!
print(any(n > 999999 for n in nums))   # True

# Check: all nums are positive in a large list
print(all(n > 0 for n in nums))        # True
```

### Bitwise vs Logical
```python
# Logical: short-circuit, returns operand value
print(0 or "default")    # "default"
print(5 and "ok")        # "ok"

# Bitwise: always evaluates both, works on ints/bools
print(True & False)      # False (int 0)
print(True | False)      # True  (int 1)
```

## 🏆 Key Takeaways
- `x = y or default` is the Pythonic default-value pattern
- `any()`/`all()` are lazy — use with generators, not lists, for efficiency
- `and`/`or` return operand values, not just `True`/`False`
""",
        "questions": [
            {"text": "What does `None or 'default'` evaluate to?", "options": [
                {"text": "'default'", "correct": True}, {"text": "None", "correct": False},
                {"text": "True", "correct": False}, {"text": "False", "correct": False}]},
            {"text": "Why is `any(gen)` more efficient than `any(list)`?", "options": [
                {"text": "Generators are lazy — stop at first True without building the full list", "correct": True},
                {"text": "Generators use less memory but are slower", "correct": False},
                {"text": "any() works differently with generators", "correct": False},
                {"text": "Lists cannot be used with any()", "correct": False}]},
            {"text": "What does `5 and 'ok'` return?", "options": [
                {"text": "'ok'", "correct": True}, {"text": "True", "correct": False},
                {"text": "5", "correct": False}, {"text": "False", "correct": False}]},
        ],
        "challenge": {
            "title": "Safe Divide",
            "description": "Read two integers. Use short-circuit evaluation to print the result of dividing the first by the second, or print 'Cannot divide by zero' if second is 0.",
            "initial_code": "# Use boolean short-circuit to guard division\n",
            "solution_code": "a = int(input())\nb = int(input())\nprint(b and a // b or 'Cannot divide by zero')\n",
            "test_cases": [{"input": "10\n2", "expected": "5"}, {"input": "10\n0", "expected": "Cannot divide by zero"}],
        },
    },

    "les-data-types-3-pro": {
        "title": "Boolean Optimization & Three-valued Logic",
        "content": """# Boolean Optimization & Three-valued Logic

## 🎯 Learning Objectives
- Implement three-valued (ternary) logic in Python
- Profile and optimize boolean expressions
- Use numpy boolean arrays for vectorized logic

## 📚 Concept Overview
### Three-valued Logic (True / False / Unknown)
```python
class Tribool:
    UNKNOWN = object()
    def __init__(self, val):
        self.val = val
    def __and__(self, other):
        if self.val is False or other.val is False:
            return Tribool(False)
        if self.val is True and other.val is True:
            return Tribool(True)
        return Tribool(Tribool.UNKNOWN)
    def __repr__(self):
        return {True: 'T', False: 'F', Tribool.UNKNOWN: '?'}[self.val]

T, F, U = Tribool(True), Tribool(False), Tribool(Tribool.UNKNOWN)
print(T & U)   # ?
print(F & U)   # F  (short-circuit: False & anything = False)
```

### Vectorized Boolean with numpy (if available)
```python
import numpy as np
arr = np.array([1, 0, 2, 0, 3])
mask = arr > 0           # array([True, False, True, False, True])
print(arr[mask])         # array([1, 2, 3])  — boolean indexing
print(np.any(mask))      # True
print(np.all(mask))      # False
```

## 🏆 Key Takeaways
- Three-valued logic handles unknown/null states (used in SQL, probabilistic systems)
- Numpy boolean operations are vectorized — orders of magnitude faster than Python loops
- Python's `and`/`or` cannot be overloaded; override `__and__`/`__or__` for bitwise ops
""",
        "questions": [
            {"text": "In three-valued logic, what is False AND Unknown?", "options": [
                {"text": "False", "correct": True}, {"text": "Unknown", "correct": False},
                {"text": "True", "correct": False}, {"text": "Error", "correct": False}]},
            {"text": "Why are numpy boolean arrays faster than Python loops?", "options": [
                {"text": "Operations are vectorized and run in compiled C code", "correct": True},
                {"text": "They use less memory", "correct": False},
                {"text": "They bypass the GIL", "correct": False},
                {"text": "They skip type checking", "correct": False}]},
            {"text": "Which operator can be overloaded to customize '&' behavior?", "options": [
                {"text": "__and__", "correct": True}, {"text": "__bool__", "correct": False},
                {"text": "__and_bool__", "correct": False}, {"text": "and is not overloadable", "correct": False}]},
        ],
        "challenge": {
            "title": "Mask Filter",
            "description": "Read N integers. Print only those that are positive and even, on one line separated by spaces. If none match, print 'None'.",
            "initial_code": "# Filter positive even numbers\n",
            "solution_code": "n = int(input())\nnums = [int(input()) for _ in range(n)]\nresult = [x for x in nums if x > 0 and x % 2 == 0]\nprint(' '.join(map(str, result)) if result else 'None')\n",
            "test_cases": [{"input": "5\n1\n4\n-2\n6\n3", "expected": "4 6"}, {"input": "3\n1\n3\n5", "expected": "None"}],
        },
    },

    # ── Lesson 4: Lists ──────────────────────────────────────────────────────
    "les-data-types-4-beginner": {
        "title": "Lists — Creating, Indexing & Modifying",
        "content": """# Lists — Creating, Indexing & Modifying

## 🎯 Learning Objectives
- Create and modify Python lists
- Use list methods: append, insert, remove, pop
- Iterate over lists with for loops

## 📚 Concept Overview
A **list** is an ordered, mutable sequence that can hold any mix of types.

```python
fruits = ["apple", "banana", "cherry"]
nums = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, 3.14]
```

### Core Operations
```python
lst = [10, 20, 30]
lst.append(40)        # [10, 20, 30, 40]
lst.insert(1, 15)     # [10, 15, 20, 30, 40]
lst.remove(15)        # removes first occurrence of 15
lst.pop()             # removes & returns last: 40
lst.pop(0)            # removes & returns index 0: 10
print(len(lst))       # 2
print(lst[0])         # 20
print(lst[-1])        # 30
```

### List Slicing
```python
nums = [0, 1, 2, 3, 4, 5]
print(nums[1:4])    # [1, 2, 3]
print(nums[::2])    # [0, 2, 4]
print(nums[::-1])   # [5, 4, 3, 2, 1, 0]
```

## ⚠️ Common Pitfalls
- `list.remove(x)` removes the FIRST occurrence — not all
- Modifying a list while iterating over it can skip elements

## 🏆 Key Takeaways
- Lists are O(1) for append/pop at end; O(n) for insert/remove at middle
- Use `.copy()` or `[:]` to make a shallow copy
- Lists support mixed types, but same-type lists are faster
""",
        "questions": [
            {"text": "What does `[1, 2, 3].pop()` return?", "options": [
                {"text": "3", "correct": True}, {"text": "1", "correct": False},
                {"text": "[1, 2]", "correct": False}, {"text": "None", "correct": False}]},
            {"text": "Which method adds an element at a specific index?", "options": [
                {"text": "insert()", "correct": True}, {"text": "append()", "correct": False},
                {"text": "add()", "correct": False}, {"text": "push()", "correct": False}]},
            {"text": "What does `nums[::2]` do for `[0,1,2,3,4]`?", "options": [
                {"text": "Returns every 2nd element: [0, 2, 4]", "correct": True},
                {"text": "Returns first 2 elements: [0, 1]", "correct": False},
                {"text": "Doubles all elements", "correct": False},
                {"text": "Returns [1, 3]", "correct": False}]},
        ],
        "challenge": {
            "title": "List Rotator",
            "description": "Read N then N integers. Rotate the list left by 1 position (first element goes to end). Print the result space-separated.",
            "initial_code": "# Read N integers and rotate left by 1\n",
            "solution_code": "n = int(input())\nlst = [int(input()) for _ in range(n)]\nrotated = lst[1:] + lst[:1]\nprint(*rotated)\n",
            "test_cases": [{"input": "4\n1\n2\n3\n4", "expected": "2 3 4 1"}, {"input": "3\n5\n6\n7", "expected": "6 7 5"}],
        },
    },

    "les-data-types-4-intermediate": {
        "title": "List Comprehensions, Sorting & Functional Tools",
        "content": """# List Comprehensions, Sorting & Functional Tools

## 🎯 Learning Objectives
- Write list comprehensions for clean, fast list creation
- Sort lists with custom keys
- Use `map`, `filter`, `zip`, `enumerate`

## 📚 Concept Overview
### List Comprehensions
```python
# Pattern: [expression for item in iterable if condition]
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]
flat = [item for row in [[1,2],[3,4]] for item in row]  # flatten
```

### Sorting
```python
students = [("Alice", 90), ("Bob", 85), ("Carol", 92)]
students.sort(key=lambda s: s[1], reverse=True)
# [('Carol', 92), ('Alice', 90), ('Bob', 85)]
```

### Functional Tools
```python
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))

# zip — parallel iteration
names = ["Alice", "Bob"]
scores = [90, 85]
for name, score in zip(names, scores):
    print(f"{name}: {score}")

# enumerate — index + value
for i, val in enumerate(["a", "b", "c"], start=1):
    print(i, val)   # 1 a, 2 b, 3 c
```

## 🏆 Key Takeaways
- List comprehensions are faster than equivalent for-loops + `append`
- Use `key=` in `sort()` — never modify the items to sort them
- Prefer `enumerate()` over `range(len(lst))` for indexed iteration
""",
        "questions": [
            {"text": "What does `[x**2 for x in range(4)]` produce?", "options": [
                {"text": "[0, 1, 4, 9]", "correct": True}, {"text": "[1, 4, 9, 16]", "correct": False},
                {"text": "[0, 2, 4, 6]", "correct": False}, {"text": "[1, 2, 3, 4]", "correct": False}]},
            {"text": "What does `zip([1,2], ['a','b'])` produce?", "options": [
                {"text": "[(1,'a'), (2,'b')]", "correct": True}, {"text": "[1,2,'a','b']", "correct": False},
                {"text": "{'1':'a', '2':'b'}", "correct": False}, {"text": "[[1,'a'],[2,'b']]", "correct": False}]},
            {"text": "Which is more Pythonic for looping with indices?", "options": [
                {"text": "for i, val in enumerate(lst)", "correct": True},
                {"text": "for i in range(len(lst))", "correct": False},
                {"text": "for i = 0; i < len(lst); i++", "correct": False},
                {"text": "for val in lst.items()", "correct": False}]},
        ],
        "challenge": {
            "title": "Grade Transformer",
            "description": "Read N scores (integers). Use a list comprehension to print each score transformed to a letter grade (>=90: A, >=80: B, >=70: C, else F), one per line.",
            "initial_code": "# Read N scores, print letter grades\n",
            "solution_code": "def grade(s):\n    return 'A' if s>=90 else 'B' if s>=80 else 'C' if s>=70 else 'F'\nn = int(input())\ngrades = [grade(int(input())) for _ in range(n)]\nprint(*grades, sep='\\n')\n",
            "test_cases": [{"input": "3\n95\n82\n67", "expected": "A\nB\nF"}],
        },
    },

    "les-data-types-4-pro": {
        "title": "List Internals, Memory Efficiency & Advanced Patterns",
        "content": """# List Internals, Memory Efficiency & Advanced Patterns

## 🎯 Learning Objectives
- Understand CPython list over-allocation strategy
- Use `array` and `deque` for specialized list needs
- Apply advanced patterns: chunking, sliding windows, flatten

## 📚 Concept Overview
### CPython List Over-allocation
Lists over-allocate to make appending O(1) amortized:
```python
import sys
lst = []
for i in range(10):
    lst.append(i)
    print(f"len={len(lst)}, allocated~={sys.getsizeof(lst)}")
```

### array — Typed, Compact Lists
```python
from array import array
arr = array('i', [1, 2, 3, 4, 5])  # 'i' = signed int
# Uses ~4x less memory than list for numbers
```

### collections.deque — O(1) at Both Ends
```python
from collections import deque
dq = deque([1, 2, 3])
dq.appendleft(0)   # O(1) — list prepend is O(n)!
dq.popleft()       # O(1)
dq.rotate(1)       # rotate right by 1
```

### Advanced Patterns
```python
# Chunking a list
def chunks(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

# Sliding window
def windows(lst, k):
    return [lst[i:i+k] for i in range(len(lst)-k+1)]

# Deep flatten
def flatten(lst):
    return [x for sub in lst for x in (flatten(sub) if isinstance(sub, list) else [sub])]
```

## 🏆 Key Takeaways
- CPython lists over-allocate — each `append` is O(1) amortized but wastes memory
- Use `array.array` for large homogeneous numeric data (4x memory savings)
- Use `deque` when you need efficient prepend/pop-left operations
""",
        "questions": [
            {"text": "Why is `list.append()` O(1) amortized?", "options": [
                {"text": "Lists over-allocate, so usually no reallocation needed", "correct": True},
                {"text": "Lists never need to resize", "correct": False},
                {"text": "Python uses linked lists internally", "correct": False},
                {"text": "Lists allocate exactly 1 extra slot", "correct": False}]},
            {"text": "What is the time complexity of `deque.appendleft()`?", "options": [
                {"text": "O(1)", "correct": True}, {"text": "O(n)", "correct": False},
                {"text": "O(log n)", "correct": False}, {"text": "O(n^2)", "correct": False}]},
            {"text": "When should you use `array.array` instead of a list?", "options": [
                {"text": "When storing large amounts of homogeneous numeric data", "correct": True},
                {"text": "When you need fast search", "correct": False},
                {"text": "When you need mixed types", "correct": False},
                {"text": "When you need O(1) indexing", "correct": False}]},
        ],
        "challenge": {
            "title": "Sliding Window Maximum",
            "description": "Read N then N integers, then K (window size). Print the maximum of each window of size K, space-separated.",
            "initial_code": "from collections import deque\n# Sliding window maximum\n",
            "solution_code": "from collections import deque\nn = int(input())\nnums = [int(input()) for _ in range(n)]\nk = int(input())\nresult = [max(nums[i:i+k]) for i in range(n-k+1)]\nprint(*result)\n",
            "test_cases": [{"input": "5\n1\n3\n2\n5\n4\n3", "expected": "3 5 5"}, {"input": "4\n2\n1\n4\n3\n2", "expected": "4 4"}],
        },
    },

    # ── Lesson 5: Tuples ─────────────────────────────────────────────────────
    "les-data-types-5-beginner": {
        "title": "Tuples — Immutable Sequences",
        "content": """# Tuples — Immutable Sequences

## 🎯 Learning Objectives
- Create and use tuples
- Understand why tuples are immutable
- Use tuple unpacking

## 📚 Concept Overview
A **tuple** is an ordered, **immutable** sequence. Once created, its contents cannot change.

```python
point = (3, 4)
rgb = (255, 128, 0)
single = (42,)       # Note the comma! (42) is just 42
empty = ()

print(point[0])      # 3
print(len(rgb))      # 3
```

### Tuple Unpacking
```python
x, y = (3, 4)          # unpack into variables
a, b, *rest = (1, 2, 3, 4, 5)  # extended unpacking
# a=1, b=2, rest=[3, 4, 5]
```

### Tuples as Dictionary Keys
```python
# Lists cannot be dict keys (unhashable)
locations = {(40.7, -74.0): "New York", (51.5, -0.1): "London"}
print(locations[(40.7, -74.0)])   # "New York"
```

## ⚠️ Common Pitfalls
- `(42)` is an `int`, NOT a tuple — you need the trailing comma: `(42,)`
- Tuples are immutable but can contain mutable objects

## 🏆 Key Takeaways
- Tuples are faster than lists for fixed data (constant access, no modification)
- Tuples are hashable (if all elements are hashable) — can be used as dict keys
- Prefer tuples for data that should not be modified (coordinates, RGB, records)
""",
        "questions": [
            {"text": "How do you create a single-element tuple?", "options": [
                {"text": "(42,)", "correct": True}, {"text": "(42)", "correct": False},
                {"text": "tuple(42)", "correct": False}, {"text": "[42]", "correct": False}]},
            {"text": "Why can tuples (but not lists) be used as dictionary keys?", "options": [
                {"text": "Tuples are hashable; lists are not", "correct": True},
                {"text": "Tuples are faster to compare", "correct": False},
                {"text": "Lists are too large for keys", "correct": False},
                {"text": "Python restricts list usage in dicts", "correct": False}]},
            {"text": "What does `a, b, *rest = (1, 2, 3, 4)` do?", "options": [
                {"text": "a=1, b=2, rest=[3,4]", "correct": True},
                {"text": "a=1, b=2, rest=(3,4)", "correct": False},
                {"text": "Raises ValueError", "correct": False},
                {"text": "a=1, b=2, rest=3", "correct": False}]},
        ],
        "challenge": {
            "title": "Point Distance",
            "description": "Read two points as 'x y' on separate lines. Compute the Euclidean distance between them. Print rounded to 2 decimal places.",
            "initial_code": "import math\n# Read two 2D points and compute distance\n",
            "solution_code": "import math\nx1, y1 = map(float, input().split())\nx2, y2 = map(float, input().split())\ndist = math.sqrt((x2-x1)**2 + (y2-y1)**2)\nprint(round(dist, 2))\n",
            "test_cases": [{"input": "0 0\n3 4", "expected": "5.0"}, {"input": "1 1\n4 5", "expected": "5.0"}],
        },
    },

    "les-data-types-5-intermediate": {
        "title": "Named Tuples, Structural Pattern Matching",
        "content": """# Named Tuples & Structural Pattern Matching

## 🎯 Learning Objectives
- Use `namedtuple` and `NamedTuple` for self-documenting records
- Apply Python 3.10+ structural pattern matching (`match/case`)
- Compare records with tuples vs dataclasses

## 📚 Concept Overview
### namedtuple
```python
from collections import namedtuple
Point = namedtuple('Point', ['x', 'y'])
p = Point(3, 4)
print(p.x, p.y)    # 3 4
print(p[0])        # 3 (still a tuple!)
print(p._asdict()) # {'x': 3, 'y': 4}
```

### typing.NamedTuple (with types)
```python
from typing import NamedTuple
class Employee(NamedTuple):
    name: str
    dept: str
    salary: float = 50000.0

emp = Employee("Alice", "Eng")
print(emp.name, emp.salary)  # Alice 50000.0
```

### Structural Pattern Matching (Python 3.10+)
```python
def process(command):
    match command:
        case ("quit",):
            return "Exiting"
        case ("go", direction):
            return f"Going {direction}"
        case ("get", obj) if obj != "":
            return f"Getting {obj}"
        case _:
            return "Unknown command"
```

## 🏆 Key Takeaways
- `NamedTuple` gives named access while remaining a true tuple (hashable, fast)
- Structural pattern matching is more powerful than `isinstance` chains
- Use `namedtuple` for simple records; `dataclass` when you need mutability
""",
        "questions": [
            {"text": "What is a key advantage of NamedTuple over a regular tuple?", "options": [
                {"text": "Fields are accessible by name, improving readability", "correct": True},
                {"text": "NamedTuples are mutable", "correct": False},
                {"text": "NamedTuples use less memory", "correct": False},
                {"text": "NamedTuples support inheritance", "correct": False}]},
            {"text": "Which Python version introduced structural pattern matching (match/case)?", "options": [
                {"text": "3.10", "correct": True}, {"text": "3.8", "correct": False},
                {"text": "3.9", "correct": False}, {"text": "3.12", "correct": False}]},
            {"text": "What does `p._asdict()` return for a namedtuple?", "options": [
                {"text": "A dict mapping field names to values", "correct": True},
                {"text": "A list of field names", "correct": False},
                {"text": "A JSON string", "correct": False},
                {"text": "A regular tuple", "correct": False}]},
        ],
        "challenge": {
            "title": "Employee Record",
            "description": "Read name, department, and salary (float) on separate lines. Create a NamedTuple Employee.  Print: 'name works in dept earning salary'.",
            "initial_code": "from typing import NamedTuple\n# Define Employee NamedTuple and print formatted string\n",
            "solution_code": "from typing import NamedTuple\nclass Employee(NamedTuple):\n    name: str\n    dept: str\n    salary: float\n\nname = input()\ndept = input()\nsalary = float(input())\nemp = Employee(name, dept, salary)\nprint(f'{emp.name} works in {emp.dept} earning {emp.salary}')\n",
            "test_cases": [{"input": "Alice\nEngineering\n75000.0", "expected": "Alice works in Engineering earning 75000.0"}],
        },
    },

    "les-data-types-5-pro": {
        "title": "Tuple Internals, Immutable Optimization & C API",
        "content": """# Tuple Internals, Immutable Optimization & Persistent Data

## 🎯 Learning Objectives
- Understand why tuples are faster than lists for fixed data
- Use persistent (immutable) data structures with pyrsistent
- Implement record-style classes with __slots__

## 📚 Concept Overview
### Why Tuples are Faster
CPython stores tuples more compactly than lists:
- Tuples have no over-allocation (exact size)
- Tuple creation is 60% faster than list creation
- Constant tuples are stored in code object as constants

```python
import timeit
# Tuple creation is faster
print(timeit.timeit('(1,2,3)', number=10_000_000))
print(timeit.timeit('[1,2,3]', number=10_000_000))
```

### __slots__ for Memory-Efficient Records
```python
class Point:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x, self.y = x, y

# Uses ~40% less memory than regular class
# Prevents adding new attributes
p = Point(3, 4)
# p.z = 5  # AttributeError!
```

### Immutable Update Pattern
```python
from collections import namedtuple
Record = namedtuple('Record', ['name', 'score'])
r = Record("Alice", 90)

# Update by creating a new namedtuple
r2 = r._replace(score=95)
print(r)   # Record(name='Alice', score=90)  unchanged!
print(r2)  # Record(name='Alice', score=95)
```

## 🏆 Key Takeaways
- Tuples are faster and more memory-efficient than lists for fixed-size data
- `__slots__` reduces instance memory by ~40% and speeds up attribute access
- `_replace()` creates a modified copy of a namedtuple without mutation
""",
        "questions": [
            {"text": "Why are tuples created faster than lists in CPython?", "options": [
                {"text": "Tuples have no over-allocation and can be stored as constants", "correct": True},
                {"text": "Tuples use a hash table internally", "correct": False},
                {"text": "Tuples skip type checking", "correct": False},
                {"text": "Lists require memory encryption", "correct": False}]},
            {"text": "What does `__slots__` do in a Python class?", "options": [
                {"text": "Restricts instance attributes to a fixed set, saving memory", "correct": True},
                {"text": "Makes all methods static", "correct": False},
                {"text": "Enables the class to be used as a dict key", "correct": False},
                {"text": "Prevents inheritance", "correct": False}]},
            {"text": "How do you 'update' a namedtuple field without mutation?", "options": [
                {"text": "Use ._replace() to create a new copy", "correct": True},
                {"text": "Directly assign: record.field = value", "correct": False},
                {"text": "Use .update() method", "correct": False},
                {"text": "Convert to list, modify, convert back", "correct": False}]},
        ],
        "challenge": {
            "title": "Slot Class Benchmark",
            "description": "Create a Point class with __slots__ = ('x','y'). Read x and y as floats. Print distance from origin rounded to 2 decimal places.",
            "initial_code": "import math\n# Create Point with __slots__ and compute distance\n",
            "solution_code": "import math\n\nclass Point:\n    __slots__ = ('x', 'y')\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n\nx, y = map(float, input().split())\np = Point(x, y)\nprint(round(math.hypot(p.x, p.y), 2))\n",
            "test_cases": [{"input": "3 4", "expected": "5.0"}, {"input": "5 12", "expected": "13.0"}],
        },
    },
}


class Command(BaseCommand):
    help = "Hydrate Module 2 (Data Types) — Lessons 1-5"

    def handle(self, *args, **options):
        count = 0
        with transaction.atomic():
            for lesson_id, data in LESSONS.items():
                updated = Lesson.objects.filter(id=lesson_id).update(
                    title=data["title"], content=data["content"],
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
                        id=f"q-{lesson_id}-{i+1}", quiz_id=quiz.id,
                        text=q["text"], type="mcq", options=q["options"], points=5,
                    )
                ch = data["challenge"]
                Challenge.objects.filter(lesson_id=lesson_id).delete()
                Challenge.objects.create(
                    lesson_id=lesson_id, title=ch["title"], description=ch["description"],
                    initial_code=ch["initial_code"], solution_code=ch["solution_code"],
                    test_cases=ch["test_cases"], points=20,
                )
                count += 1
                self.stdout.write(f"  ✅ {lesson_id}")
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 2 (1-5)"))
