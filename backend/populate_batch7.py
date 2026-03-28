import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge

BATCH7_DATA = [
    { "module_id": 21, "topics": [
        { "title": "String Methods", "beginner": {"content": "🟢 BEGINNER LEVEL\n- .upper(), .lower(), .capitalize() methods.", "challenge": {"title": "Upper Case", "description": "Print 'hi'.upper().", "initial_code": "# code", "solution_code": "print('hi'.upper())", "test_cases": [{"input": "", "expected": "HI"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- .strip(), .replace(), .split() methods.", "challenge": {"title": "Replace Char", "description": "Replace 'a' with 'o' in 'apple'.", "initial_code": "s = 'apple'\n# replace", "solution_code": "s = 'apple'\nprint(s.replace('a', 'o'))", "test_cases": [{"input": "", "expected": "opple"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- .find(), .count(), .join() and efficient string building.", "challenge": {"title": "Join List", "description": "Join ['a', 'b'] with '-' and print.", "initial_code": "# code", "solution_code": "print('-'.join(['a', 'b']))", "test_cases": [{"input": "", "expected": "a-b"}]}} },
        { "title": "Sets", "beginner": {"content": "🟢 BEGINNER LEVEL\n- Definition: Store unique items using {}.", "challenge": {"title": "Create Set", "description": "Create set {1, 2, 2} and print it.", "initial_code": "# code", "solution_code": "print({1, 2, 2})", "test_cases": [{"input": "", "expected": "{1, 2}"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Set intersection and union: s1.union(s2).", "challenge": {"title": "Set Union", "description": "Union of {1} and {2}. Print it.", "initial_code": "# code", "solution_code": "print({1}.union({2}))", "test_cases": [{"input": "", "expected": "{1, 2}"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Frozen sets and set performance O(1).", "challenge": {"title": "Intersection", "description": "Intersection of {1, 2} and {2, 3}. Print it.", "initial_code": "# code", "solution_code": "print({1, 2}.intersection({2, 3}))", "test_cases": [{"input": "", "expected": "{2}"}]}} }
    ]},
    { "module_id": 22, "topics": [
        { "title": "Math Module", "beginner": {"content": "🟢 BEGINNER LEVEL\n- Basic math.sqrt() and math.pi.", "challenge": {"title": "Sqrt 16", "description": "Import math and print sqrt(16).", "initial_code": "import math\n# print", "solution_code": "import math\nprint(math.sqrt(16))", "test_cases": [{"input": "", "expected": "4.0"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- math.ceil() and math.floor() rounding.", "challenge": {"title": "Ceil Val", "description": "Print math.ceil(4.2).", "initial_code": "import math\n# print", "solution_code": "import math\nprint(math.ceil(4.2))", "test_cases": [{"input": "", "expected": "5"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Trig functions and log calculations.", "challenge": {"title": "Log 100", "description": "Print math.log10(100).", "initial_code": "import math\n# print", "solution_code": "import math\nprint(math.log10(100))", "test_cases": [{"input": "", "expected": "2.0"}]}} }
    ]},
    { "module_id": 23, "topics": [
        { "title": "Iterators", "beginner": {"content": "🟢 BEGINNER LEVEL\n- Using iter() and next() on lists.", "challenge": {"title": "Next Item", "description": "L=[1]. i=iter(L). Print next(i).", "initial_code": "L = [1]\n# code", "solution_code": "L = [1]\ni = iter(L)\nprint(next(i))", "test_cases": [{"input": "", "expected": "1"}]}}, "intermediate": {"content": "🟡 INTERMEDIATE LEVEL\n- Implementing __iter__ and __next__ protocols.", "challenge": {"title": "Iter Protocol", "description": "Just print 'Iter ready'.", "initial_code": "print('Iter ready')", "solution_code": "print('Iter ready')", "test_cases": [{"input": "", "expected": "Iter ready"}]}}, "pro": {"content": "🔴 PRO LEVEL\n- Custom range-like iterators.", "challenge": {"title": "Last Iter", "description": "Print 'Done'.", "initial_code": "print('Done')", "solution_code": "print('Done')", "test_cases": [{"input": "", "expected": "Done"}]}} }
    ]}
]

def populate_batch7():
    print("🚀 Starting Batch 7 Population...")
    tl=0; tc=0
    for med in BATCH7_DATA:
        mid = med["module_id"]
        for topic in med["topics"]:
            title = topic["title"]
            for level in ["beginner", "intermediate", "pro"]:
                dl = level.capitalize()
                Lesson.objects.filter(module_id=mid, title=title, difficulty=dl).delete()
                l = Lesson.objects.create(module_id=mid, title=title, difficulty=dl, content=topic[level]["content"], slug=title.lower().replace(" ", "-"), order=140, duration=15)
                tl += 1
                c_data = topic[level]["challenge"]
                Challenge.objects.filter(lesson_id=l.id).delete()
                Challenge.objects.create(lesson_id=l.id, title=c_data["title"], description=c_data["description"], initial_code=c_data["initial_code"], solution_code=c_data["solution_code"], test_cases=c_data["test_cases"], points=100, difficulty=dl)
                tc += 1
    print(f"✅ Created {tl} Lessons and {tc} Challenges.")

if __name__ == "__main__":
    populate_batch7()
