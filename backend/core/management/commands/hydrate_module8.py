"""python manage.py hydrate_module8 -- Module 8 OOP Lessons 1-5"""
from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Lesson, Quiz, Question, Challenge

LESSONS = {
    # ── Lesson 1: Classes & Objects ──────────────────────────────────────────
    "les-oop-1-beginner": {
        "title": "What is a Class?",
        "content": """# What is a Class?

## 🎯 Learning Objectives
- Concept of Object-Oriented Programming (OOP)
- Difference between a Class and an Object
- Defining your first class with the `class` keyword

## 📚 Concept Overview
OOP is a way to organize code by grouping related data and functions together.
- **Class**: A blueprint or template (e.g., "Car").
- **Object**: A specific instance made from the blueprint (e.g., "The red Tesla parked outside").

```python
class Dog:
    pass

my_dog = Dog()
print(type(my_dog)) # <class '__main__.Dog'>
```

## 🏆 Key Takeaways
- Classes are like cookie cutters; objects are the cookies.
- Use CamelCase for class names (e.g., `MySimpleClass`).
""",
        "questions": [
            {"text": "What is a 'Class' in Python?", "options": [
                {"text": "A blueprint for creating objects", "correct": True},
                {"text": "A specialized type of list", "correct": False},
                {"text": "A built-in function", "correct": False},
                {"text": "A way to import modules", "correct": False}]},
            {"text": "Which naming convention is recommended for Python classes?", "options": [
                {"text": "CamelCase (e.g. MyClass)", "correct": True},
                {"text": "snake_case (e.g. my_class)", "correct": False},
                {"text": "UPPERCASE", "correct": False},
                {"text": "kebab-case", "correct": False}]},
        ],
        "challenge": {
            "title": "First Class",
            "description": "Define an empty class named `Vehicle`. Create an instance of it named `car`. Print the type of `car`.",
            "initial_code": "# Define class and object\n",
            "solution_code": "class Vehicle: pass\ncar = Vehicle()\nprint(type(car))\n",
            "test_cases": [{"input": "", "expected": "<class '__main__.Vehicle'>"}],
        },
    },

    "les-oop-1-intermediate": {
        "title": "The 'self' Parameter",
        "content": """# The 'self' Parameter

## 🎯 Learning Objectives
- Understand why every instance method needs `self`
- Learn that `self` represents the specific object being worked on
- Call methods from within other methods

## 📚 Concept Overview
In Python, `self` is how an object refers to its own data and behavior.

```python
class Dog:
    def bark(self):
        print("Woof!")
```

When you call `my_dog.bark()`, Python actually does `Dog.bark(my_dog)`. The `self` parameter receives the instance automatically.

## 🏆 Key Takeaways
- `self` must be the first parameter of any instance method.
- You use `self.attribute` to access data belonging to that specific object.
""",
        "questions": [
            {"text": "What does the `self` parameter represent in a class method?", "options": [
                {"text": "The specific instance of the class", "correct": True},
                {"text": "The class blueprint itself", "correct": False},
                {"text": "A global variable", "correct": False},
                {"text": "The result of the function", "correct": False}]},
            {"text": "Where does the `self` parameter usually go in a method definition?", "options": [
                {"text": "As the first parameter", "correct": True},
                {"text": "As the last parameter", "correct": False},
                {"text": "It is optional", "correct": False},
                {"text": "In the return statement", "correct": False}]},
        ],
        "challenge": {
            "title": "Self Talker",
            "description": "Define a class `Robot` with a method `greet(self)`. It should print 'Hello Human'. Create a robot and call the method.",
            "initial_code": "# Define and call\n",
            "solution_code": "class Robot:\n    def greet(self):\n        print('Hello Human')\nr = Robot()\nr.greet()\n",
            "test_cases": [{"input": "", "expected": "Hello Human"}],
        },
    },

    "les-oop-1-pro": {
        "title": "Internal Bytecode of Method Calls",
        "content": """# Internal Bytecode of Method Calls

## 🎯 Learning Objectives
- Differentiate between Bound and Unbound methods
- Understand how Python resolves method lookups
- Use `getattr()` to call methods dynamically

## 📚 Concept Overview
A method is just a function attached to a class. When accessed through an instance, it becomes a **Bound Method** (pre-filled with `self`).

```python
class A:
    def hi(self): print("Hi")

a = A()
# These are equivalent:
a.hi() 
A.hi(a)
```

## ️🏆 Key Takeaways
- Method calls are syntactic sugar for passing the instance as the first argument to a class function.
""",
        "questions": [
            {"text": "A method that is 'tied' to a specific object instance is called a:", "options": [
                {"text": "Bound method", "correct": True}, {"text": "Static method", "correct": False},
                {"text": "Global method", "correct": False}, {"text": "Linked method", "correct": False}]},
        ],
        "challenge": {
            "title": "Unbound Call",
            "description": "Define class `C` with `hello(self)`. Create instance `obj`. Call the method UNBOUND (using the class name and passing the object).",
            "initial_code": "class C:\n    def hello(self): print('OK')\nobj = C()\n# Call it using C.hello(...)\n",
            "solution_code": "class C:\n    def hello(self): print('OK')\nobj = C()\nC.hello(obj)\n",
            "test_cases": [{"input": "", "expected": "OK"}],
        },
    },

    # ── Lesson 2: Constructors (__init__) ────────────────────────────────────
    "les-oop-2-beginner": {
        "title": "The __init__ Method",
        "content": """# The __init__ Method

## 🎯 Learning Objectives
- Use the class constructor to set initial values
- Understand "Dunder" (Double Underscore) methods
- Initialize object state during creation

## 📚 Concept Overview
The `__init__` method runs automatically when you create a new object. It's the perfect place to set initial properties.

```python
class User:
    def __init__(self, username):
        self.username = username # Save to instance

u = User("Alice")
print(u.username) # Alice
```

## 🏆 Key Takeaways
- `__init__` is NOT technically a "constructor" in the low-level sense, but it functions as one.
- Use it to enforce required data during object creation.
""",
        "questions": [
            {"text": "Which method is called automatically when an object is instantiated?", "options": [
                {"text": "__init__", "correct": True}, {"text": "__start__", "correct": False},
                {"text": "__new__", "correct": False}, {"text": "__create__", "correct": False}]},
            {"text": "What does a 'Dunder' method refer to?", "options": [
                {"text": "A method with double underscores on both sides", "correct": True},
                {"text": "A private method", "correct": False},
                {"text": "A method that returns None", "correct": False},
                {"text": "A static method", "correct": False}]},
        ],
        "challenge": {
            "title": "User Creator",
            "description": "Define a class `Person` with `__init__` that takes `name` and `age`. Store them as `self.name` and `self.age`. Print them for a 'Bob', 25.",
            "initial_code": "# Use __init__\n",
            "solution_code": "class Person:\n    def __init__(self, name, age):\n        self.name = name\n        self.age = age\np = Person('Bob', 25)\nprint(p.name, p.age)\n",
            "test_cases": [{"input": "", "expected": "Bob 25"}],
        },
    },

    "les-oop-2-intermediate": {
        "title": "Default Arguments in __init__",
        "content": """# Default Arguments in __init__

## 🎯 Learning Objectives
- Create optional attributes
- Use default values for common states
- Handle complex initialization logic

## 📚 Concept Overview
```python
class Player:
    def __init__(self, name, score=0):
        self.name = name
        self.score = score

p1 = Player("Knight") # score defaults to 0
p2 = Player("Boss", 100) # custom score
```

## 🏆 Key Takeaways
- Default arguments make your classes more flexible and easier to use.
""",
        "questions": [
            {"text": "How do you make an attribute optional in a class constructor?", "options": [
                {"text": "Provide a default value in the __init__ parameters", "correct": True},
                {"text": "Make it a private variable", "correct": False},
                {"text": "Use the 'optional' decorator", "correct": False},
                {"text": "Define it outside the class", "correct": False}]},
        ],
        "challenge": {
            "title": "Point Creator",
            "description": "Define `Point` with `x` and `y` defaults to 0. Create `p = Point(5)`. Print `p.x` and `p.y`.",
            "initial_code": "# Default x, y\n",
            "solution_code": "class Point:\n    def __init__(self, x=0, y=0):\n        self.x = x\n        self.y = y\np = Point(5)\nprint(p.x, p.y)\n",
            "test_cases": [{"input": "", "expected": "5 0"}],
        },
    },

    "les-oop-2-pro": {
        "title": "The Lifecycle of an Object (__new__ vs __init__)",
        "content": """# The Lifecycle of an Object (__new__ vs __init__)

## 🎯 Learning Objectives
- Understand that `__new__` actually creates the object
- Differentiate between allocation and initialization
- Discussion on Singletons and Immutable types

## 📚 Concept Overview
- `__new__` is the first step (allocation). It returns the instance.
- `__init__` is the second step (customization).

You rarely need to override `__new__`, except when inheriting from immutable types like `int` or `tuple`, or when implementing a **Singleton Pattern** (ensuring only one instance of a class exists).

## 🏆 Key Takeaways
- `__new__` is a class method; `__init__` is an instance method.
""",
        "questions": [
            {"text": "Which method is responsible for returning a new instance of the class?", "options": [
                {"text": "__new__", "correct": True}, {"text": "__init__", "correct": False},
                {"text": "__start__", "correct": False}, {"text": "__alloc__", "correct": False}]},
        ],
        "challenge": {
            "title": "Lifecycle Fact",
            "description": "Print 'Init' if __init__ is for setting values, 'New' if for creating the memory space.",
            "initial_code": "# choice\n",
            "solution_code": "print('Init')\n",
            "test_cases": [{"input": "", "expected": "Init"}],
        },
    },

    # ── Lesson 3: Attributes & Methods ───────────────────────────────────────
    "les-oop-3-beginner": {
        "title": "Instance Methods",
        "content": """# Instance Methods

## 🎯 Learning Objectives
- Create functions that act on an object's data
- Understand the logic flow: Data + Behavior
- Return values from methods

## 📚 Concept Overview
Methods are functions that belong to an object.

```python
class Rectangle:
    def __init__(self, w, h):
        self.w = w
        self.h = h
    
    def area(self):
        return self.w * self.h

rect = Rectangle(10, 5)
print(rect.area()) # 50
```

## 🏆 Key Takeaways
- Methods allow you to interact with the object's internal state safely.
""",
        "questions": [
            {"text": "How do you call a method named 'run' on an object called 'player'?", "options": [
                {"text": "player.run()", "correct": True}, {"text": "player->run()", "correct": False},
                {"text": "run(player)", "correct": False}, {"text": "call run on player", "correct": False}]},
        ],
        "challenge": {
            "title": "Circle Area",
            "description": "Define `Circle` with `radius`. Add method `get_area(self)` that returns `3.14 * radius * radius`. Print area for radius 10.",
            "initial_code": "# Define method\n",
            "solution_code": "class Circle:\n    def __init__(self, r): self.radius = r\n    def get_area(self): return 3.14 * self.radius ** 2\nc = Circle(10)\nprint(c.get_area())\n",
            "test_cases": [{"input": "", "expected": "314.0"}],
        },
    },

    "les-oop-3-intermediate": {
        "title": "Class Methods & Static Methods",
        "content": """# Class Methods & Static Methods

## 🎯 Learning Objectives
- Use `@classmethod` for logic related to the whole class
- Use `@staticmethod` for utility functions inside a class namespace
- Distinguish when to NOT use `self`

## 📚 Concept Overview
### Class Methods (`cls`)
Takes the class as the first argument. Useful for specialized "factory" creators.
```python
class User:
    @classmethod
    def from_string(cls, data):
        # Create user from "Alice-Admin"
        name, role = data.split("-")
        return cls(name, role)
```

### Static Methods
Regular functions that happen to live inside a class. They don't take `self` or `cls`.
```python
@staticmethod
def check_password(p): return len(p) > 8
```

## ️🏆 Key Takeaways
- `@classmethod` is for class-state logic.
- `@staticmethod` is for pure functions grouped logically within the class.
""",
        "questions": [
            {"text": "What is the convention for the first parameter of a @classmethod?", "options": [
                {"text": "cls", "correct": True}, {"text": "self", "correct": False},
                {"text": "class", "correct": False}, {"text": "obj", "correct": False}]},
            {"text": "Does a @staticmethod require 'self'?", "options": [
                {"text": "No", "correct": True}, {"text": "Yes", "correct": False},
                {"text": "Only if returning a value", "correct": False}, {"text": "Only for private methods", "correct": False}]},
        ],
        "challenge": {
            "title": "Utility Static",
            "description": "Define class `MathTools`. Add a `@staticmethod` named `add(a, b)` that returns their sum. Call it without creating an instance.",
            "initial_code": "class MathTools:\n    # add @staticmethod\n",
            "solution_code": "class MathTools:\n    @staticmethod\n    def add(a, b): return a + b\nprint(MathTools.add(10, 20))\n",
            "test_cases": [{"input": "", "expected": "30"}],
        },
    },

    "les-oop-3-pro": {
        "title": "Method Dispatch & __dict__",
        "content": """# Method Dispatch & __dict__

## 🎯 Learning Objectives
- Understand that attributes are stored in a dictionary
- Modify attributes dynamically
- Explore the `vars()` function

## 📚 Concept Overview
Almost every object in Python has a `__dict__` where its attributes are kept.

```python
class MyClass:
    def __init__(self, x): self.x = x

m = MyClass(10)
print(m.__dict__) # {'x': 10}

# You can even add attributes on the fly!
m.y = 20
```

## 🏆 Key Takeaways
- Python objects are extremely dynamic. This "flexibility" is why it's so powerful.
""",
        "questions": [
            {"text": "What is the name of the internal dictionary where Python stores instance attributes?", "options": [
                {"text": "__dict__", "correct": True}, {"text": "__data__", "correct": False},
                {"text": "__vars__", "correct": False}, {"text": "__map__", "correct": False}]},
        ],
        "challenge": {
            "title": "Dict Inspect",
            "description": "Create an object of an empty class. Add an attribute `m.color = 'red'`. Print `m.__dict__`.",
            "initial_code": "# Dynamic attribute\n",
            "solution_code": "class E: pass\nm = E()\nm.color = 'red'\nprint(m.__dict__)\n",
            "test_cases": [{"input": "", "expected": "{'color': 'red'}"}],
        },
    },

    # ── Lesson 4: Class vs Instance Variables ────────────────────────────────
    "les-oop-4-beginner": {
        "title": "Instance Variables",
        "content": """# Instance Variables

## 🎯 Learning Objectives
- Define data unique to each object
- Understand the `self.name` syntax
- Avoid accidental data sharing

## 📚 Concept Overview
Data defined in `__init__` belongs to that instance.

```python
class Cat:
    def __init__(self, name):
        self.name = name

c1 = Cat("Misty")
c2 = Cat("Tom")
# c1.name is different from c2.name
```

## 🏆 Key Takeaways
- Instance variables are used for state that differs between objects.
""",
        "questions": [
            {"text": "Where are instance variables typically defined?", "options": [
                {"text": "Inside the __init__ method using self", "correct": True},
                {"text": "At the top of the class, outside methods", "correct": False},
                {"text": "In a separate module", "correct": False},
                {"text": "In the main loop", "correct": False}]},
        ],
        "challenge": {
            "title": "Unique IDs",
            "description": "Create two `Student` objects with different `id` instance variables. Print both IDs.",
            "initial_code": "# Define and print\n",
            "solution_code": "class Student:\n    def __init__(self, i): self.id = i\ns1 = Student(1)\ns2 = Student(2)\nprint(s1.id, s2.id)\n",
            "test_cases": [{"input": "", "expected": "1 2"}],
        },
    },

    "les-oop-4-intermediate": {
        "title": "Class Variables",
        "content": """# Class Variables

## 🎯 Learning Objectives
- Define data shared by ALL instances
- Use class variables for constants or counters
- Update class state across all objects

## 📚 Concept Overview
Class variables are defined at the top of the class.

```python
class Robot:
    population = 0 # Shared by all robots
    
    def __init__(self):
        Robot.population += 1

r1 = Robot()
r2 = Robot()
print(Robot.population) # 2
```

## ️🏆 Key Takeaways
- Class variables are great for tracking "Global" state for that class type.
""",
        "questions": [
            {"text": "What happens if you update a class variable?", "options": [
                {"text": "The change is visible to all instances of the class", "correct": True},
                {"text": "Only the current instance sees the change", "correct": False},
                {"text": "The program crashes", "correct": False},
                {"text": "It creates a new instance variable", "correct": False}]},
        ],
        "challenge": {
            "title": "Pop Counter",
            "description": "Create a class `Counter` with a class variable `count = 0`. Each time a new instance is made, increment `Counter.count`. Print it after 3 creations.",
            "initial_code": "class Counter:\n    count = 0\n",
            "solution_code": "class Counter:\n    count = 0\n    def __init__(self): Counter.count += 1\nCounter()\nCounter()\nCounter()\nprint(Counter.count)\n",
            "test_cases": [{"input": "", "expected": "3"}],
        },
    },

    "les-oop-4-pro": {
        "title": "Attribute Masking",
        "content": """# Attribute Masking

## 🎯 Learning Objectives
- Understand what happens when instance and class variables share a name
- Explore the lookup order (Instance -> Class -> Parent)
- Avoid confusing bugs in state management

## 📚 Concept Overview
If you have `self.x` and a class variable `x`, Python will always pick the instance one first.

```python
class A:
    x = 10
    def __init__(self):
        self.x = 20

obj = A()
print(obj.x) # 20 (Instance hides Class)
```

## 🏆 Key Takeaways
- Be careful with naming to avoid "masking" class-level configurations with local data.
""",
        "questions": [
            {"text": "If an instance and its class both have an attribute named 'v', which one does `obj.v` access?", "options": [
                {"text": "The instance attribute", "correct": True},
                {"text": "The class attribute", "correct": False},
                {"text": "It raises an error", "correct": False},
                {"text": "It returns a list of both", "correct": False}]},
        ],
        "challenge": {
            "title": "Mask Check",
            "description": "Print '20' if an instance variable overrides a class variable of the same name.",
            "initial_code": "# knowledge test\n",
            "solution_code": "print('20')\n",
            "test_cases": [{"input": "", "expected": "20"}],
        },
    },

    # ── Lesson 5: Property Decorators ────────────────────────────────────────
    "les-oop-5-beginner": {
        "title": "The @property Decorator",
        "content": """# The @property Decorator

## 🎯 Learning Objectives
- Use getters and setters the "Pythonic" way
- Treat methods like attributes (no parentheses needed)
- Add basic validation to attribute access

## 📚 Concept Overview
Java uses `get_age()` and `set_age()`. Python uses `@property`.

```python
class User:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name.upper()

u = User("alice")
print(u.name) # ALICE (no parentheses!)
```

## 🏆 Key Takeaways
- Use `@property` for logic that feels like "getting data".
""",
        "questions": [
            {"text": "What is the primary benefit of the @property decorator?", "options": [
                {"text": "Allowing a method to be accessed like an attribute (without parentheses)", "correct": True},
                {"text": "Making a method run faster", "correct": False},
                {"text": "Hiding a method from the user", "correct": False},
                {"text": "Calculating math automatically", "correct": False}]},
        ],
        "challenge": {
            "title": "Uppercase Name",
            "description": "Define `Product` with `_price`. Use `@property` named `price` that returns the value. Access it for a product and print it.",
            "initial_code": "class Product:\n    def __init__(self, p): self._price = p\n",
            "solution_code": "class Product:\n    def __init__(self, p): self._price = p\n    @property\n    def price(self): return self._price\nprint(Product(100).price)\n",
            "test_cases": [{"input": "", "expected": "100"}],
        },
    },

    "les-oop-5-intermediate": {
        "title": "Setters & Deleters",
        "content": """# Setters & Deleters

## 🎯 Learning Objectives
- Control how attributes are updated
- Validate data before saving (e.g. no negative ages)
- Remove attributes safely

## 📚 Concept Overview
```python
class Age:
    def __init__(self, a): self._a = a
    
    @property
    def age(self): return self._a
    
    @age.setter
    def age(self, value):
        if value < 0: raise ValueError("Age error")
        self._a = value
```

## 🏆 Key Takeaways
- `.setter` allows you to add security and validation to private data.
""",
        "questions": [
            {"text": "Which decorator is used to define a setter for a property named 'score'?", "options": [
                {"text": "@score.setter", "correct": True}, {"text": "@setter.score", "correct": False},
                {"text": "@set_score", "correct": False}, {"text": "@property.set", "correct": False}]},
        ],
        "challenge": {
            "title": "Secure Setter",
            "description": "Define `Temperature`. Add an `@val.setter` that prevents setting values below -273. Raise `ValueError` if lower.",
            "initial_code": "class Temperature:\n    def __init__(self, v): self._v = v\n",
            "solution_code": "class Temperature:\n    def __init__(self, v): self._v = v\n    @property\n    def v(self): return self._v\n    @v.setter\n    def v(self, value):\n        if value < -273: raise ValueError()\n        self._v = value\nt = Temperature(0)\nt.v = -300 # should fail\n",
            "test_cases": [{"input": "", "expected": "*ValueError*"}],
        },
    },

    "les-oop-5-pro": {
        "title": "Cached Properties & Descriptors",
        "content": """# Cached Properties & Descriptors

## 🎯 Learning Objectives
- Optimize expensive property calculations with `functools.cached_property`
- Understand the Descriptor Protocol (`__get__`, `__set__`)
- Build reusable custom attribute logic

## 📚 Concept Overview
If a property requires a heavy database call, you don't want to re-run it every time. `cached_property` computes it once and then saves it.

The Descriptor Protocol is the engine underneath `@property`. It allows classes to define the behavior of attribute access globally.

## 🏆 Key Takeaways
- Behind every `@property` is a Descriptor object.
- Use `cached_property` for performance optimization in data classes.
""",
        "questions": [
            {"text": "Which module provides the `cached_property` decorator?", "options": [
                {"text": "functools", "correct": True}, {"text": "sys", "correct": False},
                {"text": "math", "correct": False}, {"text": "contextlib", "correct": False}]},
        ],
        "challenge": {
            "title": "Property Engine",
            "description": "Name the protocol that allows objects to manage attribute access on other objects.",
            "initial_code": "# answer: Iterator or Descriptor or Generator\n",
            "solution_code": "print('Descriptor')\n",
            "test_cases": [{"input": "", "expected": "Descriptor"}],
        },
    },
}

class Command(BaseCommand):
    help = "Hydrate Module 8 (OOP) — Lessons 1-5"

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
        self.stdout.write(self.style.SUCCESS(f"\n🎉 Hydrated {count} lessons in Module 8 (1-5)"))
