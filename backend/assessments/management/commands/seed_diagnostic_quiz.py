from django.core.management.base import BaseCommand
from django.db import transaction
from assessments.models import DiagnosticQuiz, DiagnosticQuestion


class Command(BaseCommand):
    help = "Seed the 30-question diagnostic quiz with topic tags, difficulty mix, and points"

    def handle(self, *args, **options):
        quiz, _ = DiagnosticQuiz.objects.get_or_create(title="Diagnostic Quiz")
        DiagnosticQuestion.objects.filter(quiz=quiz).delete()

        topics = [
            "Python Basics", "Control Flow", "Loops", "Functions", "Data Structures", "OOP", "Comprehensions", "Error Handling"
        ]
        total_questions = 30
        distribution = {
            "easy": int(total_questions * 0.30),
            "medium": int(total_questions * 0.40),
            "hard": total_questions - int(total_questions * 0.30) - int(total_questions * 0.40),
        }
        points_map = {"easy": 1, "medium": 2, "hard": 3}
        questions = []

        idx = 0
        for difficulty, count in distribution.items():
            for _ in range(count):
                topic = topics[idx % len(topics)]
                idx += 1
                options = [
                    f"{topic} correct statement",
                    f"{topic} incorrect statement",
                    "Unrelated Python topic",
                    "Invalid syntax",
                ]
                questions.append(DiagnosticQuestion(
                    quiz=quiz,
                    topic=topic,
                    difficulty=difficulty,
                    text=f"[{topic}] Choose the correct option ({difficulty}).",
                    options=options,
                    correct_index=0,
                    points=points_map[difficulty],
                ))

        with transaction.atomic():
            DiagnosticQuestion.objects.bulk_create(questions)

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(questions)} diagnostic questions with difficulty distribution and points."))
