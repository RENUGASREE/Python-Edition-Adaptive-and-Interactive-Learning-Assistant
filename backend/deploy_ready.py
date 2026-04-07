import os
import sys
import django
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

def setup_production():
    User = get_user_model()
    admin_user = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")

    # 1. Create Superuser if not exists
    if not User.objects.filter(username=admin_user).exists():
        print(f"👤 Creating superuser: {admin_user}...")
        User.objects.create_superuser(admin_user, admin_email, admin_password)
        print("✅ Superuser created.")
    else:
        print("ℹ️ Superuser already exists.")

    # 2. Run Quizzes Seed (Diagnostic)
    try:
        from seed_quiz import seed_quiz_questions
        seed_quiz_questions()
    except Exception as e:
        print(f"❌ Error seeding diagnostic quizzes: {e}")

    # 3. Seed Curriculum (Modules, Lessons, Challenges)
    try:
        from curriculum_data import CURRICULUM_DATA
        from core.models import Module, Lesson, Challenge
        
        print("📚 Seeding Curriculum Data...")
        for m_idx, module_data in enumerate(CURRICULUM_DATA):
            m_id = str(module_data["module_id"])
            m_title = "Python Fundamentals" if m_id == "19" else "Data Structures"
            
            module, _ = Module.objects.update_or_create(
                id=m_id,
                defaults={
                    "title": m_title,
                    "order": m_idx,
                    "description": f"Master the essentials of {m_title}."
                }
            )

            for t_idx, topic_data in enumerate(module_data["topics"]):
                topic_title = topic_data["title"]
                
                # In this structure, Lessons are tied to Modules and Topics via ID strings
                for level in ["beginner", "intermediate", "pro"]:
                    if level in topic_data:
                        data = topic_data[level]
                        l_id = f"{slugify(topic_title)}-{level}"
                        
                        # Create/Update Lesson
                        lesson, _ = Lesson.objects.update_or_create(
                            id=l_id,
                            defaults={
                                "module_id": m_id,
                                "title": f"{topic_title} ({level.capitalize()})",
                                "slug": l_id,
                                "content": data["content"],
                                "order": t_idx,
                                "difficulty": level.capitalize(),
                                "duration": 15
                            }
                        )
                        
                        # Create/Update Challenge
                        c_data = data["challenge"]
                        Challenge.objects.update_or_create(
                            id=f"challenge-{l_id}",
                            defaults={
                                "lesson_id": l_id,
                                "title": c_data["title"],
                                "description": c_data["description"],
                                "initial_code": c_data["initial_code"],
                                "solution_code": c_data["solution_code"],
                                "test_cases": c_data["test_cases"],
                                "difficulty": level.capitalize(),
                                "points": 10
                            }
                        )
        print("✅ Curriculum Seeded.")
    except Exception as e:
        print(f"❌ Error seeding curriculum: {e}")

if __name__ == "__main__":
    setup_production()
