from django.db import models
from django.conf import settings

if "pgvector.django" in settings.INSTALLED_APPS:
    from pgvector.django import VectorField
    EMBEDDING_FIELD = VectorField(dimensions=1536, null=True, blank=True)
else:
    # Use JSONField for local fallback without vector extension
    EMBEDDING_FIELD = models.JSONField(default=list, blank=True)


class LessonProfile(models.Model):
    lesson_id = models.CharField(max_length=255, unique=True)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    prerequisites = models.JSONField(default=list, blank=True)
    embedding_vector = EMBEDDING_FIELD

    def __str__(self):
        return f"Profile: {self.topic} ({self.lesson_id})"


class LessonChunk(models.Model):
    lesson_id = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    content = models.TextField()
    embedding_vector = EMBEDDING_FIELD
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chunk: {self.topic} ({self.lesson_id})"
