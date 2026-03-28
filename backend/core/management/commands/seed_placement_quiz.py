from django.core.management.base import BaseCommand
from core.models import Quiz, Question

class Command(BaseCommand):
    help = "Seed placement quiz with 40 questions and understandable string IDs"

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Cleaning up old placement quizzes...")
        Quiz.objects.filter(id="quiz-placement-test").delete()
        Question.objects.filter(quiz_id="quiz-placement-test").delete()

        quiz = Quiz.objects.create(
            id="quiz-placement-test",
            title="Placement Test"
        )

        self.stdout.write(f"🚀 Seeding 40 quiz questions for {quiz.title}...")

        for i in range(1, 41):
            q_id = f"ques-placement-{i}"
            Question.objects.create(
                id=q_id,
                quiz_id="quiz-placement-test",
                text=f"Placement Quiz Sample Question {i}: What is the output of `print(type([]))` in Python?",
                type="mcq",
                options=[
                    {"text": "<class 'list'>", "correct": True},
                    {"text": "<class 'dict'>", "correct": False},
                    {"text": "<class 'tuple'>", "correct": False},
                    {"text": "<class 'set'>", "correct": False},
                ],
                points=1
            )

        self.stdout.write(self.style.SUCCESS(f"✅ Created {Quiz.objects.count()} Quiz and {Question.objects.filter(quiz_id='quiz-placement-test').count()} Questions"))
