import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from core.models import Lesson, Challenge

def get_challenge_data(topic, level):
    if level == "Beginner":
        return {
            "title": f"{topic} Mastery I",
            "desc": f"Write a simple Python script demonstrating high-level concepts of {topic}. Print 'Successfully implemented {topic} basics.'",
            "init": f"# Beginner challenge for {topic}\n",
            "test_cases": [{"input": "", "expected": f"Successfully implemented {topic} basics.\n", "hidden": False}]
        }
    elif level == "Intermediate":
        return {
            "title": f"{topic} Mastery II",
            "desc": f"Create a function `process_{topic.lower().replace(' ', '_')}(val)` that returns val appended with ' (Processed)'. Call it and print the result for 'A'.",
            "init": f"# Intermediate challenge for {topic}\ndef process_{topic.lower().replace(' ', '_')}(val):\n    return val + ' (Processed)'\n\n# Call and print below\n",
            "test_cases": [{"input": "", "expected": "A (Processed)\n", "hidden": False}]
        }
    else: # Pro
        return {
            "title": f"{topic} Mastery III",
            "desc": f"Build a pro-grade validation system for {topic}. Print 'Data Validated' if the input matches 'SECRET', otherwise print 'Access Denied'.",
            "init": f"# Pro challenge for {topic}\nval = input()\n# Your logic here\n",
            "test_cases": [
                {"input": "SECRET", "expected": "Data Validated\n"},
                {"input": "WRONG", "expected": "Access Denied\n"}
            ]
        }

def update_challenges_180():
    lessons = Lesson.objects.all().order_by('order')
    count = 0
    for lesson in lessons:
        # Extract topic from title "Name (Level)"
        if "(" in lesson.title:
            topic = lesson.title.split("(")[0].strip()
            level = lesson.difficulty
        else:
            topic = lesson.title
            level = lesson.difficulty or "Beginner"
            
        data = get_challenge_data(topic, level)
        
        # CLEAR solution binary to ensure the Runner logic uses the user input
        ch, created = Challenge.objects.update_or_create(
            lesson_id=lesson.id,
            defaults={
                "title": data["title"],
                "description": data["desc"],
                "initial_code": data["init"],
                "test_cases": data["test_cases"],
                "solution_code": "",
                "difficulty": level
            }
        )
        print(f"[{'NEW' if created else 'UPD'}] {ch.title} for {lesson.title}")
        count += 1
    
    print(f"\nCompleted! {count} challenges updated.")

if __name__ == "__main__":
    update_challenges_180()
