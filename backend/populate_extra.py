import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge
from curriculum_data import CURRICULUM_DATA

# Additional curriculum data (batch 2)
EXTRA_CURRICULUM_DATA = [
    {
        "module_id": 20, # Control Flow
        "topics": [
            {
                "title": "If-Else Statements",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nAn if-else statement allows Python to make decisions.\n\n🧠 Explanation\nIf the condition is True, the 'if' block runs. Otherwise, the 'else' block runs.\n\n🔤 Syntax\nif condition:\n    # do something\nelse:\n    # do something else\n\n📌 Example\nage = 18\nif age >= 18:\n    print('You are an adult')\nelse:\n    print('You are a child')\n\n🌍 Use Case\nChecking if a user is logged in before showing a page.\n\n🧪 Knowledge Check\n1. What keyword is used for the condition?\n\n💻 Challenge\nWrite an if-else statement to check if a number is positive or negative.",
                    "challenge": {
                        "title": "Positive or Negative",
                        "description": "Check if number n=5 is positive or negative. Print 'Positive' if > 0.",
                        "initial_code": "n = 5\n# If-Else here",
                        "solution_code": "n = 5\nif n > 0:\n    print('Positive')\nelse:\n    print('Negative')",
                        "test_cases": [{"input": "", "expected": "Positive"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\nCompound conditionals allow multiple tests using 'elif' and nested if statements.\n\n🧠 Explanation\n'elif' stands for 'else if'. You can have many elifs but only one else.\n\n🔤 Syntax\nif condition:\n    ...\nelif condition2:\n    ...\n\n📌 Example\nscore = 85\nif score >= 90:\n    print('A')\nelif score >= 80:\n    print('B')\n\n🌍 Use Case\nCalculating grades or tax brackets based on income ranges.\n\n🧪 Knowledge Check\n1. Can you have multiple elifs?\n\n💻 Challenge\nTake a number and print 'Zero', 'Positive', or 'Negative' using elif.",
                    "challenge": {
                        "title": "Zero Check",
                        "description": "Check n=0. Print 'Zero' if 0, 'Positive' if >0, else 'Negative'.",
                        "initial_code": "n = 0\n# Elif logic here",
                        "solution_code": "n = 0\nif n == 0:\n    print('Zero')\nelif n > 0:\n    print('Positive')\nelse:\n    print('Negative')",
                        "test_cases": [{"input": "", "expected": "Zero"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nConditional expressions (ternary operators) and pattern matching (Python 3.10+) allow for concise decision logic.\n\n🧠 Explanation\nA ternary operator is a one-line if-else. Match-case is like a structural switch statement.\n\n🔤 Advanced Syntax\nx = 'Adult' if age >= 18 else 'Child'\n\n📌 Example\nstatus = 'High' if x > 100 else 'Low'\n\n🌍 Use Case\nSetting configuration defaults or mapping categories in data processing.\n\n🧪 Knowledge Check\n1. What is the ternary operator syntax?\n\n💻 Challenge\nUsing a ternary operator, assign 'Even' or 'Odd' to a variable and print it.",
                    "challenge": {
                        "title": "Ternary Check",
                        "description": "Use a ternary operator to print 'Even' for n=10.",
                        "initial_code": "n = 10\n# One-liner",
                        "solution_code": "n = 10\nres = 'Even' if n % 2 == 0 else 'Odd'\nprint(res)",
                        "test_cases": [{"input": "", "expected": "Even"}]
                    }
                }
            },
            {
                "title": "Loops",
                "beginner": {
                    "content": "🟢 BEGINNER LEVEL\n\n📘 Definition\nLoops are used to repeat a block of code multiple times.\n\n🧠 Explanation\nA 'for' loop is like a list of chores. You do each chore one by one until the list is empty.\n\n🔤 Syntax\nfor i in range(5):\n    # do something\n\n📌 Example\nfor i in range(3):\n    print('Hello!')\n\n🌍 Use Case\nPrinting numbers 1 to 10 without typing 10 print statements.\n\n🧪 Knowledge Check\n1. What does range(5) do?\n\n💻 Challenge\nWrite a for loop that prints the numbers 1 to 5.",
                    "challenge": {
                        "title": "Count to 5",
                        "description": "Print numbers 1 to 5 using a for loop.",
                        "initial_code": "# Loop here",
                        "solution_code": "for i in range(1, 6):\n    print(i)",
                        "test_cases": [{"input": "", "expected": "1\n2\n3\n4\n5"}]
                    }
                },
                "intermediate": {
                    "content": "🟡 INTERMEDIATE LEVEL\n\n📘 Definition\n'while' loops and control statements like break/continue allow for more complex repetition.\n\n🧠 Explanation\nA 'while' loop runs as long as a condition is True. Use `break` to stop early, and `continue` to skip a step.\n\n🔤 Syntax\nwhile condition:\n    ...\n\n📌 Example\ni = 1\nwhile i < 5:\n    print(i)\n    i += 1\n\n🌍 Use Case\nWaiting for user input or processing data until an end-of-file is reached.\n\n🧪 Knowledge Check\n1. What does 'break' do?\n\n💻 Challenge\nUse a while loop to print numbers 1 to 3, but use break to exit if i == 3.",
                    "challenge": {
                        "title": "Break Early",
                        "description": "Print numbers 1, 2 using a while loop and break when i reaches 3. Print 'Done' after breaking.",
                        "initial_code": "i = 1\n# while loop",
                        "solution_code": "i = 1\nwhile i < 5:\n    if i == 3:\n        break\n    print(i)\n    i += 1\nprint('Done')",
                        "test_cases": [{"input": "", "expected": "1\n2\nDone"}]
                    }
                },
                "pro": {
                    "content": "🔴 PRO LEVEL\n\n📘 Definition\nIterators and the 'else' clause in loops provide advanced control flow mechanics.\n\n🧠 Explanation\nA loop-else block runs only if the loop finished naturally (meaning it didn't hit a 'break').\n\n🔤 Advanced Syntax\nfor x in data:\n    ...\nelse:\n    print('Finished without break')\n\n📌 Example\nfor i in range(5):\n    if i == 10: break\nelse:\n    print('Loop complete')\n\n🌍 Use Case\nSearching through a database where the 'else' handles the 'Not Found' case efficiently.\n\n🧪 Knowledge Check\n1. When does the loop-else block NOT run?\n\n💻 Challenge\nSearch for n=5 in list [1,2,3,4]. If NOT found, use 'else' to print 'Missing'.",
                    "challenge": {
                        "title": "Search Else",
                        "description": "Search for 5 in L = [1,2,3,4]. Print 'Found' if exists, else 'Missing' using loop-else.",
                        "initial_code": "L = [1,2,3,4]\n# Loop with else",
                        "solution_code": "L = [1,2,3,4]\nfor x in L:\n    if x == 5:\n        print('Found')\n        break\nelse:\n    print('Missing')",
                        "test_cases": [{"input": "", "expected": "Missing"}]
                    }
                }
            }
        ]
    }
]

def populate_extra():
    # Similar to populate_curriculum but specifically for EXTRA_CURRICULUM_DATA
    print("🚀 Starting EXTRA Curriculum Population...")
    total_lessons = 0
    total_challenges = 0
    for module_entry in EXTRA_CURRICULUM_DATA:
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
                    order=topics.index(topic_entry) + 10, # Offset to avoid conflict
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
    populate_extra()
