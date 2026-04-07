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

    # 4. Seed Badges & Certificate Templates
    try:
        from core.models import Badge, CertificateTemplate
        
        print("🏅 Seeding Gamification & Certificates...")
        
        # Badges
        badges = [
            {"name": "Python Pioneer", "description": "Completed the first lesson in Python Edition."},
            {"name": "Quiz Master", "description": "Scored 100% on a module diagnostic quiz."},
            {"name": "Streak Star", "description": "Maintained a 7-day learning streak."},
            {"name": "Topic Pro", "description": "Reached 'Pro' level in any curriculum topic."},
            {"name": "Bug Hunter", "description": "Successfully debugged 5 complex Python scripts."},
            {"name": "Fast Finger", "description": "Completed a coding challenge in under 30 seconds."},
            {"name": "Deep Diver", "description": "Completed 100% of a module's content and challenges."},
            {"name": "AI Tinkerer", "description": "Used the AI Tutor to optimize or explain complex logic."},
            {"name": "Persistent", "description": "Logged in and learned for 7 consecutive days."},
            {"name": "Syntax Sage", "description": "Passed 5 quizzes without a single syntax error."},
            {"name": "Algorithm Architect", "description": "Mastered complex nested data structures and logic."},
            {"name": "Logic Legend", "description": "Completed Advanced sessions with 100% accuracy."}
        ]
        for b_data in badges:
            Badge.objects.get_or_create(name=b_data["name"], defaults={"description": b_data["description"]})

        # Certificate Templates
        templates = [
            {"code": "PY-FUND-01", "title": "Python Fundamentals", "description": "Certificate for mastering core Python syntax and logic."},
            {"code": "DS-ALGO-01", "title": "Data Structures", "description": "Certificate for advanced proficiency in Python data structures."},
            {"code": "ADV-PY-01", "title": "Advanced Python Mastery", "description": "Mastery of decorators, generators, and advanced concepts."},
            {"code": "OOP-PY-01", "title": "Object-Oriented Programming", "description": "Specialization in classes, inheritance, and OOP design."},
            {"code": "MASTER-PY-01", "title": "Master of Python", "description": "Final course completion certificate for the entire Python Edition curriculum."}
        ]
        for t_data in templates:
            CertificateTemplate.objects.get_or_create(code=t_data["code"], defaults={"title": t_data["title"], "description": t_data["description"]})
        
        # 5. Sync Existing Certificates (Generate UUIDs if missing)
        try:
            from core.models import Certificate
            import uuid
            print("📜 Syncing Certificate Verification Codes...")
            certs_to_update = Certificate.objects.filter(verification_code__isnull=True)
            if certs_to_update.exists():
                for cert in certs_to_update:
                    cert.verification_code = uuid.uuid4()
                    cert.save()
                print(f"✅ Synced {certs_to_update.count()} certificates.")
            else:
                print("ℹ️ All certificates already have verification codes.")
        except Exception as e:
            print(f"❌ Error syncing certificates: {e}")

        print("✅ Gamification & Certificates Seeded.")
    except Exception as e:
        print(f"❌ Error seeding gamification/certificates: {e}")

if __name__ == "__main__":
    setup_production()
