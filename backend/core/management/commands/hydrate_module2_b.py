"""python manage.py hydrate_module2_b -- Module 2 Data Types Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: Dictionaries ──────────────────────────────────────────────
    "les-data-types-6-beginner": {
        "title": "Dictionaries — Key-Value Pairs",
        "content": """# Dictionaries — Key-Value Pairs

## 🎯 Learning Objectives
- Create and use dictionaries in Python
- Access, add, and modify key-value pairs
- Understand dictionary keys and values

## 📚 Concept Overview
A **dictionary** is an unordered, mutable collection of key-value pairs. Think of it like a real dictionary or a phonebook.

```python
# Create a dictionary
user = {
    "name": "Alice",
    "age": 25,
    "email": "alice@example.com"
}

# Access values
print(user["name"])    # Alice

# Add or modify
user["age"] = 26       # Update
user["city"] = "NYC"   # Add new

# Delete
del user["email"]
```

### Essential Methods
```python
print(user.keys())     # dict_keys(['name', 'age', 'city'])
print(user.values())   # dict_values(['Alice', 26, 'NYC'])
print(user.items())    # dict_items([('name', 'Alice'), ...])
print(user.get("job", "N/A"))  # "N/A" (safe access)
```

## ⚠️ Common Pitfalls
- Accessing a missing key with `dict[key]` raises `KeyError`. Use `.get()` or check `if key in dict:`.
- Dictionary keys must be **hashable** (e.g., strings, numbers, tuples). Lists cannot be keys.

## 🏆 Key Takeaways
- Dictionaries are optimized for fast lookups by key
- Keys are unique; assigning to an existing key overwrites the value
- Use `.get()` to avoid crashes on missing keys
""",
        "questions": [
            {"text": "What happens if you try to access a non-existent key using `my_dict['key']`?", "options": [
                {"text": "KeyError is raised", "correct": True}, {"text": "Returns None", "correct": False},
                {"text": "Returns empty string", "correct": False}, {"text": "Variable is created", "correct": False}]},
            {"text": "Which method returns all values in a dictionary?", "options": [
                {"text": ".values()", "correct": True}, {"text": ".keys()", "correct": False},
                {"text": ".items()", "correct": False}, {"text": ".all()", "correct": False}]},
            {"text": "What type of object CANNOT be used as a dictionary key?", "options": [
                {"text": "A list", "correct": True}, {"text": "A string", "correct": False},
                {"text": "An integer", "correct": False}, {"text": "A tuple of strings", "correct": False}]},
        ],
        "challenge": {
            "title": "Contact Book",
            "description": "Read a name and a phone number as strings. Store them in a dictionary. Then read a search name. If the name exists in the dictionary, print the phone number, else print 'Not Found'.",
            "initial_code": "# Build a simple contact lookup\n",
            "solution_code": "name = input()\nphone = input()\ncontacts = {name: phone}\nsearch = input()\nprint(contacts.get(search, 'Not Found'))\n",
            "test_cases": [
                {"input": "Alice\n555-0100\nAlice", "expected": "555-0100"},
                {"input": "Bob\n555-0200\nCharlie", "expected": "Not Found"}
            ],
        },
    },

    "les-data-types-6-intermediate": {
        "title": "Dict Comprehensions & Advanced Mapping",
        "content": """# Dict Comprehensions & Advanced Mapping

## 🎯 Learning Objectives
- Write efficient dictionary comprehensions
- Use `defaultdict` and `Counter` from `collections`
- Merge dictionaries using the `|` operator

## 📚 Concept Overview
### Dictionary Comprehensions
```python
# {key_expr: val_expr for item in iterable if condition}
names = ["Alice", "Bob", "Charlie"]
name_lengths = {name: len(name) for name in names}
# {'Alice': 5, 'Bob': 3, 'Charlie': 7}
```

### collections.defaultdict
Avoids `KeyError` by providing a default value for missing keys.
```python
from collections import defaultdict
counts = defaultdict(int)  # default value is 0
counts["apple"] += 1
```

### collections.Counter
High-performance tool for counting hashable objects.
```python
from collections import Counter
c = Counter("abracadabra")
print(c.most_common(2))  # [('a', 5), ('b', 2)]
```

### Merging (Python 3.9+)
```python
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2  # {'a': 1, 'b': 3, 'c': 4}
```

## 🏆 Key Takeaways
- Dict comprehensions transform one collection into a mapping in a single line
- `defaultdict` is cleaner than manual `if key not in d` checks
- Counter is the standard way to frequency-count items
""",
        "questions": [
            {"text": "What does `{x: x**2 for x in (2, 3)}` produce?", "options": [
                {"text": "{2: 4, 3: 9}", "correct": True}, {"text": "{4, 9}", "correct": False},
                {"text": "[2, 4, 3, 9]", "correct": False}, {"text": "{2, 3}", "correct": False}]},
            {"text": "Which class is best for counting word frequencies in a list?", "options": [
                {"text": "Counter", "correct": True}, {"text": "defaultdict", "correct": False},
                {"text": "OrderedDict", "correct": False}, {"text": "ChainMap", "correct": False}]},
            {"text": "How do you merge two dictionaries d1 and d2 in Python 3.9+?", "options": [
                {"text": "d1 | d2", "correct": True}, {"text": "d1 + d2", "correct": False},
                {"text": "d1.merge(d2)", "correct": False}, {"text": "d1 & d2", "correct": False}]},
        ],
        "challenge": {
            "title": "Frequency Counter",
            "description": "Read a sentence. Print a dictionary where keys are words and values are their counts. Sort by words alphabetically.",
            "initial_code": "from collections import Counter\n# Print word frequencies sorted alphabetically\n",
            "solution_code": "from collections import Counter\nwords = input().split()\ncounts = dict(sorted(Counter(words).items()))\nprint(counts)\n",
            "test_cases": [{"input": "apple banana apple cherry banana apple", "expected": "{'apple': 3, 'banana': 2, 'cherry': 1}"}],
        },
    },

    "les-data-types-6-pro": {
        "title": "Dict Internals (Hash Tables) & Optimization",
        "content": """# Dict Internals (Hash Tables) & Optimization

## 🎯 Learning Objectives
- Understand CPython's hash table implementation
- Analyze time complexity of dict operations
- Optimize memory usage for large dictionaries

## 📚 Concept Overview
### How Dictionaries Work (Hash Tables)
1. **Hash**: The key is hashed using `hash(key)`.
2. **Bucket**: The hash is mapped to an index in an underlying array.
3. **Collision**: If two keys hash to the same bucket, Python uses **open addressing** (probing) to find the next empty slot.

### Time Complexity
| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| Lookup    | O(1)         | O(n)       |
| Insert    | O(1)         | O(n)       |
| Delete    | O(1)         | O(n)       |

### Memory Optimization
- Since Python 3.6, dictionaries are **ordered** by default and used a more **compact** representation saving 20-25% memory.
- If you have millions of objects with fixed keys, consider using `__slots__` or a `NamedTuple` instead of a dictionary for each instance.

## 🏆 Key Takeaways
- Dictionary lookups are O(1) on average because of hashing
- Custom objects must implement `__hash__` and `__eq__` to be used as keys correctly
- Modern CPython dictionaries are both fast and memory-efficient compared to older versions
""",
        "questions": [
            {"text": "What is the average time complexity of looking up a value in a Python dictionary?", "options": [
                {"text": "O(1)", "correct": True}, {"text": "O(log n)", "correct": False},
                {"text": "O(n)", "correct": False}, {"text": "O(n log n)", "correct": False}]},
            {"text": "What happens if a hash collision occurs in a Python dictionary?", "options": [
                {"text": "Python uses open addressing to find another slot", "correct": True},
                {"text": "The key is replaced", "correct": False},
                {"text": "The dictionary crashes", "correct": False},
                {"text": "It uses a linked list at that bucket", "correct": False}]},
            {"text": "Why must keys be hashable?", "options": [
                {"text": "To ensure their hash value stays constant throughout their lifetime", "correct": True},
                {"text": "To make them easier to print", "correct": False},
                {"text": "To save memory", "correct": False},
                {"text": "It is just a naming convention", "correct": False}]},
        ],
        "challenge": {
            "title": "Custom Hashable Object",
            "description": "Read two integers x and y. Create a simple Point(x, y) class that is hashable. Add it to a set. If you read the same x, y again, set size should stay 1. Print the set size.",
            "initial_code": "# Implement __hash__ and __eq__\n",
            "solution_code": "class Point:\n    def __init__(self, x, y):\n        self.x, self.y = x, y\n    def __hash__(self):\n        return hash((self.x, self.y))\n    def __eq__(self, other):\n        return (self.x, self.y) == (other.x, other.y)\n\nx, y = map(int, input().split())\np1 = Point(x, y)\np2 = Point(x, y)\ns = {p1, p2}\nprint(len(s))\n",
            "test_cases": [{"input": "10 20", "expected": "1"}],
        },
    },

    # ── Lesson 7: Sets ───────────────────────────────────────────────────────
    "les-data-types-7-beginner": {
        "title": "Sets — Ensuring Uniqueness",
        "content": """# Sets — Ensuring Uniqueness

## 🎯 Learning Objectives
- Create and manipulate sets
- Perform set operations like union and intersection
- Use sets to remove duplicates from other collections

## 📚 Concept Overview
A **set** is an unordered collection of **unique** elements.

```python
# Create a set
colors = {"red", "green", "blue"}
fruits = set(["apple", "banana", "apple"]) # {"apple", "banana"}

# Add/Remove
colors.add("yellow")
colors.remove("red") # Raises KeyError if not found
colors.discard("purple") # Safe remove

# Check membership (O(1) fast!)
print("blue" in colors) # True
```

### Set Operations
```python
a = {1, 2, 3}
b = {3, 4, 5}

print(a | b) # Union: {1, 2, 3, 4, 5}
print(a & b) # Intersection: {3}
print(a - b) # Difference: {1, 2}
print(a ^ b) # Symmetric Difference: {1, 2, 4, 5}
```

## 🏆 Key Takeaways
- Sets automatically remove duplicates
- Membership testing (`x in set`) is extremely fast (O(1))
- Sets are like dictionaries without values
""",
        "questions": [
            {"text": "What happens if you add an existing element to a set?", "options": [
                {"text": "Nothing, sets keep only unique elements", "correct": True},
                {"text": "An error is raised", "correct": False},
                {"text": "The element is added twice", "correct": False},
                {"text": "The set is cleared", "correct": False}]},
            {"text": "How do you create an empty set in Python?", "options": [
                {"text": "set()", "correct": True}, {"text": "{}", "correct": False},
                {"text": "[]", "correct": False}, {"text": "empty(set)", "correct": False}]},
            {"text": "What is the result of `{1, 2} | {2, 3}`?", "options": [
                {"text": "{1, 2, 3}", "correct": True}, {"text": "{2}", "correct": False},
                {"text": "{1, 3}", "correct": False}, {"text": "{1, 2, 2, 3}", "correct": False}]},
        ],
        "challenge": {
            "title": "Duplicate Remover",
            "description": "Read a line of numbers. Print only the unique numbers, sorted numerically, space-separated.",
            "initial_code": "# Remove duplicates and sort\n",
            "solution_code": "nums = list(map(int, input().split()))\nunique_nums = sorted(list(set(nums)))\nprint(*(unique_nums))\n",
            "test_cases": [{"input": "5 2 8 5 2 1", "expected": "1 2 5 8"}],
        },
    },

    "les-data-types-7-intermediate": {
        "title": "Set Comprehensions & Frozenset",
        "content": """# Set Comprehensions & Frozenset

## 🎯 Learning Objectives
- Use set comprehensions for filtering and transformation
- Understand and use `frozenset` as a hashable set
- Solve mathematical set problems efficiently

## 📚 Concept Overview
### Set Comprehensions
```python
# {expr for item in iterable if condition}
names = ["Alice", "bob", "Alice", "CHARLIE"]
unique_lower = {n.lower() for n in names}
# {'alice', 'bob', 'charlie'}
```

### Frozenset
A `frozenset` is an **immutable** set. Since it's immutable, it's hashable!
```python
# Regular sets cannot be keys
# d = {{1, 2}: "values"} # TypeError

fs = frozenset([1, 2, 3])
d = {fs: "a lucky set"} # Allowed!
```

### Advanced Operations
```python
a = {1, 2, 3}
b = {1, 2}
print(b.issubset(a))   # True
print(a.issuperset(b)) # True
print(a.isdisjoint({4, 5})) # True (no common elements)
```

## 🏆 Key Takeaways
- Use set comprehensions to create unique collections from existing data
- Use `frozenset` when you need a set as a dictionary key or in another set
- `isdisjoint()` is faster than checking if intersection is empty
""",
        "questions": [
            {"text": "Which collection type is hashable and can be used as a dictionary key?", "options": [
                {"text": "frozenset", "correct": True}, {"text": "set", "correct": False},
                {"text": "list", "correct": False}, {"text": "dict", "correct": False}]},
            {"text": "What is the output of `{x % 3 for x in range(10)}`?", "options": [
                {"text": "{0, 1, 2}", "correct": True}, {"text": "{0, 1, 2, ..., 9}", "correct": False},
                {"text": "{1, 2, 0}", "correct": True}, {"text": "{0, 3, 6, 9}", "correct": False}]},
            {"text": "What does `a.isdisjoint(b)` return?", "options": [
                {"text": "True if they have no common elements", "correct": True},
                {"text": "True if a is subset of b", "correct": False},
                {"text": "True if they are equal", "correct": False},
                {"text": "The intersection of a and b", "correct": False}]},
        ],
        "challenge": {
            "title": "Common Words",
            "description": "Read two lines of text. Print the common words (intersection) between them, sorted alphabetically.",
            "initial_code": "# Find common words in two sentences\n",
            "solution_code": "s1 = set(input().split())\ns2 = set(input().split())\ncommon = sorted(list(s1 & s2))\nprint(*(common))\n",
            "test_cases": [{"input": "python is great\nlearning python is fun", "expected": "is python"}],
        },
    },

    "les-data-types-7-pro": {
        "title": "Set Optimization & Mathematical Applications",
        "content": """# Set Optimization & Mathematical Applications

## 🎯 Learning Objectives
- Analyze the time and space complexity of set operations
- Implement Jaccard Similarity and other set metrics
- Use sets for graph algorithms and large-scale deduplication

## 📚 Concept Overview
### Efficiency Analysis
Python sets use exactly the same hash table machinery as dictionaries, but without storing values.
- **Space Complexity**: O(n) — set stores hashes and keys.
- **Set Operations Complexity**:
    - Union (a | b): O(len(a) + len(b))
    - Intersection (a & b): O(min(len(a), len(b)))
    - Difference (a - b): O(len(a))

### Jaccard Similarity
A measure used in data science to compare similarity between sets.
`J(A, B) = |A ∩ B| / |A ∪ B|`

```python
def jaccard(s1, s2):
    intersection = len(s1 & s2)
    union = len(s1 | s2)
    return intersection / union if union > 0 else 0
```

## 🏆 Key Takeaways
- Intersection is O(min(A, B)) because Python iterates over the smaller set
- For huge datasets, use `Bloom Filters` if you can tolerate small false-positive rates with massive space savings
- Proper use of sets can turn O(n²) logic into O(n)
""",
        "questions": [
            {"text": "What is the time complexity of the intersection operation `A & B` in Python?", "options": [
                {"text": "O(min(len(A), len(B)))", "correct": True}, {"text": "O(len(A) + len(B))", "correct": False},
                {"text": "O(len(A) * len(B))", "correct": False}, {"text": "O(1)", "correct": False}]},
            {"text": "Which metric measures similarity as intersection divided by union?", "options": [
                {"text": "Jaccard Similarity", "correct": True}, {"text": "Cosine Similarity", "correct": False},
                {"text": "Euclidean Distance", "correct": False}, {"text": "Hamming Distance", "correct": False}]},
            {"text": "Why are sets faster than lists for checking if an item exists?", "options": [
                {"text": "Hashing allows direct lookup; lists require a linear scan", "correct": True},
                {"text": "Sets are sorted", "correct": False},
                {"text": "Sets use binary search", "correct": False},
                {"text": "Sets are smaller", "correct": False}]},
        ],
        "challenge": {
            "title": "Unique Word Ratio",
            "description": "Read a sentence. Print the ratio of unique words to total words, rounded to 2 decimal places.",
            "initial_code": "# Calculate unique/total ratio\n",
            "solution_code": "words = input().split()\ntotal = len(words)\nunique = len(set(words))\nprint(round(unique / total, 2) if total > 0 else 0.0)\n",
            "test_cases": [{"input": "to be or not to be", "expected": "0.67"}],
        },
    },

    # ── Lesson 8: Choosing the Right Data Structure ──────────────────────────
    "les-data-types-8-beginner": {
        "title": "Choosing the Right Collection",
        "content": """# Choosing the Right Collection

## 🎯 Learning Objectives
- Compare List, Tuple, Set, and Dictionary
- Select the best structure based on problem requirements
- Understand the pros and cons of each type

## 📚 Concept Overview
| Type | Summary | Mutability | Uniqueness | Best For... |
|------|---------|------------|------------|--------------|
| **List** | Ordered items | Mutable | No | General storage, keeping order |
| **Tuple** | Fixed list | Immutable | No | Fixed records, coordinates |
| **Set** | Unique bunch | Mutable | Yes | Deduplication, intersection |
| **Dict** | Mapped pairs | Mutable | Keys unique| Lookups, property storage |

### Decision Flow:
1. Do I need to Map keys to values? → **Dict**
2. Do I need to ensure Uniqueness? → **Set**
3. Is my data Fixed and should not change? → **Tuple**
4. Do I need internal Order and duplicates? → **List**
""",
        "questions": [
            {"text": "Which structure should you use to store unique user IDs?", "options": [
                {"text": "Set", "correct": True}, {"text": "List", "correct": False},
                {"text": "Tuple", "correct": False}, {"text": "Any of them", "correct": False}]},
            {"text": "You need to store (Latitude, Longitude) for a city. Which is best?", "options": [
                {"text": "Tuple", "correct": True}, {"text": "List", "correct": False},
                {"text": "Set", "correct": False}, {"text": "Dictionary", "correct": False}]},
            {"text": "You need to count word occurrences. Which is best?", "options": [
                {"text": "Dictionary", "correct": True}, {"text": "List", "correct": False},
                {"text": "Set", "correct": False}, {"text": "Tuple", "correct": False}]},
        ],
        "challenge": {
            "title": "Smart Storage",
            "description": "You are given a list of tasks. Some repeat. You need to print the task count (unique) and the full task list in original order. Print count first, then the list space-separated.",
            "initial_code": "# Use two different collections to solve this\n",
            "solution_code": "tasks = input().split()\nunique_count = len(set(tasks))\nprint(unique_count)\nprint(*(tasks))\n",
            "test_cases": [{"input": "code test code deploy", "expected": "3\ncode test code deploy"}],
        },
    },

    "les-data-types-8-intermediate": {
        "title": "Standard Library Extensions (Collections)",
        "content": """# Standard Library Extensions (Collections)

## 🎯 Learning Objectives
- Use `deque` for queues and stacks
- Use `OrderedDict` and `ChainMap`
- Use `UserList`, `UserDict` for custom classes

## 📚 Concept Overview
### collections.deque
Double-ended queue. Excellent for O(1) performance at both ends.
```python
from collections import deque
q = deque([1, 2, 3])
q.append(4)
q.appendleft(0)
q.popleft() # 0
```

### collections.ChainMap
Groups multiple dictionaries into a single view.
```python
from collections import ChainMap
defaults = {"color": "red", "user": "guest"}
user_settings = {"color": "blue"}
combined = ChainMap(user_settings, defaults)
print(combined["color"]) # 'blue' (found in first dict)
print(combined["user"])  # 'guest' (found in second)
```

## 🏆 Key Takeaways
- Use `deque` instead of `list.insert(0, ...)`
- `ChainMap` is great for configuration layering (Command line > Env vars > Defaults)
""",
        "questions": [
            {"text": "Which collection provides O(1) appends and pops from both ends?", "options": [
                {"text": "deque", "correct": True}, {"text": "list", "correct": False},
                {"text": "queue", "correct": False}, {"text": "stack", "correct": False}]},
            {"text": "What does ChainMap do?", "options": [
                {"text": "Links multiple dictionaries for unified searching", "correct": True},
                {"text": "Chains lists together", "correct": False},
                {"text": "Creates a sequence of maps", "correct": False},
                {"text": "Is used for blockchain in Python", "correct": False}]},
        ],
        "challenge": {
            "title": "Undo System",
            "description": "Simulate an undo system. Read a sequence of operations. 'write [text]' adds text to history, 'undo' removes the latest. Print the final history content space-separated.",
            "initial_code": "from collections import deque\n# Implement undo with a stack (deque)\n",
            "solution_code": "from collections import deque\nhistory = deque()\nops = int(input())\nfor _ in range(ops):\n    cmd = input().split()\n    if cmd[0] == 'write': history.append(cmd[1])\n    elif cmd[0] == 'undo' and history: history.pop()\nprint(*(history))\n",
            "test_cases": [{"input": "4\nwrite A\nwrite B\nundo\nwrite C", "expected": "A C"}],
        },
    },

    "les-data-types-8-pro": {
        "title": "Persistent Data Structures & Memory Layouts",
        "content": """# Persistent Data Structures & Memory Layouts

## 🎯 Learning Objectives
- Understand the internal C-layout of Python objects
- Explore functional persistent data structures
- Analyze garbage collection impacts of different structures

## 📚 Concept Overview
### Object Memory Layout
Every Python object has a header:
- `ob_refcnt`: Reference count
- `ob_type`: Pointer to the object type

A List is an array of **pointers** to these objects. This is why lists can hold different types, but also why they are slower than C-arrays (indirection).

### Persistent Data Structures
Instead of mutating, they return a new structure while sharing most memory with the old one (Structural Sharing).

## 🏆 Key Takeaways
- Indirection in Python collections (pointers to objects) causes cache misses
- For high-performance numeric arrays, use `numpy` or `array.array`
- Understand reference counting to avoid memory leaks in circular structures
""",
        "questions": [
            {"text": "What does a Python list store internally?", "options": [
                {"text": "An array of pointers to objects", "correct": True},
                {"text": "The raw bytes of objects", "correct": False},
                {"text": "A linked list of values", "correct": False},
                {"text": "A hash table", "correct": False}]},
            {"text": "What are the two items in a standard Python object header?", "options": [
                {"text": "Reference count and type pointer", "correct": True},
                {"text": "Value and ID", "correct": False},
                {"text": "Size and Name", "correct": False},
                {"text": "Pointer and Value", "correct": False}]},
        ],
        "challenge": {
            "title": "Memory Saved?",
            "description": "Calculate size of a list vs array.array for 1000 integers. Just print 'Array is smaller' if it occupies less space in memory based on sys.getsizeof.",
            "initial_code": "import sys, array\n# Compare memory of list and array\n",
            "solution_code": "import sys, array\nl = list(range(1000))\na = array.array('i', range(1000))\nif sys.getsizeof(a) < sys.getsizeof(l): print('Array is smaller')\n",
            "test_cases": [{"input": "", "expected": "Array is smaller"}],
        },
    },

    # ── Lesson 9: None & Identity ────────────────────────────────────────────
    "les-data-types-9-beginner": {
        "title": "None Type & Object Identity",
        "content": """# None Type & Object Identity

## 🎯 Learning Objectives
- Use `None` to represent absence of value
- Compare objects using `is` vs `==`
- Understand the Singleton pattern for `None`

## 📚 Concept Overview
### The None Object
`None` is a special constant in Python used to represent nothingness or null. It is the only instance of the `NoneType`.

```python
x = None
if x is None:
    print("x has no value")
```

### Identity (is) vs Equality (==)
- `==` checks if values are **Equal** (content)
- `is` checks if they are the **Same object** (memory address)

```python
a = [1, 2]
b = [1, 2]
print(a == b) # True  (same content)
print(a is b) # False (different objects)
```

## 🏆 Key Takeaways
- Always use `is None` to check for `None`
- `None` is a Singleton (only one exists in memory)
- Functions that don't return anything return `None` by default
""",
        "questions": [
            {"text": "Which operator should you use to check if x is None?", "options": [
                {"text": "is", "correct": True}, {"text": "==", "correct": False},
                {"text": "===", "correct": False}, {"text": "=", "correct": False}]},
            {"text": "What type is None?", "options": [
                {"text": "NoneType", "correct": True}, {"text": "Null", "correct": False},
                {"text": "void", "correct": False}, {"text": "Object", "correct": False}]},
            {"text": "If a function has no return statement, what does it return?", "options": [
                {"text": "None", "correct": True}, {"text": "False", "correct": False},
                {"text": "0", "correct": False}, {"text": "Error", "correct": False}]},
        ],
        "challenge": {
            "title": "Safety Checker",
            "description": "Read a value. If the value is 'None' (string), set x = None, else set x = value. Print 'Status: Empty' if x is None, else print 'Status: Full'.",
            "initial_code": "# Use 'is None' check\n",
            "solution_code": "val = input()\nx = None if val == 'None' else val\nprint('Status: Empty' if x is None else 'Status: Full')\n",
            "test_cases": [{"input": "None", "expected": "Status: Empty"}, {"input": "hello", "expected": "Status: Full"}],
        },
    },

    "les-data-types-9-intermediate": {
        "title": "Interning & Object Caching",
        "content": """# Interning & Object Caching

## 🎯 Learning Objectives
- Understand integer and string interning
- Recognize how Python optimizes small object memory
- Predict identity comparison results

## 📚 Concept Overview
### Integer Interning
Python caches integers from **-5 to 256**.
```python
a = 256
b = 256
print(a is b) # True (cached)

a = 257
b = 257
print(a is b) # False (usually - depending on interpreter/context)
```

### String Interning
Python automatically interns some strings (like identifiers).
```python
a = "hello"
b = "hello"
print(a is b) # True
```

## 🏆 Key Takeaways
- Identity checks (`is`) are faster than equality checks (`==`)
- Don't rely on `is` for numbers/strings in logic, as behavior can change
- Use `sys.intern(s)` to manually cache long strings for fast comparison
""",
        "questions": [
            {"text": "What is the range of integers Python interns by default?", "options": [
                {"text": "-5 to 256", "correct": True}, {"text": "0 to 100", "correct": False},
                {"text": "-128 to 127", "correct": False}, {"text": "All integers", "correct": False}]},
            {"text": "Why does Python intern some objects?", "options": [
                {"text": "To save memory and speed up comparisons", "correct": True},
                {"text": "To prevent them from being changed", "correct": False},
                {"text": "To make them globally accessible", "correct": False},
                {"text": "It is a security feature", "correct": False}]},
        ],
        "challenge": {
            "title": "Interning Test",
            "description": "Read an integer. Compare it to another instance of the same integer using 'is'. Print 'Cached' if same object, else 'Not Cached'.",
            "initial_code": "import sys\n# Check if integer is cached\n",
            "solution_code": "n1 = int(input())\nn2 = int(str(n1))\nprint('Cached' if n1 is n2 else 'Not Cached')\n",
            "test_cases": [{"input": "100", "expected": "Cached"}, {"input": "1000", "expected": "Not Cached"}],
        },
    },

    "les-data-types-9-pro": {
        "title": "Garbage Collection & Weak References",
        "content": """# Garbage Collection & Weak References

## 🎯 Learning Objectives
- Understand CPython's reference counting and cyclic GC
- Use `weakref` to avoid memory leaks
- Profile memory usage with `gc` module

## 📚 Concept Overview
### Reference Counting
Python tracks how many references point to an object. When it hits zero, it's deleted.

### Cyclic Garbage Collector
Reference counting fails on **Cycles** (A points to B, B points to A). Python has a separate GC to find and break these cycles.

### Weak Reference
A reference that doesn't increase the count.
```python
import weakref
class Large: pass
obj = Large()
r = weakref.ref(obj)
# If obj is deleted, r() becomes None
```
""",
        "questions": [
            {"text": "What is the primary way Python manages memory?", "options": [
                {"text": "Reference Counting", "correct": True}, {"text": "Manual Deallocation", "correct": False},
                {"text": "Generational Stop-the-World GC", "correct": False}, {"text": "ARC", "correct": False}]},
            {"text": "What can cause memory leaks in simple reference counting?", "options": [
                {"text": "Reference Cycles", "correct": True}, {"text": "Small integers", "correct": False},
                {"text": "Global variables", "correct": False}, {"text": "Large Lists", "correct": False}]},
        ],
        "challenge": {
            "title": "Weak Ref Check",
            "description": "Create an object, attach a weak reference to it. Delete the strong reference. Print 'True' if the weak reference returns None, else 'False'.",
            "initial_code": "import weakref\n# Test weakref behavior after del\n",
            "solution_code": "import weakref\nclass Obj: pass\no = Obj()\nr = weakref.ref(o)\ndel o\nprint(True if r() is None else False)\n",
            "test_cases": [{"input": "", "expected": "True"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-data-types-10-beginner": {
        "title": "Project: Inventory System",
        "content": """# Project: Inventory System

## 🎯 Goal
Build a small inventory management tool using Dictionaries and Lists.

## 📝 Requirements
- Add items with quantities
- Update quantities
- View total inventory

```python
inventory = {}

def add_item(name, qty):
    inventory[name] = inventory.get(name, 0) + qty

add_item("apple", 10)
add_item("banana", 5)
add_item("apple", 2) # total 12

for item, qty in inventory.items():
    print(f"{item}: {qty}")
```
""",
        "questions": [
            {"text": "Which structure is best for storing item names and their stock quantities?", "options": [
                {"text": "Dictionary", "correct": True}, {"text": "Set", "correct": False},
                {"text": "List", "correct": False}, {"text": "Tuple", "correct": False}]},
            {"text": "How do you safely add to a quantity in a dictionary if the key might not exist?", "options": [
                {"text": "d[key] = d.get(key, 0) + val", "correct": True}, {"text": "d[key] += val", "correct": False},
                {"text": "d.update(key, val)", "correct": False}, {"text": "if key: d[key] += val", "correct": False}]},
        ],
        "challenge": {
            "title": "Inventory Manager",
            "description": "Read N commands: 'add name quantity'. Print the final inventory sorted by name.",
            "initial_code": "inv = {}\n# Process inventory commands\n",
            "solution_code": "n = int(input())\ninv = {}\nfor _ in range(n):\n    _, name, qty = input().split()\n    inv[name] = inv.get(name, 0) + int(qty)\nfor name in sorted(inv.keys()):\n    print(f'{name} {inv[name]}')\n",
            "test_cases": [{"input": "3\nadd apple 10\nadd banana 5\nadd apple 2", "expected": "apple 12\nbanana 5"}],
        },
    },

    "les-data-types-10-intermediate": {
        "title": "Project: Text Analyzer Pro",
        "content": """# Project: Text Analyzer Pro

## 🎯 Goal
Build a tool that analyzes a large text and provides statistics.

## 📝 Features
- Word frequency counting (Counter)
- Unique word set
- Sentence count
- Average word length

## 💻 Logic Sketch
```python
from collections import Counter

text = "Python is great. Learning Python is fun."
words = text.lower().replace(".", "").split()
counts = Counter(words)
unique = set(words)
```
""",
        "questions": [
            {"text": "Which tool provides the fastest way to get the top 5 most common words?", "options": [
                {"text": "Counter.most_common(5)", "correct": True}, {"text": "Sorted Dictionary", "correct": False},
                {"text": "Set of words", "correct": False}, {"text": "Loop through list", "correct": False}]},
        ],
        "challenge": {
            "title": "Text Stat Pro",
            "description": "Read a sentence. Print: Total Words, Unique Words, and the Most Common Word. (If tie, first one).",
            "initial_code": "from collections import Counter\n# Print word statistics\n",
            "solution_code": "from collections import Counter\nwords = input().split()\ncounts = Counter(words)\nprint(f'Total: {len(words)}')\nprint(f'Unique: {len(set(words))}')\nprint(f'Most Common: {counts.most_common(1)[0][0]}')\n",
            "test_cases": [{"input": "apple banana apple apple cherry", "expected": "Total: 5\nUnique: 3\nMost Common: apple"}],
        },
    },

    "les-data-types-10-pro": {
        "title": "Project: Performance Benchmarker",
        "content": """# Project: Performance Benchmarker

## 🎯 Goal
Verify the theoretical time complexity of Python data structures with code.

## 📝 Tasks
- Compare `in` operator for List vs Set with 1,000,000 items
- Measure memory of regular Dict vs Compact Dict
- Use `timeit` for precision

```python
import timeit
data_list = list(range(1000000))
data_set = set(data_list)

# Test 'in' speed
t1 = timeit.timeit('999999 in data_list', globals=globals(), number=100)
t2 = timeit.timeit('999999 in data_set', globals=globals(), number=100)
print(f"List: {t1}, Set: {t2}")
```
""",
        "questions": [
            {"text": "Which module is designed for measuring execution time of small code snippets?", "options": [
                {"text": "timeit", "correct": True}, {"text": "time", "correct": False},
                {"text": "datetime", "correct": False}, {"text": "calendar", "correct": False}]},
        ],
        "challenge": {
            "title": "Is Set Faster?",
            "description": "Create a list of 10000 numbers and a set of same numbers. Print 'Set is Faster' if set lookup for the last element is at least 2 times faster than list lookup.",
            "initial_code": "import timeit\n# Compare lookup speeds\n",
            "solution_code": "import timeit\nl = list(range(10000))\ns = set(l)\nt_l = timeit.timeit('9999 in l', globals=locals(), number=1000)\nt_s = timeit.timeit('9999 in s', globals=locals(), number=1000)\nif t_l > 2 * t_s: print('Set is Faster')\n",
            "test_cases": [{"input": "", "expected": "Set is Faster"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 2 Data Types Lessons 6-10"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 2 (6-10)"))
