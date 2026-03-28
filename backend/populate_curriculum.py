import os
import sys
import django

# Set up Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Challenge
from curriculum_data import CURRICULUM_DATA

def populate():
    print("🚀 Starting Curriculum Population...")
    
    total_lessons = 0
    total_challenges = 0

    for module_entry in CURRICULUM_DATA:
        module_id = module_entry["module_id"]
        topics = module_entry["topics"]
        
        # Verify module exists
        if not Module.objects.filter(id=module_id).exists():
            print(f"⚠️ Module ID {module_id} not found. Skipping.")
            continue

        for topic_entry in topics:
            title = topic_entry["title"]
            print(f"📦 Processing Topic: {title}")
            
            for level in ["beginner", "intermediate", "pro"]:
                diff_label = level.capitalize()
                if level == "pro": diff_label = "Pro" # Ensure it matches "Pro" not "Advanced" if that's the standard
                
                content = topic_entry[level]["content"]
                challenge_data = topic_entry[level]["challenge"]
                
                # 1. Purge and Recreate Lesson
                Lesson.objects.filter(module_id=module_id, title=title, difficulty=diff_label).delete()
                lesson = Lesson.objects.create(
                    module_id=module_id,
                    title=title,
                    difficulty=diff_label,
                    content=content,
                    slug=title.lower().replace(" ", "-"),
                    order=topics.index(topic_entry) + 1,
                    duration=15
                )
                total_lessons += 1
                
                # 2. Purge and Recreate Challenge
                Challenge.objects.filter(lesson_id=lesson.id).delete()
                # Also purge potentially orphaned challenges with same title/difficulty
                Challenge.objects.filter(title=challenge_data["title"], difficulty=diff_label).delete()
                
                challenge = Challenge.objects.create(
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
                total_challenges += 1

    print(f"✅ Success! Created/Updated {total_lessons} Lessons and {total_challenges} Challenges.")

if __name__ == "__main__":
    populate()
