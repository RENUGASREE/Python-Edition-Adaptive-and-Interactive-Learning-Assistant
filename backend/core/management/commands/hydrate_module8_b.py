"""python manage.py hydrate_module8_b -- Module 8 OOP Lessons 6-10"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 6: Encapsulation ──────────────────────────────────────────────
    "les-oop-6-beginner": {
        "title": "Private vs Public",
        "content": """# Private vs Public

## 🎯 Learning Objectives
- Use the single underscore `_` for "Internal" data
- Use the double underscore `__` for "Private" data
- Understand Python's philosophy: "We are all consenting adults here"

## 📚 Concept Overview
In Python, there is no hard "Private" keyword like in Java. We use naming conventions.

- `_variable`: "Please don't change this, it's for internal use."
- `__variable`: "Seriously, don't touch this!" (Triggers name mangling).

```python
class Secret:
    def __init__(self):
        self._hint = "123" # Protected
        self.__code = "TOP-SECRET" # Private (Mangling)
```

## 🏆 Key Takeaways
- The `_` prefix is a hint to other developers.
- `__` makes it harder (but not impossible) to access data from outside the class.
""",
        "questions": [
            {"text": "What does a single underscore prefix (e.g. _name) indicate in Python?", "options": [
                {"text": "The attribute is intended for internal use only", "correct": True},
                {"text": "The attribute is public", "correct": False},
                {"text": "The attribute is global", "correct": False},
                {"text": "The attribute is a constant", "correct": False}]},
            {"text": "What happens when you use a double underscore prefix (e.g. __name)?", "options": [
                {"text": "Name mangling occurs (renaming it to _ClassName__name)", "correct": True},
                {"text": "The variable is encrypted", "correct": False},
                {"text": "The variable is deleted from memory", "correct": False},
                {"text": "It becomes a static variable", "correct": False}]},
        ],
        "challenge": {
            "title": "Hidden Data",
            "description": "Define a class `Safe` with a private attribute `__key`. If you try to print `obj.__key` from outside, it will fail. Print 'Hidden'.",
            "initial_code": "# Private attr\n",
            "solution_code": "class Safe:\n    def __init__(self): self.__key = 1\ns = Safe()\ntry: print(s.__key)\nexcept AttributeError: print('Hidden')\n",
            "test_cases": [{"input": "", "expected": "Hidden"}],
        },
    },

    "les-oop-6-intermediate": {
        "title": "Name Mangling Explained",
        "content": """# Name Mangling Explained

## 🎯 Learning Objectives
- Access "Private" attributes from outside correctly
- Avoid attribute collisions in inheritance
- Understand the internal renaming mechanism

## 📚 Concept Overview
If a class `User` has `__id`, Python renames it to `_User__id`.

```python
class User:
    def __init__(self):
        self.__id = 42

u = User()
# print(u.__id) # Attribute Error!
print(u._User__id) # 42 (The mangled name)
```

## 🏆 Key Takeaways
- Name mangling is mostly used to prevent name clashes in child classes.
""",
        "questions": [
            {"text": "If class 'Person' has a private attribute '__pin', what is its mangled name?", "options": [
                {"text": "_Person__pin", "correct": True}, {"text": "__Person_pin", "correct": False},
                {"text": "_pin_Person", "correct": False}, {"text": "Person.__pin", "correct": False}]},
        ],
        "challenge": {
            "title": "Mangle Access",
            "description": "Create instance of `Box` with `self.__data = 'Gold'`. Print the data using its MANGLED name.",
            "initial_code": "class Box:\n    def __init__(self): self.__data = 'Gold'\nb = Box()\n# Print mangled\n",
            "solution_code": "class Box:\n    def __init__(self): self.__data = 'Gold'\nb = Box()\nprint(b._Box__data)\n",
            "test_cases": [{"input": "", "expected": "Gold"}],
        },
    },

    "les-oop-6-pro": {
        "title": "Encapsulation Design Patterns",
        "content": """# Encapsulation Design Patterns

## 🎯 Learning Objectives
- Discuss the "Data Hiding" vs "Abstraction"
- Use properties to enforce consistency
- Learn about `__slots__` for memory optimization

## 📚 Concept Overview
`__slots__` tells Python not to create a `__dict__` for each object. This saves massive amounts of RAM when you have millions of small objects.

```python
class Point:
    __slots__ = ('x', 'y') # Only these two variables allowed!
```

## ️🏆 Key Takeaways
- Good encapsulation means the user doesn't need to know **how** the object works, just **what** it can do.
""",
        "questions": [
            {"text": "Which special attribute allows you to optimize memory by preventing the creation of an instance dictionary?", "options": [
                {"text": "__slots__", "correct": True}, {"text": "__dict__", "correct": False},
                {"text": "__lock__", "correct": False}, {"text": "__fast__", "correct": False}]},
        ],
        "challenge": {
            "title": "Memory Saver",
            "description": "Define a class `Coord` that only allows `x` and `y` using slots. Try to add `z = 10` to an instance and catch the `AttributeError`. Print 'No Z'.",
            "initial_code": "class Coord:\n    __slots__ = ('x', 'y')\n# Test slotting\n",
            "solution_code": "class Coord:\n    __slots__ = ('x', 'y')\nc = Coord()\ntry: c.z = 10\nexcept AttributeError: print('No Z')\n",
            "test_cases": [{"input": "", "expected": "No Z"}],
        },
    },

    # ── Lesson 7: Inheritance ────────────────────────────────────────────────
    "les-oop-7-beginner": {
        "title": "Inheritance Basics",
        "content": """# Inheritance Basics

## 🎯 Learning Objectives
- Extend functionality from a Parent class to a Child class
- Reuse code effectively
- Understand the "Is-A" relationship

## 📚 Concept Overview
```python
class Animal:
    def breathe(self): print("Breathing...")

class Dog(Animal):
    def bark(self): print("Woof!")

d = Dog()
d.breathe() # Inherited from Animal!
```

- **Parent (Base)**: `Animal`
- **Child (Derived)**: `Dog` (A Dog **is an** Animal)

## 🏆 Key Takeaways
- Inheritance reduces duplication by putting shared logic in the parent.
""",
        "questions": [
            {"text": "If class 'Bird' inherits from class 'Animal', which one is the child?", "options": [
                {"text": "Bird", "correct": True}, {"text": "Animal", "correct": False},
                {"text": "Both", "correct": False}, {"text": "Neither", "correct": False}]},
            {"text": "What is the primary goal of inheritance?", "options": [
                {"text": "Code reuse and logical organization", "correct": True},
                {"text": "Encryption", "correct": False},
                {"text": "Making code run faster", "correct": False},
                {"text": "Generating documentation", "correct": False}]},
        ],
        "challenge": {
            "title": "Inheritance Test",
            "description": "Define `Parent` with `hello()`. Define `Child` that inherits from it. Call `hello` on a Child instance.",
            "initial_code": "# Inheritance\n",
            "solution_code": "class Parent:\n    def hello(self): print('Hi')\nclass Child(Parent): pass\nc = Child()\nc.hello()\n",
            "test_cases": [{"input": "", "expected": "Hi"}],
        },
    },

    "les-oop-7-intermediate": {
        "title": "The super() Function",
        "content": """# The super() Function

## 🎯 Learning Objectives
- Call parent methods from within a child
- Extend the `__init__` method without overriding it completely
- Pass arguments up the inheritance chain

## 📚 Concept Overview
```python
class Employee:
    def __init__(self, name): self.name = name

class Developer(Employee):
    def __init__(self, name, lang):
        super().__init__(name) # Call parent init
        self.lang = lang
```

## 🏆 Key Takeaways
- `super()` lets you build on top of existing logic rather than rewriting it.
""",
        "questions": [
            {"text": "How do you call the parent class's version of a method from the child class?", "options": [
                {"text": "super().method_name()", "correct": True},
                {"text": "parent.method_name()", "correct": False},
                {"text": "self.parent.method_name()", "correct": False},
                {"text": "base.method_name()", "correct": False}]},
        ],
        "challenge": {
            "title": "Super Init",
            "description": "Child `C` inherits from `P`. `P.__init__` takes `x`. Make `C.__init__` take `x` and `y`, calling `super().__init__(x)`. Print their sum.",
            "initial_code": "# super usage\n",
            "solution_code": "class P:\n    def __init__(self, x): self.x = x\nclass C(P):\n    def __init__(self, x, y):\n        super().__init__(x)\n        self.y = y\nobj = C(10, 20)\nprint(obj.x + obj.y)\n",
            "test_cases": [{"input": "", "expected": "30"}],
        },
    },

    "les-oop-7-pro": {
        "title": "Method Resolution Order (MRO)",
        "content": """# Method Resolution Order (MRO)

## 🎯 Learning Objectives
- Understand how Python finds methods in complex trees
- Learn the C3 Linearization algorithm (conceptually)
- Inspect the `.mro()` of a class

## 📚 Concept Overview
When a class has multiple parents, which one "wins" if they both have the same method? Python uses a deterministic order called MRO.

```python
class A: pass
class B(A): pass
class C(A): pass
class D(B, C): pass

print(D.mro()) # [D, B, C, A, Object]
```

## 🏆 Key Takeaways
- Use `help(MyClass)` or `MyClass.mro()` to see the search path.
""",
        "questions": [
            {"text": "What does MRO stand for in Python OOP?", "options": [
                {"text": "Method Resolution Order", "correct": True},
                {"text": "Module Resource Optimization", "correct": False},
                {"text": "Manual Reset Option", "correct": False},
                {"text": "Main Runtime Object", "correct": False}]},
        ],
        "challenge": {
            "title": "MRO Print",
            "description": "Define `X`, then `Y(X)`. Print the MRO of `Y` (just the class names as strings).",
            "initial_code": "class X: pass\nclass Y(X): pass\n# print MRO list\n",
            "solution_code": "class X: pass\nclass Y(X): pass\nprint([c.__name__ for c in Y.mro()])\n",
            "test_cases": [{"input": "", "expected": "['Y', 'X', 'object']"}],
        },
    },

    # ── Lesson 8: Polymorphism ───────────────────────────────────────────────
    "les-oop-8-beginner": {
        "title": "Polymorphism Basics",
        "content": """# Polymorphism Basics

## 🎯 Learning Objectives
- Multiple classes sharing the same interface
- Call the same method on different objects and get different results
- Build generic functions that work with many types

## 📚 Concept Overview
"Many forms" (Poly-morphism).

```python
class Cat: 
    def speak(self): return "Meow"
class Dog: 
    def speak(self): return "Woof"

animals = [Cat(), Dog()]
for a in animals:
    print(a.speak()) # Same name, different output!
```

## 🏆 Key Takeaways
- Polymorphism allows you to treat different objects as the same family.
""",
        "questions": [
            {"text": "What is 'Polymorphism'?", "options": [
                {"text": "The ability of different classes to respond to the same method call in their own way", "correct": True},
                {"text": "A way to hide private data", "correct": False},
                {"text": "A tool to compile code manually", "correct": False},
                {"text": "A method to delete objects", "correct": False}]},
        ],
        "challenge": {
            "title": "Speaker System",
            "description": "Create two classes `A` and `B` both with a method `go()`. Print 'A' and 'B' respectively. Loop through a list of both and call `go()`.",
            "initial_code": "# Polymorphism\n",
            "solution_code": "class A: def go(self): print('A')\nclass B: def go(self): print('B')\nfor x in [A(), B()]: x.go()\n",
            "test_cases": [{"input": "", "expected": "A\nB"}],
        },
    },

    "les-oop-8-intermediate": {
        "title": "Abstract Base Classes (ABC)",
        "content": """# Abstract Base Classes (ABC)

## 🎯 Learning Objectives
- Enforce that child classes MUST implement certain methods
- Use the `abc` module
- Prevent instantiation of the parent class

## 📚 Concept Overview
An **Abstract Class** is a blueprint that cannot be used by itself.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self): pass

# s = Shape() # ERROR!
class Square(Shape):
    def area(self): return 100
```

## 🏆 Key Takeaways
- Use ABCs to design rigid frameworks that others can build on.
""",
        "questions": [
            {"text": "Which module allows you to define Abstract Base Classes?", "options": [
                {"text": "abc", "correct": True}, {"text": "sys", "correct": False},
                {"text": "base", "correct": False}, {"text": "abstract", "correct": False}]},
            {"text": "Can you create an instance of an Abstract class directly?", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only if it has no methods", "correct": False},
                {"text": "Only in Python 2", "correct": False}]},
        ],
        "challenge": {
            "title": "ABCs in Action",
            "description": "Inherit from `ABC`. Define `@abstractmethod` `run()`. Ensure child `C` implements it and prints 'Running'.",
            "initial_code": "from abc import ABC, abstractmethod\n# Setup ABC\n",
            "solution_code": "from abc import ABC, abstractmethod\nclass B(ABC):\n    @abstractmethod\n    def run(self): pass\nclass C(B):\n    def run(self): print('Running')\nC().run()\n",
            "test_cases": [{"input": "", "expected": "Running"}],
        },
    },

    "les-oop-8-pro": {
        "title": "Protocol & Duck Typing",
        "content": """# Protocol & Duck Typing

## 🎯 Learning Objectives
- Understand "If it walks like a duck and quacks like a duck..."
- Use `typing.Protocol` for structural subtyping
- Dynamic vs Static polymorphism

## 📚 Concept Overview
In Python, you don't *need* inheritance for polymorphism. You just need the method to exist!

```python
def make_fly(obj):
    obj.fly() # As long as obj has a .fly() method, it works!
```

In modern Python, we use `typing.Protocol` to define these expectations formally for Type Checkers (like MyPy).

## 🏆 Key Takeaways
- Duck Typing is the foundation of Python's extreme flexibility.
""",
        "questions": [
            {"text": "What is 'Duck Typing'?", "options": [
                {"text": "Relying on an object's behavior (methods) rather than its actual class type", "correct": True},
                {"text": "A way to draw ducks", "correct": False},
                {"text": "A special class for birds", "correct": False},
                {"text": "A memory management technique", "correct": False}]},
        ],
        "challenge": {
            "title": "Duck Logic",
            "description": "Write a function `do(obj)` that calls `obj.start()`. Test it with a random class that has a `start()` method.",
            "initial_code": "def do(obj):\n    # call start\n",
            "solution_code": "def do(obj): obj.start()\nclass Any: def start(self): print('GO')\ndo(Any())\n",
            "test_cases": [{"input": "", "expected": "GO"}],
        },
    },

    # ── Lesson 9: Operator Overloading ───────────────────────────────────────
    "les-oop-9-beginner": {
        "title": "Magic Methods (__add__)",
        "content": """# Magic Methods (__add__)

## 🎯 Learning Objectives
- Use arithmetic operators (+, -, *, /) with your custom objects
- Understand the `__add__` and `__sub__` methods
- Build intuitive mathematical classes

## 📚 Concept Overview
```python
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

v1 = Vector(1, 1)
v2 = Vector(2, 2)
v3 = v1 + v2 # Calls v1.__add__(v2)
```

## 🏆 Key Takeaways
- Magic methods allow your objects to behave like built-in types.
""",
        "questions": [
            {"text": "Which magic method implements the '+' operator?", "options": [
                {"text": "__add__", "correct": True}, {"text": "__plus__", "correct": False},
                {"text": "__sum__", "correct": False}, {"text": "__total__", "correct": False}]},
        ],
        "challenge": {
            "title": "String Adder",
            "description": "Define `Word`. Implement `__add__` to concatenate its string with another. Print `Word('A') + Word('B')` result string.",
            "initial_code": "class Word:\n    def __init__(self, s): self.s = s\n",
            "solution_code": "class Word:\n    def __init__(self, s): self.s = s\n    def __add__(self, other): return self.s + other.s\nprint(Word('A') + Word('B'))\n",
            "test_cases": [{"input": "", "expected": "AB"}],
        },
    },

    "les-oop-9-intermediate": {
        "title": "Representing Objects (__str__ vs __repr__)",
        "content": """# Representing Objects (__str__ vs __repr__)

## 🎯 Learning Objectives
- Customize how objects look when printed
- Differentiate between "End-user display" and "Developer debugging"
- Return strings from both methods

## 📚 Concept Overview
- `__str__`: For users. Should be readable. `print(obj)`
- `__repr__`: For developers. Should help recreate the object. `repr(obj)`

```python
class Car:
    def __repr__(self): return "Car('Tesla')"
    def __str__(self): return "A shiny red Tesla"
```

## 🏆 Key Takeaways
- Always implement `__repr__` for easier debugging.
""",
        "questions": [
            {"text": "Which method is used for a human-friendly representation of an object?", "options": [
                {"text": "__str__", "correct": True}, {"text": "__repr__", "correct": False},
                {"text": "__print__", "correct": False}, {"text": "__text__", "correct": False}]},
        ],
        "challenge": {
            "title": "Dunder Repr",
            "description": "Define `User`. Implement `__repr__` to return 'USER-ID'. Print an instance directly.",
            "initial_code": "# repr demo\n",
            "solution_code": "class User:\n    def __repr__(self): return 'USER-ID'\nprint(User())\n",
            "test_cases": [{"input": "", "expected": "USER-ID"}],
        },
    },

    "les-oop-9-pro": {
        "title": "Comparison & Hashing Magic",
        "content": """# Comparison & Hashing Magic

## 🎯 Learning Objectives
- Implement `__eq__`, `__lt__`, `__gt__` for logic checks (==, <, >)
- Make your objects "Hashable" so they can be dict keys
- Understand `__hash__` and the relationship with `__eq__`

## 📚 Concept Overview
```python
class Item:
    def __init__(self, name): self.name = name
    def __eq__(self, other):
        return self.name == other.name
```

## 🏆 Key Takeaways
- If you define `__eq__`, you should also define `__hash__` if you want the object to be used in sets or as dict keys.
""",
        "questions": [
            {"text": "Which magic method allows you to use '==' between two objects?", "options": [
                {"text": "__eq__", "correct": True}, {"text": "__equal__", "correct": False},
                {"text": "__comp__", "correct": False}, {"text": "__same__", "correct": False}]},
        ],
        "challenge": {
            "title": "Equal Logic",
            "description": "Implement `__eq__` for `Box` to compare their `size`. Print result of `Box(10) == Box(10)`.",
            "initial_code": "class Box:\n    def __init__(self, s): self.size = s\n",
            "solution_code": "class Box:\n    def __init__(self, s): self.size = s\n    def __eq__(self, other): return self.size == other.size\nprint(Box(10) == Box(10))\n",
            "test_cases": [{"input": "", "expected": "True"}],
        },
    },

    # ── Lesson 10: Mini Project ──────────────────────────────────────────────
    "les-oop-10-beginner": {
        "title": "Project: Library Management",
        "content": """# Project: Library Management

## 🎯 Goal
Create matching classes for `Book` and `Library`.

## 📝 Requirements
- `Book`: has title, author.
- `Library`: has a list of books.
- Method `add_book(book)` and `show_all()`.
""",
        "questions": [],
        "challenge": {
            "title": "Book Adder",
            "description": "Define `Library` with `self.books = []`. Method `add(self, b)`. Add 'Python' to a library and print count.",
            "initial_code": "# Library logic\n",
            "solution_code": "class Library:\n    def __init__(self): self.books = []\n    def add(self, b): self.books.append(b)\nl = Library()\nl.add('Python')\nprint(len(l.books))\n",
            "test_cases": [{"input": "", "expected": "1"}],
        },
    },

    "les-oop-10-intermediate": {
        "title": "Project: RPG Game Battle",
        "content": """# Project: RPG Game Battle

## 🎯 Goal
Build a battle system between a `Warrior` and a `Mage`.

## 📝 Features
- Base class `Character` with `hp` and `take_damage`.
- Child classes with unique `attack` styles.
- A `battle(c1, c2)` function that uses Polymorphism.
""",
        "questions": [],
        "challenge": {
            "title": "HP System",
            "description": "Character starts with 100 HP. Method `damage(amount)` reduces it. Create one, apply 30 damage, print HP.",
            "initial_code": "# damage loop\n",
            "solution_code": "class Char:\n    def __init__(self): self.hp = 100\n    def damage(self, a): self.hp -= a\nc = Char()\nc.damage(30)\nprint(c.hp)\n",
            "test_cases": [{"input": "", "expected": "70"}],
        },
    },

    "les-oop-10-pro": {
        "title": "Project: Banking API with Custom Logic",
        "content": """# Project: Banking API with Custom Logic

## 🎯 Goal
Build a safe banking system with encapsulation and auditing.

## 📝 Features
- `__balance` is strictly private.
- `@property` for balance access (read-only).
- `@balance.setter` to prevent fraudulent deposits.
- Exception handling for overdraws.
""",
        "questions": [],
        "challenge": {
            "title": "Bank Security",
            "description": "Implement private `__bal`. If someone tries to set it directly, it should fail. Use `@property` to return it. Print 500 deposit result.",
            "initial_code": "# secure bank\n",
            "solution_code": "class Bank:\n    def __init__(self): self.__bal = 0\n    @property\n    def balance(self): return self.__bal\n    def deposit(self, a): self.__bal += a\nb = Bank()\nb.deposit(500)\nprint(b.balance)\n",
            "test_cases": [{"input": "", "expected": "500"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 8 (OOP) — Lessons 6-10"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 8 (6-10)"))
