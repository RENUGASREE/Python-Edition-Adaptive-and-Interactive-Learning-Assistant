import logging
import time
from django.db import transaction
from core.models import Lesson
from lessons.models import LessonProfile, LessonChunk
from ai_engine.services import embed_text

logger = logging.getLogger("ai_engine.embeddings")


def generate_lesson_embeddings(lesson_id: int):
    start = time.perf_counter()
    lesson = Lesson.objects.filter(id=lesson_id).first()
    if not lesson:
        logger.warning("Lesson not found for embedding", extra={"lesson_id": lesson_id})
        return
    profile = LessonProfile.objects.filter(lesson_id=lesson_id).first()
    topic = profile.topic if profile and profile.topic else lesson.title
    content = lesson.content or ""
    chunks = [chunk.strip() for chunk in content.split("\n\n") if chunk.strip()]
    if not chunks:
        logger.warning("No content chunks for embedding", extra={"lesson_id": lesson_id})
        return
    embeddings = [embed_text(chunk) for chunk in chunks]
    lesson_embedding = embed_text(content)
    with transaction.atomic():
        LessonChunk.objects.filter(lesson_id=lesson_id).delete()
        for chunk, vector in zip(chunks, embeddings):
            LessonChunk.objects.create(
                lesson_id=lesson_id,
                topic=topic,
                content=chunk,
                embedding_vector=vector,
            )
        if profile:
            profile.embedding_vector = lesson_embedding
            profile.topic = profile.topic or topic
            profile.difficulty = profile.difficulty or (lesson.difficulty or "Beginner")
            profile.save(update_fields=["embedding_vector", "topic", "difficulty"])
        else:
            LessonProfile.objects.create(
                lesson_id=lesson_id,
                topic=topic,
                difficulty=lesson.difficulty or "Beginner",
                prerequisites=[],
                embedding_vector=lesson_embedding,
            )
    duration = round(time.perf_counter() - start, 3)
    logger.info("Embedding generation complete", extra={"lesson_id": lesson_id, "duration_seconds": duration, "chunks": len(chunks)})
