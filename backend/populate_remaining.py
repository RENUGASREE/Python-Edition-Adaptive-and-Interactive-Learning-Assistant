import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

REMAINING_CURRICULUM = [
    {
        "module_id": 22, # Functions & Modules
        "topics": [
            {
                "title": "Function Basics",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nA function is a reusable block of code that performs a specific task.\n\n🧠 Explanation\nInstead of writing the same code 10 times, you put it in a function and 'call' it whenever you need it.\n\n🔤 Syntax\ndef function_name():\n    # code here\n\n📌 Example\ndef greet():\n    print('Hello Friend!')\ngreet()\n\n🌍 Use Case\nReusing a piece of code that calculates the area of a circle.\n\n🧪 Knowledge Check\n1. What keyword starts a function definition?\n\n💻 Challenge\ndef hello(): print('Hi'). Call it.",
                    "challenge": {
                        "title": "Simple Call",
                        "description": "Define function `say_hi` to print 'Hi' and call it.",
                        "initial_code": "def say_hi():\n    # code\n# call it",
                        "solution_code": "def say_hi():\n    print('Hi')\nsay_hi()",
                        "test_cases": [{"input": "", "expected": "Hi"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nFunctions can accept parameters and return values.\n\n🧠 Explanation\nYou pass information into a function as arguments. The function 'returns' a result back to you.\n\n🔤 Syntax\ndef add(a, b): return a + b\n\n📌 Example\ndef square(n): return n*n\nprint(square(4)) # 16\n\n🌍 Use Case\nA function that takes a list of prices and returns the total including tax.\n\n🧪 Knowledge Check\n1. What is a parameter?\n\n💻 Challenge\nWrite function `multiply(a, b)` that returns the product.",
                    "challenge": {
                        "title": "Multiply Function",
                        "description": "Create a function `multiply(a, b)` that returns a * b. Call it with 5, 2 and print.",
                        "initial_code": "def multiply(a, b):\n    pass\nprint(multiply(5, 2))",
                        "solution_code": "def multiply(a, b):\n    return a * b\nprint(multiply(5, 2))",
                        "test_cases": [{"input": "", "expected": "10"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nFunctions are first-class objects in Python supporting recursion, higher-order logic, and dynamic arguments (`*args`, `**kwargs`).\n\n🧠 Explanation\nYou can pass a function into another function. Recursion is when a function calls itself.\n\n🔤 Advanced Syntax\ndef multi(*args, **kwargs):\n    for a in args: print(a)\n\n📌 Example\ndef factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)\n\n🌍 Use Case\nWriting dynamic wrappers (decorators) or mathematical algorithms like quicksort.\n\n🧪 Knowledge Check\n1. Use of **kwargs?\n\n💻 Challenge\nWrite a recursive function to sum numbers from 1 to n.",
                    "challenge": {
                        "title": "Recursive Sum",
                        "description": "Write a recursive function `rec_sum(n)` that sums 1..n. Call with 5.",
                        "initial_code": "def rec_sum(n):\n    # base case\n    # recursive case\nprint(rec_sum(5))",
                        "solution_code": "def rec_sum(n):\n    if n == 1: return 1\n    return n + rec_sum(n-1)\nprint(rec_sum(5))",
                        "test_cases": [{"input": "", "expected": "15"}]
                    }
                }
            }
        ]
    },
    {
        "module_id": 23, # Advanced Python
        "topics": [
            {
                "title": "Exception Handling",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nException handling stops your program from crashing when an error occurs.\n\n🧠 Explanation\nUse `try` to run code that might fail, and `except` to handle the failure gracefully.\n\n🔤 Syntax\ntry:\n    # code\nexcept:\n    # stop crash\n\n📌 Example\ntry:\n    print(1 / 0)\nexcept:\n    print('Cannot divide by zero')\n\n🌍 Use Case\nPreventing a calculation error from closing the entire app.\n\n🧪 Knowledge Check\n1. When does 'except' run?\n\n💻 Challenge\ntry to divide 10 by a string 'a', print 'Error'.",
                    "challenge": {
                        "title": "Catch Error",
                        "description": "Try dividing 10 by 'a'. Print 'Error' if it fails.",
                        "initial_code": "try:\n    # calc\nexcept:\n    # print",
                        "solution_code": "try:\n    10 / 'a'\nexcept:\n    print('Error')",
                        "test_cases": [{"input": "", "expected": "Error"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nHandling specific exception types and using `finally` for cleanup tasks.\n\n🧠 Explanation\nYou can catch `ValueError`, `ZeroDivisionError` separately. `finally` runs NO MATTER WHAT.\n\n🔤 Syntax\nexcept ZeroDivisionError:\n    ...\nfinally:\n    ...\n\n📌 Example\ntry:\n    n = int('abc')\nexcept ValueError:\n    print('Not a number!')\n\n🌍 Use Case\nClosing a database connection in `finally` even if a query failed.\n\n🧪 Knowledge Check\n1. Purpose of 'finally'?\n\n💻 Challenge\nTry int('hi'), catch ValueError, print 'Invalid'.",
                    "challenge": {
                        "title": "Value Error",
                        "description": "Attempt to convert 'hi' to int. Catch ValueError and print 'Invalid'.",
                        "initial_code": "try:\n    # code\nexcept ValueError:\n    # print",
                        "solution_code": "try:\n    int('hi')\nexcept ValueError:\n    print('Invalid')",
                        "test_cases": [{"input": "", "expected": "Invalid"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nCustom decorators and context managers allow for reusable error handling patterns.\n\n🧠 Explanation\nYou can create your own exception classes (`class MyError(Exception)`) to define domain-specific issues.\n\n🔤 Advanced Syntax\nclass MyError(Exception): pass\n\n📌 Example\ndef log_errors(func):\n    def wrapper(*args):\n        try: return func(*args)\n        except Exception as e: print(e)\n    return wrapper\n\n🌍 Use Case\nBuilding an API where every error is logged and formatted before being sent to the client.\n\n🧪 Knowledge Check\n1. How to create a custom Exception?\n\n💻 Challenge\nDefine `UserError(Exception)` and 'raise' it.",
                    "challenge": {
                        "title": "Raise Custom",
                        "description": "Define `class MyErr(Exception): pass`. Raise it and print 'Caught' in except.",
                        "initial_code": "class MyErr(Exception): pass\ntry:\n    # raise\nexcept MyErr:\n    print('Caught')",
                        "solution_code": "class MyErr(Exception): pass\ntry:\n    raise MyErr\nexcept MyErr:\n    print('Caught')",
                        "test_cases": [{"input": "", "expected": "Caught"}]
                    }
                }
            }
        ]
    },
    {
        "module_id": 24, # OOP
        "topics": [
            {
                "title": "Classes and Objects",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nA class is a blueprint, and an object is a real thing built from that blueprint.\n\n🧠 Explanation\nA 'Car' class is the drawing. My blue Toyota is the 'Object'.\n\n🔤 Syntax\nclass Car:\n    pass\nmy_car = Car()\n\n📌 Example\nclass Dog:\n    species = 'Animal'\nlassie = Dog()\nprint(lassie.species)\n\n🌍 Use Case\nCreating many characters in a game with shared traits like 'health' and 'power'.\n\n🧪 Knowledge Check\n1. What is a class?\n\n💻 Challenge\nDefine class `Person` and create object `p1`. Print its type.",
                    "challenge": {
                        "title": "Person Class",
                        "description": "Create class Person. Instantiate p1. Print 'Object Created'.",
                        "initial_code": "class Person:\n    pass\n# Create p1\n# Print",
                        "solution_code": "class Person:\n    pass\np1 = Person()\nprint('Object Created')",
                        "test_cases": [{"input": "", "expected": "Object Created"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nThe `__init__` method (constructor) initializes an object's state.\n\n🧠 Explanation\nUse `self` to assign values to the specific object being created.\n\n🔤 Syntax\ndef __init__(self, name): self.name = name\n\n📌 Example\nclass Cat:\n    def __init__(self, name):\n        self.name = name\nmy_cat = Cat('Whiskers')\n\n🌍 Use Case\nInitializing a user account with a specific username and email.\n\n🧪 Knowledge Check\n1. What is 'self'?\n\n💻 Challenge\nCreate `Robot` class with `name` attribute. Instantiate with 'R2D2'.",
                    "challenge": {
                        "title": "Robot Init",
                        "description": "Class Robot with __init__ taking name. Create 'R2D2' and print name.",
                        "initial_code": "class Robot:\n    def __init__(self, name):\n        # assign\n# inst and print",
                        "solution_code": "class Robot:\n    def __init__(self, name):\n        self.name = name\nr = Robot('R2D2')\nprint(r.name)",
                        "test_cases": [{"input": "", "expected": "R2D2"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nInheritance allows a class to derive features from another class.\n\n🧠 Explanation\nSub-classes override methods for specific behaviors. Inheritance promotes DRY (Don't Repeat Yourself).\n\n🔤 Advanced Syntax\nclass Child(Parent):\n    def override(self): super().override()\n\n📌 Example\nclass Animal:\n    def speak(self): print('Animal sound')\nclass Dog(Animal):\n    def speak(self): print('Bark')\n\n🌍 Use Case\nCreating specialized GUI components from a base 'Widget' class.\n\n🧪 Knowledge Check\n1. What is super() used for?\n\n💻 Challenge\nInherit `Dog` from `Animal`. Call `super().speak()` inside Dog's `speak`.",
                    "challenge": {
                        "title": "Super Call",
                        "description": "Animal.speak prints 'A'. Dog inherits Animal, speak prints 'D' then calls super().speak().",
                        "initial_code": "class Animal:\n    def speak(self): print('A')\nclass Dog(Animal):\n    # speak logic\nDog().speak()",
                        "solution_code": "class Animal:\n    def speak(self): print('A')\nclass Dog(Animal):\n    def speak(self):\n        super().speak()\n        print('D')\nDog().speak()",
                        "test_cases": [{"input": "", "expected": "A\nD"}]
                    }
                }
            }
        ]
    }
]

def populate_remaining():
    print("🚀 Starting REMAINING Curriculum Population...")
    total_lessons = 0
    total_challenges = 0
    for module_entry in REMAINING_CURRICULUM:
        module_id = module_entry["module_id"]
        topics = module_entry["topics"]
        for topic_entry in topics:
            title = topic_entry["title"]
            print(f"📦 Processing Topic: {title}")
            for level in ["beginner", "intermediate", "pro"]:
                diff_label = level.capitalize()
                content = topic_entry[level]["content"]
                challenge_data = topic_entry[level]["challenge"]
                Lesson.objects.filter(module_id=module_id, title=title, difficulty=diff_label).delete()
                lesson = Lesson.objects.create(
                    module_id=module_id,
                    title=title,
                    difficulty=diff_label,
                    content=content,
                    slug=title.lower().replace(" ", "-"),
                    order=100 + topics.index(topic_entry), # Offset
                    duration=15
                )
                total_lessons += 1
                Challenge.objects.filter(lesson_id=lesson.id).delete()
                Challenge.objects.filter(title=challenge_data["title"], difficulty=diff_label).delete()
                Challenge.objects.create(
                    lesson_id=lesson.id,
                    title=challenge_data["title"],
                    description=challenge_data["description"],
                    initial_code=challenge_data["initial_code"],
                    solution_code=challenge_data["solution_code"],
                    test_cases=challenge_data["test_cases"],
                    points=50 if diff_label == "Beginner" else (100 if diff_label == "Intermediate" else 200),
                    difficulty=diff_label
                )
                total_challenges += 1
    print(f"✅ Success! Created {total_lessons} Lessons and {total_challenges} Challenges.")

if __name__ == "__main__":
    populate_remaining()
