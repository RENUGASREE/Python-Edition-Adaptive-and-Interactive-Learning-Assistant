from django.core.management.base import BaseCommand
from core.models import Module, Lesson
from django.utils.text import slugify

class Command(BaseCommand):
    help = "Seed modules and lessons (titles only) with understandable string IDs"

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Cleaning up modules and lessons...")
        Module.objects.all().delete()
        Lesson.objects.all().delete()

        modules_list = [
            "Python Basics",
            "Data Types",
            "Control Flow",
            "Functions",
            "Modules & Packages",
            "File Handling",
            "Error Handling",
            "OOP",
            "Advanced Python",
            "Real-world Projects"
        ]

        levels = ["Beginner", "Intermediate", "Pro"]

        self.stdout.write(f"🚀 Seeding {len(modules_list)} modules and {len(modules_list) * 10 * 3} lessons...")
        
        for i, module_name in enumerate(modules_list, start=1):
            m_id = f"mod-{slugify(module_name)}"
            module = Module.objects.create(
                id=m_id,
                title=module_name, 
                order=i,
                description=f"Deep dive into {module_name} concepts, syntax, and best practices."
            )

            for j in range(1, 11):
                for level in levels:
                    lesson_title = f"{module_name} Lesson {j} ({level})"
                    l_id = f"les-{slugify(module_name)}-{j}-{slugify(level)}"
                    Lesson.objects.create(
                        id=l_id,
                        module_id=m_id,
                        title=lesson_title,
                        slug=slugify(lesson_title),
                        order=j,
                        difficulty=level,
                        content=f"Detailed educational content for {lesson_title} will be added here.",
                        duration=15
                    )

        self.stdout.write(self.style.SUCCESS(f"✅ Created {Module.objects.count()} Modules and {Lesson.objects.count()} Lessons"))
