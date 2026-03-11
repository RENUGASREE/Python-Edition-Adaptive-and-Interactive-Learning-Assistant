from django.db import models

EMBEDDING_FIELD = models.JSONField(default=list, blank=True)


class LessonProfile(models.Model):
    lesson_id = models.IntegerField(unique=True)
    topic = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=50)
    prerequisites = models.JSONField(default=list, blank=True)
    embedding_vector = EMBEDDING_FIELD


class LessonChunk(models.Model):
    lesson_id = models.IntegerField()
    topic = models.CharField(max_length=255)
    content = models.TextField()
    embedding_vector = EMBEDDING_FIELD
    created_at = models.DateTimeField(auto_now_add=True)
