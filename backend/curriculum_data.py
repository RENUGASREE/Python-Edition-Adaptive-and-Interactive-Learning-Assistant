CURRICULUM_DATA = [
    {
        "module_id": 19, # Python Fundamentals
        "topics": [
            {
                "title": "Python Intro",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nPython is a popular programming language that is easy to read and write.\n\n🧠 Explanation\nThink of Python as a robot that follows your instructions. You use it to tell a computer what to do.\n\n🔤 Syntax\nprint('Hello World')\n\n📌 Example\nprint('Welcome to Python!')\n\n🌍 Use Case\nBuilding simple calculators or welcome messages.\n\n🔑 Key Takeaways\n- Python is beginner-friendly.\n- Uses simple English-like syntax.\n\n💻 Challenge\nWrite a program that prints your name.",
                    "challenge": {
                        "title": "My First Hello",
                        "description": "Write a Python script to print the message 'Python is Awesome!'",
                        "initial_code": "# Write your code here",
                        "solution_code": "print('Python is Awesome!')",
                        "test_cases": [{"input": "", "expected": "Python is Awesome!"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nPython is an interpreted, high-level, general-purpose programming language with dynamic typing and garbage collection.\n\n🧠 Explanation\nPython handles memory management for you. It's 'interpreted', meaning you don't need to compile it before running.\n\n🔤 Syntax\nimport sys\nprint(sys.version)\n\n📌 Example\nx = 10\ny = 20\nprint(f'Sum: {x+y}')\n\n🌍 Use Case\nScripting tasks once done manually, like renaming 100 files at once.\n\n💻 Challenge\nAssign two numbers to variables, add them, and print the result with a label.",
                    "challenge": {
                        "title": "Variable Addition",
                        "description": "Create two variables a=5 and b=10, then print 'The sum is 15'",
                        "initial_code": "a = 5\nb = 10\n# Calc sum and print",
                        "solution_code": "a = 5\nb = 10\nprint(f'The sum is {a+b}')",
                        "test_cases": [{"input": "", "expected": "The sum is 15"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nPython is a multi-paradigm language favoring readability (PEP 8) and utilizing 'batteries included' philosophy through its extensive standard library.\n\n🧠 Explanation\nPro Python involves understanding the internals: Bytecode, GIL (Global Interpreter Lock), and efficient memory usage via slots or generators.\n\n🔤 Advanced Syntax\n[x**2 for x in range(10) if x % 2 == 0]\n\n📌 Example\ndef optimized_sum(n):\n    return n * (n + 1) // 2\n\n🌍 Use Case\nBuilding scalable web backends or high-performance data processing pipelines.\n\n💻 Challenge\nWrite a one-liner to generate squares of even numbers from 1 to 20.",
                    "challenge": {
                        "title": "One-Liner Squares",
                        "description": "Use a list comprehension to calculate squares of even numbers from 1 to 20.",
                        "initial_code": "squares = []\nprint(squares)",
                        "solution_code": "squares = [x**2 for x in range(1, 21) if x % 2 == 0]\nprint(squares)",
                        "test_cases": [{"input": "", "expected": "[4, 16, 36, 64, 100, 144, 196, 256, 324, 400]"}]
                    }
                }
            },
            {
                "title": "Variables",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nVariables are like boxes that store data.\n\n🧠 Explanation\nYou give a box a name, and put a value inside it. Example: name = 'Renuga'\n\n🔤 Syntax\nvariable_name = value\n\n📌 Example\nage = 20\nprint(age)\n\n🌍 Use Case\nSaving a user's score in a game.\n\n🧪 Knowledge Check\n1. Can a variable name start with a number?\n\n💻 Challenge\nCreate a variable 'city' and store your city name in it.",
                    "challenge": {
                        "title": "City Variable",
                        "description": "Create a variable named 'city' with value 'New York' and print it.",
                        "initial_code": "# Code here",
                        "solution_code": "city = 'New York'\nprint(city)",
                        "test_cases": [{"input": "", "expected": "New York"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nVariables in Python are references to objects in memory. Python uses dynamic typing.\n\n🧠 Explanation\nYou don't need to specify 'int' or 'string'. Names point to objects. x = 5 makes 'x' point to an integer object 5.\n\n🔤 Syntax\nname: str = 'John' # Type Hinting\n\n📌 Example\nx, y, z = 1, 2, 3\nprint(x, y, z)\n\n🌍 Use Case\nSwapping two variable values without a temporary variable: a, b = b, a\n\n🧪 Knowledge Check\n1. What is dynamic typing?\n\n💻 Challenge\nSwap two variables x=10 and y=20 in one line and print them.",
                    "challenge": {
                        "title": "One-Line Swap",
                        "description": "Swap x=10 and y=20 using tuple unpacking. Print x and y.",
                        "initial_code": "x = 10\ny = 20\n# Swap here\nprint(x, y)",
                        "solution_code": "x = 10\ny = 20\nx, y = y, x\nprint(x, y)",
                        "test_cases": [{"input": "", "expected": "20 10"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nPython handles variables through namespaces and scopes (Local, Enclosing, Global, Built-in).\n\n🧠 Explanation\nPro developers use `__slots__` for memory optimization and understand the difference between mutable and immutable defaults in functions.\n\n🔤 Advanced Syntax\ndef func(items=[]): # Dangerous!\n    ...\n\n📌 Example\nimport gc\n# Check reference counts\n\n🌍 Use Case\nOptimizing memory in loops or handling deep/shallow copies of complex structures.\n\n🧪 Knowledge Check\n1. What is __slots__ used for?\n\n💻 Challenge\nDemonstrate how a global variable can be modified inside a function using the 'global' keyword.",
                    "challenge": {
                        "title": "Global Keyword",
                        "description": "Modify a global variable 'count' inside a function 'increment'.",
                        "initial_code": "count = 0\ndef increment():\n    # Modify count\n    pass\nincrement()\nprint(count)",
                        "solution_code": "count = 0\ndef increment():\n    global count\n    count += 1\nincrement()\nprint(count)",
                        "test_cases": [{"input": "", "expected": "1"}]
                    }
                }
            }
        ]
    },
    {
        "module_id": 21, # Data Structures
        "topics": [
            {
                "title": "Python Lists",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nA list is a collection of items stored together.\n\n🧠 Explanation\nLists use square brackets []. They store multiple values in order.\n\n🔤 Syntax\nmy_list = [1, 2, 3]\n\n📌 Example\nfruits = ['apple', 'banana']\nprint(fruits)\n\n🌍 Use Case\nShopping lists or playlists.\n\n🧪 Knowledge Check\n1. What brackets do lists use?\n\n💻 Challenge\nPrint the first item of list ['a', 'b', 'c']",
                    "challenge": {
                        "title": "First Element",
                        "description": "Print the first element of list L = [10, 20, 30]",
                        "initial_code": "L = [10, 20, 30]\n# Print",
                        "solution_code": "L = [10, 20, 30]\nprint(L[0])",
                        "test_cases": [{"input": "", "expected": "10"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nLists are mutable, ordered collections that support indexing and slicing.\n\n🧠 Explanation\nYou can add with `.append()`, delete with `.remove()`, and slice with `[start:end]`.\n\n🔤 Syntax\nL.append(new_item)\n\n📌 Example\nnums = [1, 2, 3, 4, 5]\nprint(nums[1:4]) # [2, 3, 4]\n\n🌍 Use Case\nManaging dynamic data like items in a digital inventory.\n\n🧪 Knowledge Check\n1. What does .pop() do?\n\n💻 Challenge\nAdd '40' to the list [10, 20, 30] and print the result.",
                    "challenge": {
                        "title": "List Append",
                        "description": "Append 40 to L = [10, 20, 30] and print L.",
                        "initial_code": "L = [10, 20, 30]\n# Append and print",
                        "solution_code": "L = [10, 20, 30]\nL.append(40)\nprint(L)",
                        "test_cases": [{"input": "", "expected": "[10, 20, 30, 40]"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nLists are dynamic arrays with amortized O(1) append time and support advanced manipulations like comprehensions and deep copies.\n\n🧠 Explanation\nInternally, Python over-allocates memory for lists. Comprehensions are often faster than basic map/filter.\n\n🔤 Advanced Syntax\neven_sq = [x*x for x in data if x % 2 == 0]\n\n📌 Example\nmulti_dim = [[1, 2], [3, 4]]\n\n🌍 Use Case\nNumerical processing pipelines and matrix manipulation.\n\n🧪 Knowledge Check\n1. Time complexity of list append?\n\n💻 Challenge\nFlat a nested list [[1,2], [3,4]] using a nested list comprehension.",
                    "challenge": {
                        "title": "Nested Flattening",
                        "description": "Flatten list L = [[1,2], [3,4]] to [1,2,3,4] using list comprehension.",
                        "initial_code": "L = [[1,2], [3,4]]\n# Flatten\nprint(flat)",
                        "solution_code": "L = [[1,2], [3,4]]\nflat = [item for sublist in L for item in sublist]\nprint(flat)",
                        "test_cases": [{"input": "", "expected": "[1, 2, 3, 4]"}]
                    }
                }
            }
        ]
    }
]
