import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "python_edition_django.settings")
django.setup()

from core.models import Lesson, Quiz, Question

QUIZ_DATA = {
    "Strings Basics": [
        {
            "text": "What is the main purpose of strings basics in Python?",
            "options": [
                {"text": "To solve problems and build programs", "is_correct": True},
                {"text": "To slow down the computer", "is_correct": False},
                {"text": "To create errors", "is_correct": False},
                {"text": "To make code unreadable", "is_correct": False}
            ]
        },
        {
            "text": "Which is a best practice when learning strings basics?",
            "options": [
                {"text": "Practice with small examples and test your code", "is_correct": True},
                {"text": "Skip the fundamentals", "is_correct": False},
                {"text": "Copy code without understanding it", "is_correct": False},
                {"text": "Avoid asking questions", "is_correct": False}
            ]
        }
    ]
}

def update_quizzes():
    count = 0
    for lesson_title, questions in QUIZ_DATA.items():
        lesson = Lesson.objects.filter(title__icontains=lesson_title).first()
        if not lesson:
            print(f"Skipping {lesson_title}: Lesson not found")
            continue
            
        quiz, created = Quiz.objects.get_or_create(lesson_id=lesson.id, defaults={"title": f"Quiz: {lesson.title}"})
        
        # Clear existing questions for this quiz to avoid duplicates
        Question.objects.filter(quiz_id=quiz.id).delete()
        
        for q_data in questions:
            Question.objects.create(
                quiz_id=quiz.id,
                text=q_data["text"],
                options=q_data["options"],
                points=10
            )
        print(f"✅ Updated quiz for [{lesson.title}] with {len(questions)} questions")
        count += 1

    print(f"\nDone! Updated {count} quizzes.")

if __name__ == "__main__":
    update_quizzes()
