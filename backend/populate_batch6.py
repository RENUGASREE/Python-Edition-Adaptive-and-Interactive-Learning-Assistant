import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

BATCH6_DATA = [
    { "module_id": 19, "topics": [
        { "title": "Input & Output", "beginner": {"content": "🟢 BEGINNER LEVEL\n\n- Definition: Getting data from users and showing it.\n- Explanation: input() waits for user typing, print() shows it.\n- Example: name = input('Name? '); print(name).", "challenge": {"title": "Say Name", "description": "Ask for input 'Enter Name: ' and print it.", "initial_code": "# code", "solution_code": "name = input('Enter Name: ')\nprint(name)", "test_cases": [{"input": "Renuga", "expected": "Enter Name: \nRenuga"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n\n- Formatted strings (f-strings) and input casting.\n- Example: age = int(input('Age? ')).", "challenge": {"title": "Age Check", "description": "Input 'Enter Age: ', cast to int, print age + 5.", "initial_code": "# code", "solution_code": "a = int(input('Enter Age: '))\nprint(a + 5)", "test_cases": [{"input": "20", "expected": "Enter Age: \n25"}]}}, "pro": {"content": "🔴 PRO LEVEL\n\n- Multi-line f-strings and sys.stdout basics.", "challenge": {"title": "Multi F-string", "description": "Print name and age on new lines using one f-string.", "initial_code": "n='R'; a=20\n# print", "solution_code": "n='R'; a=20\nprint(f'{n}\\n{a}')", "test_cases": [{"input": "", "expected": "R\n20"}]}} },
        { "title": "Type Casting", "beginner": {"content": "🟢 BEGINNER LEVEL\n\n- Definition: Converting one data type to another.\n- Example: int('5') = 5.", "challenge": {"title": "Str to Int", "description": "Convert '10' to int and print it.", "initial_code": "s = '10'\n# cast", "solution_code": "s = '10'\nprint(int(s))", "test_cases": [{"input": "", "expected": "10"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n\n- Implicit vs Explicit casting.\n- Example: float(10) = 10.0.", "challenge": {"title": "Int to Float", "description": "Convert 5 to float and print it.", "initial_code": "# code", "solution_code": "print(float(5))", "test_cases": [{"input": "", "expected": "5.0"}]}}, "pro": {"content": "🔴 PRO LEVEL\n\n- Complex casting and handling NaN/Inf check.", "challenge": {"title": "Bool Cast", "description": "Print result of bool('') and bool('Hi').", "initial_code": "# code", "solution_code": "print(bool(''))\nprint(bool('Hi'))", "test_cases": [{"input": "", "expected": "False\nTrue"}]}} }
    ]},
    { "module_id": 21, "topics": [
        { "title": "Tuples", "beginner": {"content": "🟢 BEGINNER LEVEL\n- Definition: Immutable lists using ().", "challenge": {"title": "Create Tuple", "description": "Create tuple (1, 2) and print it.", "initial_code": "# code", "solution_code": "t = (1, 2)\nprint(t)", "test_cases": [{"input": "", "expected": "(1, 2)"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Tuple unpacking: x, y = (1, 2).", "challenge": {"title": "Unpack Tuple", "description": "Unpack (10, 20) into a, b. Print a+b.", "initial_code": "t = (10, 20)\n# unpack", "solution_code": "t = (10, 20)\na, b = t\nprint(a + b)", "test_cases": [{"input": "", "expected": "30"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Nested tuples and hashability.", "challenge": {"title": "Nested Tuple", "description": "Print the second element of second tuple in ((1,2), (3,4)).", "initial_code": "t = ((1,2), (3,4))\n# print", "solution_code": "t = ((1,2), (3,4))\nprint(t[1][1])", "test_cases": [{"input": "", "expected": "4"}]}} }
    ]}
]

def populate_batch6():
    print("🚀 Starting Batch 6 Population...")
    tl=0; tc=0
    for med in BATCH6_DATA:
        mid = med["module_id"]
        for topic in med["topics"]:
            title = topic["title"]
            for level in ["beginner", "intermediate", "pro"]:
                dl = level.capitalize()
                Lesson.objects.filter(module_id=mid, title=title, difficulty=dl).delete()
                l = Lesson.objects.create(module_id=mid, title=title, difficulty=dl, content=topic[level]["content"], slug=title.lower().replace(" ", "-"), order=120, duration=15)
                tl += 1
                c_data = topic[level]["challenge"]
                Challenge.objects.filter(lesson_id=l.id).delete()
                Challenge.objects.create(lesson_id=l.id, title=c_data["title"], description=c_data["description"], initial_code=c_data["initial_code"], solution_code=c_data["solution_code"], test_cases=c_data["test_cases"], points=100, difficulty=dl)
                tc += 1
    print(f"✅ Created {tl} Lessons and {tc} Challenges.")

if __name__ == "__main__":
    populate_batch6()
