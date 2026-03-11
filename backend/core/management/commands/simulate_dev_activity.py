from __future__ import annotations

import random
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from core.models import User, Lesson, Module, UserProgress, QuizAttempt
from lessons.models import LessonProfile
from assessments.models import DiagnosticQuiz, DiagnosticQuizAttempt, AssessmentInteraction
from gamification.services import add_xp, update_streak, award_badge
from evaluation.services import log_recommendation_event, mark_recommendation_accepted, mark_recommendation_completed
from recommendation.services import recommend_next


class Command(BaseCommand):
    help = (
        "Development simulator: generates realistic user events (diagnostic attempts, lesson completions, "
        "challenge/quiz interactions, mastery updates via normal flows, and recommendation events) "
        "to populate analytics dashboards during testing."
    )

    def add_arguments(self, parser):
        parser.add_argument("--username", default="admin", help="Target username to simulate activity for.")
        parser.add_argument("--days", type=int, default=7, help="How many days back to simulate.")
        parser.add_argument("--lesson-completions", type=int, default=8, help="How many lessons to mark completed.")
        parser.add_argument("--interactions", type=int, default=40, help="How many interactions to generate.")
        parser.add_argument("--seed", type=int, default=42, help="RNG seed for repeatable results.")

    def handle(self, *args, **options):
        username: str = options["username"]
        days: int = int(options["days"])
        lesson_completions: int = int(options["lesson_completions"])
        interactions: int = int(options["interactions"])
        seed: int = int(options["seed"])

        rng = random.Random(seed)
        now = timezone.now()
        start = now - timedelta(days=days)

        user = User.objects.filter(username=username).first()
        if not user:
            self.stdout.write(self.style.ERROR(f"User '{username}' not found. Create it first (or use --username)."))
            return

        lessons = list(Lesson.objects.all().order_by("module_id", "order", "id"))
        if not lessons:
            self.stdout.write(self.style.ERROR("No lessons found. Run seed_curriculum_data (or seed_platform_data) first."))
            return

        profiles = list(LessonProfile.objects.all())
        topic_pool = [p.topic for p in profiles if p.topic] or [l.title for l in lessons[:20]]

        with transaction.atomic():
            # Ensure a diagnostic quiz exists
            diagnostic = DiagnosticQuiz.objects.order_by("-id").first()
            if not diagnostic:
                diagnostic = DiagnosticQuiz.objects.create(title="Python Placement Diagnostic")

            # Create 2 diagnostic attempts to give mastery progression + learning gain
            # Use small numbers (0..1) because analytics expects overall_score in 0..1
            first_score = round(rng.uniform(0.25, 0.45), 4)
            last_score = round(min(0.95, first_score + rng.uniform(0.15, 0.35)), 4)

            attempt1 = DiagnosticQuizAttempt.objects.create(
                user=user,
                quiz=diagnostic,
                module_scores={"Module 1": first_score, "Module 2": first_score},
                overall_score=first_score,
                raw_score=first_score,
                weighted_score=first_score,
                difficulty_tier="Beginner",
                start_time=start + timedelta(hours=1),
                completed_at=start + timedelta(hours=1, minutes=12),
                locked=True,
                status="completed",
            )
            attempt2 = DiagnosticQuizAttempt.objects.create(
                user=user,
                quiz=diagnostic,
                module_scores={"Module 1": last_score, "Module 2": last_score},
                overall_score=last_score,
                raw_score=last_score,
                weighted_score=last_score,
                difficulty_tier="Intermediate" if last_score >= 0.55 else "Beginner",
                start_time=now - timedelta(days=max(1, days // 2), hours=2),
                completed_at=now - timedelta(days=max(1, days // 2), hours=1, minutes=40),
                locked=True,
                status="completed",
            )

            # Update user flags so curriculum unlocks + recommendations work
            user.diagnostic_completed = True
            user.has_taken_quiz = True
            # A simple level assignment based on last score
            if last_score < 0.5:
                user.level = "Beginner"
            elif last_score < 0.75:
                user.level = "Intermediate"
            else:
                user.level = "Advanced"
            user.save(update_fields=["diagnostic_completed", "has_taken_quiz", "level"])

            # Mark some lessons as completed across the last N days
            selected_lessons = lessons[: max(1, min(lesson_completions, len(lessons)))]
            progress_user_key = user.original_uuid or str(user.id)
            for i, lesson in enumerate(selected_lessons):
                completed_at = now - timedelta(days=min(days - 1, i), hours=rng.randint(0, 6))
                UserProgress.objects.update_or_create(
                    user_id=progress_user_key,
                    lesson_id=lesson.id,
                    defaults={
                        "completed": True,
                        "score": rng.randint(70, 100),
                        "last_code": "print('ok')",
                        "completed_at": completed_at,
                    },
                )
                add_xp(user, points=10, reason=f"Simulated lesson completion: {lesson.title}")
                update_streak(user)

            # Add quiz attempts notes to simulate module-level personalization (used by curriculum filtering)
            modules = list(Module.objects.all().order_by("order"))
            for module in modules[:3]:
                level = user.level
                # Store module-specific level markers the UI parses: module:<id>:level:<Level>
                QuizAttempt.objects.create(user=user, score=rng.randint(40, 100), notes=f"module:{module.id}:level:{level}")

            # Generate interactions across topics (quiz/challenge/lesson sources)
            sources = ["quiz", "challenge", "lesson"]
            for _ in range(interactions):
                topic = rng.choice(topic_pool)
                created_at = start + timedelta(seconds=rng.randint(0, int((now - start).total_seconds())))
                correctness = rng.random() > 0.35  # ~65% correct
                AssessmentInteraction.objects.create(
                    user=user,
                    topic=topic,
                    correctness=correctness,
                    time_spent=rng.uniform(8, 60),
                    hints_used=rng.randint(0, 3),
                    source=rng.choice(sources),
                    created_at=created_at,
                )

            # Log recommendation events + outcomes using the real recommender
            # (This also creates outcomes rows used by evaluation metrics.)
            for _ in range(4):
                rec = recommend_next(user)
                lesson_id = rec.get("recommended_lesson_id")
                topic = rec.get("next_topic")
                confidence = float(rec.get("confidence_score") or 0.0)
                event = log_recommendation_event(
                    user=user,
                    algorithm_name=rec.get("algorithm") or "strategy_a",
                    recommended_lesson_id=lesson_id,
                    recommended_topic=topic,
                    confidence=confidence,
                )
                if lesson_id:
                    mark_recommendation_accepted(user, lesson_id)
                    # Fake a completion for half of them
                    if rng.random() > 0.5:
                        mark_recommendation_completed(user, lesson_id, mastery_before=0.4, mastery_after=0.55)

            # Award a couple of badges to make Achievements look active
            award_badge(user, "diagnostic-done")
            award_badge(user, "first-lesson")

        self.stdout.write(
            self.style.SUCCESS(
                "Simulation complete for user "
                f"'{username}'. Diagnostic attempts: 2, lesson completions: {len(selected_lessons)}, "
                f"interactions: {interactions}."
            )
        )

