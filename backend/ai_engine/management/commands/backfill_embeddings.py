import sys
import time
import logging
from django.core.management.base import BaseCommand
from core.models import Lesson
from lessons.models import LessonProfile, LessonChunk
from ai_engine.tasks import generate_lesson_embeddings

logger = logging.getLogger("ai_engine.embeddings")


class Command(BaseCommand):
    help = "Backfill embeddings for lessons"

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Regenerate all embeddings")

    def handle(self, *args, **options):
        force = options.get("force", False)
        lessons = Lesson.objects.all().order_by("id")
        total = lessons.count()
        if total == 0:
            self.stdout.write(self.style.WARNING("No lessons found"))
            return
        processed = 0
        failures = 0
        start = time.perf_counter()
        for lesson in lessons:
            processed += 1
            try:
                if not force:
                    has_profile = LessonProfile.objects.filter(lesson_id=lesson.id, embedding_vector__isnull=False).exists()
                    has_chunks = LessonChunk.objects.filter(lesson_id=lesson.id).exists()
                    if has_profile and has_chunks:
                        self._render_progress(processed, total)
                        continue
                generate_lesson_embeddings(lesson.id)
            except Exception as exc:
                failures += 1
                logger.error("Backfill embedding failed", extra={"lesson_id": lesson.id})
                logger.error(str(exc))
            self._render_progress(processed, total)
        duration = round(time.perf_counter() - start, 2)
        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(f"Backfill complete in {duration}s with {failures} failures"))

    def _render_progress(self, processed: int, total: int):
        width = 30
        ratio = processed / total if total else 1
        filled = int(width * ratio)
        bar = "=" * filled + "-" * (width - filled)
        percent = int(ratio * 100)
        sys.stdout.write(f"\r[{bar}] {processed}/{total} {percent}%")
        sys.stdout.flush()
