"""Lesson metadata services that support adaptive selection and RAG."""
from core.models import Lesson
from .models import LessonProfile, LessonChunk


def get_lessons_by_difficulty(difficulty: str):
    return Lesson.objects.filter(difficulty=difficulty).order_by("order", "id")


def upsert_lesson_profile(lesson_id: int, topic: str, difficulty: str, prerequisites=None, embedding_vector=None):
    profile, _ = LessonProfile.objects.update_or_create(
        lesson_id=lesson_id,
        defaults={
            "topic": topic,
            "difficulty": difficulty,
            "prerequisites": prerequisites or [],
            "embedding_vector": embedding_vector or [],
        },
    )
    return profile


def create_lesson_chunks(lesson_id: int, topic: str, chunks, embeddings):
    LessonChunk.objects.filter(lesson_id=lesson_id).delete()
    for content, embedding in zip(chunks, embeddings):
        LessonChunk.objects.create(
            lesson_id=lesson_id,
            topic=topic,
            content=content,
            embedding_vector=embedding,
        )
