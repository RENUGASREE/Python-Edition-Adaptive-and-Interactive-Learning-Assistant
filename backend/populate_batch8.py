import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

BATCH8_DATA = [
    { "module_id": 19, "topics": [
        { "title": "Variables Types", "beginner": {"content": "🟢 BEGINNER LEVEL\n- Names for variables can contain letters, numbers, and underscores.", "challenge": {"title": "Var Naming", "description": "L = 5. print(L).", "initial_code": "L = 5\n# print", "solution_code": "L = 5\nprint(L)", "test_cases": [{"input": "", "expected": "5"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Assigning multiple values in one line: x, y = 5, 10.", "challenge": {"title": "Multi Assign", "description": "x, y = 1, 2. print(x, y).", "initial_code": "# code", "solution_code": "x, y = 1, 2\nprint(x, y)", "test_cases": [{"input": "", "expected": "1 2"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Id and memory address: id(x).", "challenge": {"title": "Var ID", "description": "x = 5. print(type(id(x))).", "initial_code": "x = 5\n# id", "solution_code": "x = 5\nprint(type(id(x)))", "test_cases": [{"input": "", "expected": "<class 'int'>"}]}} },
        { "title": "Number Methods", "beginner": {"content": "🟢 BEGINNER LEVEL\n- abs(x) and pow(x, y).", "challenge": {"title": "Abs Val", "description": "print abs(-10).", "initial_code": "# code", "solution_code": "print(abs(-10))", "test_cases": [{"input": "", "expected": "10"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- round(x, n) for dec precision.", "challenge": {"title": "Round Num", "description": "round 3.14159 to 2 digits.", "initial_code": "# code", "solution_code": "print(round(3.14159, 2))", "test_cases": [{"input": "", "expected": "3.14"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Complex() numbers.", "challenge": {"title": "Complex Type", "description": "create 1 + 2j and print its real part.", "initial_code": "# code", "solution_code": "c = complex(1, 2)\nprint(c.real)", "test_cases": [{"input": "", "expected": "1.0"}]}} }
    ]},
    { "module_id": 20, "topics": [
        { "title": "If-Elif-Else", "beginner": {"content": "🟢 BEGINNER LEVEL\n- if x > 0: print('Hi').", "challenge": {"title": "Check Zero", "description": "x=0. If 0 print 'Z'. Else 'N'.", "initial_code": "x = 0\n# code", "solution_code": "x = 0\nif x == 0: print('Z')\nelse: print('N')", "test_cases": [{"input": "", "expected": "Z"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Nested conditions.", "challenge": {"title": "Nested If", "description": "If x=1, if y=2, print 'B'.", "initial_code": "x=1; y=2\n# code", "solution_code": "x=1; y=2\nif x==1: \n  if y==2: print('B')", "test_cases": [{"input": "", "expected": "B"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Ternary operator: x = 'A' if y else 'B'.", "challenge": {"title": "Ternary Op", "description": "print 'Y' if True else 'N'.", "initial_code": "# code", "solution_code": "print('Y' if True else 'N')", "test_cases": [{"input": "", "expected": "Y"}]}} },
        { "title": "While Loops", "beginner": {"content": "🟢 BEGINNER LEVEL\n- while x < 5: x += 1.", "challenge": {"title": "While 3", "description": "While x<3, print x, x++.", "initial_code": "x = 0\n# while", "solution_code": "x = 0\nwhile x < 3:\n    print(x)\n    x += 1", "test_cases": [{"input": "", "expected": "0\n1\n2"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- While-Else loops.", "challenge": {"title": "While Else", "description": "Loop x once, print 'E' in else.", "initial_code": "x=0\nwhile x<1: x+=1\nelse: print('E')", "solution_code": "x=0\nwhile x<1: x+=1\nelse: print('E')", "test_cases": [{"input": "", "expected": "E"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Avoid infinite loops.", "challenge": {"title": "Loop Break", "description": "While True, break and print 'B'.", "initial_code": "# code", "solution_code": "while True:\n    break\nprint('B')", "test_cases": [{"input": "", "expected": "B"}]}} }
    ]}
]

def populate_batch8():
    print("🚀 Starting Batch 8 Population...")
    tl=0; tc=0
    for med in BATCH8_DATA:
        mid = med["module_id"]
        for topic in med["topics"]:
            title = topic["title"]
            for level in ["beginner", "intermediate", "pro"]:
                dl = level.capitalize()
                # Use module_id as well to avoid deleting cross-module lessons if titles collide
                Lesson.objects.filter(module_id=mid, title=title, difficulty=dl).delete()
                l = Lesson.objects.create(module_id=mid, title=title, difficulty=dl, content=topic[level]["content"], slug=title.lower().replace(" ", "-"), order=50, duration=15)
                tl += 1
                c_data = topic[level]["challenge"]
                Challenge.objects.filter(lesson_id=l.id).delete()
                Challenge.objects.create(lesson_id=l.id, title=c_data["title"], description=c_data["description"], initial_code=c_data["initial_code"], solution_code=c_data["solution_code"], test_cases=c_data["test_cases"], points=100, difficulty=dl)
                tc += 1
    print(f"✅ Created {tl} Lessons and {tc} Challenges.")

if __name__ == "__main__":
    populate_batch8()
