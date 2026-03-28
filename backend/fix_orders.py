import os
import sys
import django

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson

def fix_lesson_orders():
    print("🛠️ Fixing lesson orders for sequential unlocking...")
    modules = Module.objects.all().order_by('order')
    
    for module in modules:
        # Get all lessons in this module, sorted by their current best-effort order and ID
        lessons = Lesson.objects.filter(module_id=module.id).order_by('order', 'id')
        
        # Unique titles in this module (topics)
        seen_topics = []
        topic_to_lessons = {} # title -> [Beginner, Intermediate, Pro]
        
        for l in lessons:
            if l.title not in seen_topics:
                seen_topics.append(l.title)
                topic_to_lessons[l.title] = []
            topic_to_lessons[l.title].append(l)
            
        # Now assign unique order index to each topic's lessons
        # All difficulty levels for the same topic should have the same 'order' index
        # so they occupy the same "slot" in the curriculum.
        for idx, title in enumerate(seen_topics):
            topic_order = idx + 1 # 1, 2, 3...
            for l in topic_to_lessons[title]:
                l.order = topic_order
                l.save(update_fields=['order'])
            print(f"✅ Topic '{title}' (Module {module.id}) set to order {topic_order}")

    print("🚀 All lesson orders normalized.")

if __name__ == "__main__":
    fix_lesson_orders()
