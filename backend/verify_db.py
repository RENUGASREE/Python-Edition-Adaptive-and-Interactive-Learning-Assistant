import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'python_edition_django.settings')
django.setup()

from core.models import Module, Lesson, Quiz, Question

def verify():
    print(f"--- Database Verification ---")
    
    # Modules
    m_count = Module.objects.count()
    print(f"Modules Total: {m_count}")
    if m_count > 0:
        first_m = Module.objects.order_by('order').first()
        print(f"First Module ID: {first_m.id} (Title: {first_m.title})")
    
    # Lessons
    l_count = Lesson.objects.count()
    print(f"Lessons Total: {l_count}")
    if l_count > 0:
        first_l = Lesson.objects.first()
        print(f"Sample Lesson ID: {first_l.id} (Module ID: {first_l.module_id})")
        
    # Placement Quiz
    quiz = Quiz.objects.filter(id="quiz-placement-test").first()
    if quiz:
        q_count = Question.objects.filter(quiz_id=quiz.id).count()
        print(f"Placement Quiz ID: {quiz.id}")
        print(f"Placement Questions Count: {q_count}")
        if q_count > 0:
            first_q = Question.objects.filter(quiz_id=quiz.id).first()
            print(f"Sample Question ID: {first_q.id}")
    else:
        print("Placement Quiz NOT FOUND!")

if __name__ == "__main__":
    verify()
