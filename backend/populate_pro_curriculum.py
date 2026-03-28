import os
import django
import sys

# Set up Django environment
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge, Quiz, Question

def generate_pro_markdown(title, objective, introduction, syntax_code, best_practices, takeaways):
    return f"""# {title}

## Objective
{objective}

## Conceptual Overview
{introduction}

## Technical Implementation & Syntax
```python
{syntax_code}
```

## Professional Best Practices
{best_practices}

## Key Takeaways
- {takeaways[0]}
- {takeaways[1]}
- {takeaways[2]}
"""

CURRICULUM = [
    {
        "module": ("Python Core Foundations", "High-fidelity essentials for professional Python development, covering variables, memory allocation, and bitwise logic.", 1),
        "topics": [
            ("Variables & Memory", "references", "x=1", "use snake_case", ["Refs", "L-values", "Memory"]),
            ("Mutability", "change objects", "l=[1]", "use tuples", ["Lists", "Strings", "Tuples"]),
            ("Truthiness", "logic bool", "if x:", "bool()", ["True", "False", "None"]),
            ("Type Hinting", "static hints", "x: int = 1", "mypy", ["int", "str", "hints"]),
            ("Bitwise Ops", "binary logic", "x & y", "masking", ["And", "Or", "Xor"]),
            ("Constants", "fixed data", "MAX=100", "final", ["Caps", "PEP8", "Enum"])
        ]
    },
    {
        "module": ("Control Flow & Logic", "Loop optimization and pattern matching.", 2),
        "topics": [
            ("Conditionals", "if/else", "if x: pass", "nesting", ["if", "elif", "else"]),
            ("Match Statements", "structural pattern", "match x:", "3.10+", ["case", "match", "wildcard"]),
            ("List Comprehensions", "efficient lists", "[x for x in l]", "dont over-nest", ["List", "Inline", "Speed"]),
            ("Dict/Set Comp", "mappings/sets", "{x:y for x,y in l}", "uniqueness", ["Dict", "Set", "3.x"]),
            ("Enumeration", "index iterate", "for i, x in enumerate(l)", "avoid len()", ["Index", "Value", "Iter"]),
            ("Parallel Zipping", "multi iter", "for a, b in zip(l1, l2)", "strict=True", ["Zip", "Iter", "Strict"])
        ]
    },
    {
        "module": ("Functions & Closures", "Functional programming and advanced scoping.", 3),
        "topics": [
            ("Args & Kwargs", "variadic params", "def f(*a, **k)", "packing", ["args", "kwargs", "flexible"]),
            ("Unpacking", "destructuring", "a, b = [1, 2]", "star unpacking", ["Tuple", "List", "Assign"]),
            ("Closures", "nested scope", "def outer(): def inner():", "nonlocal", ["Scope", "Memory", "State"]),
            ("Decorators", "wrap funcs", "@dec def f():", "wraps", ["Wrap", "Meta", "Logic"]),
            ("Parametrized Dec", "args in dec", "@dec(arg) def f():", "3 nested levels", ["Factory", "Arg", "DSL"]),
            ("Lambda Internals", "anonymous funcs", "f = lambda x: x", "readability", ["Map", "Filter", "Inline"])
        ]
    },
    {
        "module": ("Data Structures & Performance", "Specialized collections and complexity.", 4),
        "topics": [
            ("Set Theory", "unique logic", "s = {1, 2}", "intersection", ["Set", "Union", "Diff"]),
            ("Dict Performance", "hash tables", "d = {k: v}", "collisions", ["Hash", "Key", "O(1)"]),
            ("Collections Module", "specialized data", "from collections import Counter", "use Counter", ["Deque", "Counter", "Default"]),
            ("NamedTuples", "structured data", "from collections import namedtuple", "readability", ["Tuple", "Named", "Class"]),
            ("Dataclasses", "boilerplate-free", "@dataclass class X:", "frozen=True", ["Data", "Class", "Type"]),
            ("Complexity (O)", "Big O analysis", "O(1) vs O(n)", "scalability", ["Complexity", "Time", "Space"])
        ]
    },
    {
        "module": ("OOP: The Basics", "Class architecture and instance management.", 5),
        "topics": [
            ("Classes & Self", "object blueprints", "class X: def f(self):", "self naming", ["Class", "Inst", "Self"]),
            ("Init vs New", "constructor/alloc", "def __init__(self):", "allocation", ["Init", "New", "Alloc"]),
            ("Attributes", "data storage", "self.x = 1", "private __x", ["Inst", "Class", "Attr"]),
            ("Properties", "managed attrs", "@property", "getters", ["Prop", "Setter", "Logic"]),
            ("Static Methods", "stateless funcs", "@staticmethod", "namespaces", ["Static", "ClassMethod", "Tool"]),
            ("Encapsulation", "data hiding", "setters/getters", "protection", ["Private", "Public", "API"])
        ]
    },
    {
        "module": ("Advanced OOP Patterns", "Inheritance, MRO, and Protocols.", 6),
        "topics": [
            ("Inheritance", "code reuse", "class B(A):", "dry", ["Base", "Sub", "Extend"]),
            ("Super()", "chain parent", "super().__init__()", "delegation", ["Super", "Parent", "Chain"]),
            ("MRO", "method resolution", "X.mro()", "c3 linear", ["Diamond", "Resolution", "Order"]),
            ("ABCs", "abstract bases", "from abc import ABC", "interfaces", ["Abstract", "Base", "Interface"]),
            ("Mixins", "flavor patterns", "class X(Mixin, Base):", "orthogonality", ["Mixin", "Plug", "Extend"]),
            ("Protocols", "duck typing", "from typing import Protocol", "structural", ["Static", "Duck", "Strict"])
        ]
    },
    {
        "module": ("Resource Management", "Managing files, memory, and connections.", 7),
        "topics": [
            ("Context Managers", "scoped logic", "with open() as f:", "__enter__", ["With", "Enter", "Exit"]),
            ("Contextlib", "decorator cm", "@contextmanager", "yield", ["yield", "lib", "tool"]),
            ("File I/O", "reading/writing", "f.read()", "buffering", ["Read", "Write", "Open"]),
            ("Serialization", "data format", "import json", "security", ["JSON", "Pickle", "Data"]),
            ("Garbage Collection", "gc internals", "gc.collect()", "cycles", ["Heap", "Stack", "GC"]),
            ("Memory Views", "buffer protocol", "memoryview(b)", "no-copy", ["Bytes", "Buffer", "View"])
        ]
    },
    {
        "module": ("Error Handling & Maintenance", "Robustness, logging, and testing.", 8),
        "topics": [
            ("Exception Tree", "error hierarchy", "except Exception:", "hierarchy", ["Catch", "Raise", "Finally"]),
            ("Custom Errors", "domain specific", "class MyError(Exception):", "clarity", ["Error", "Custom", "Domain"]),
            ("Logging", "event tracking", "import logging", "levels", ["Log", "Info", "Error"]),
            ("Unit Testing", "code quality", "import unittest", "assertions", ["Test", "Assert", "Mock"]),
            ("Assertions", "internal checks", "assert x > 0", "debug only", ["Assert", "Check", "Invariant"]),
            ("PDB Debugger", "tracing code", "breakpoint()", "n, s, c", ["Debug", "Break", "Step"])
        ]
    },
    {
        "module": ("Practical Data & Web", "Standard libraries for web and analytics.", 9),
        "topics": [
            ("Pathlib", "path logic", "from pathlib import Path", "cross-platform", ["Path", "Dir", "Link"]),
            ("CSV & Excel", "tabular data", "import csv", "pandas", ["CSV", "Excel", "Data"]),
            ("Requests API", "http client", "requests.get()", "json", ["GET", "POST", "HTTP"]),
            ("BeautifulSoup", "scraping", "from bs4 import BeautifulSoup", "tags", ["HTML", "Scrape", "Selector"]),
            ("RegEx", "patterns", "import re", "greedy", ["Regex", "Match", "Find"]),
            ("SQLite", "database", "import sqlite3", "transaction", ["SQL", "Db", "Acid"])
        ]
    },
    {
        "module": ("Advanced Python: Async", "Modern Concurrency, Iterators, and Generators.", 10),
        "topics": [
            ("Iterators", "iterator protocol", "iter(x)", "next", ["Iter", "Loop", "Next"]),
            ("Generators", "lazy sequences", "yield x", "memory", ["Yield", "Memory", "Lazy"]),
            ("Itertools", "combinatorics", "from itertools import count", "efficiency", ["Count", "Chain", "Cycle"]),
            ("Async Basics", "concurrency", "async def f():", "event loop", ["Async", "Await", "Loop"]),
            ("Threading", "io parallel", "from threading import Thread", "GIL", ["IO", "Thread", "Lock"]),
            ("Processing", "cpu parallel", "from multiprocessing import Process", "cores", ["CPU", "Process", "Pool"])
        ]
    }
]

def populate():
    print("Starting Professional Triple-Level Seeding...")
    for mod_info in CURRICULUM:
        m_title, m_desc, m_order = mod_info["module"]
        # Use exact field names from models.py
        m = Module.objects.create(title=m_title, description=m_desc, order=m_order)
        print(f"Created Module: {m_title}")
        
        for t_idx, topic in enumerate(mod_info["topics"]):
            t_title, t_obj, t_code, t_best, t_keys = topic
            
            for level in ["Beginner", "Intermediate", "Pro"]:
                content = generate_pro_markdown(
                    f"{t_title} ({level})",
                    f"Master {t_title} at a {level} level.",
                    f"This lesson provides a deep technical analysis of {t_title} for {level} developers.",
                    f"# Example of {t_title}\n{t_code}",
                    f"Professional context: {t_best}.",
                    [t_keys[0], t_keys[1], f"Applied {level} constraints."]
                )
                
                # Lesson uses module_id
                lesson = Lesson.objects.create(
                    module_id=m.id,
                    title=t_title,
                    slug=f"{t_title.lower().replace(' ', '-')}-{level.lower()}",
                    content=content,
                    order=t_idx + 1,
                    difficulty=level,
                    duration=15
                )
                
                # Quiz uses lesson_id
                quiz = Quiz.objects.create(lesson_id=lesson.id, title=f"Checkpoint: {t_title}")
                
                # Question uses quiz_id
                Question.objects.create(
                    quiz_id=quiz.id,
                    text=f"Which is a key concept of {t_title} in {level} context?",
                    options=[
                        {"text": t_keys[0], "correct": True},
                        {"text": "Placeholder concept", "correct": False}
                    ],
                    points=1
                )
                
                # Challenge uses lesson_id, snake_case fields
                Challenge.objects.create(
                    lesson_id=lesson.id,
                    title=f"Logic: {t_title}",
                    description=f"Implement the logic for {t_title} using professional Python syntax.",
                    initial_code=f"def solution():\n    # {t_obj}\n    pass",
                    solution_code=f"def solution():\n    return '{t_code}'",
                    test_cases=[{"input": "", "output": t_code}],
                    points=10,
                    difficulty=level
                )
                
    print(f"Seeding complete! 10 Modules, 60 Topics, 180 Lessons created.")

if __name__ == "__main__":
    populate()
