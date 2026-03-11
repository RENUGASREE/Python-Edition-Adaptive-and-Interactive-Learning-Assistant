from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from core.models import Lesson
from ai_engine.services import enqueue_lesson_embedding_update


@receiver(post_save, sender=Lesson)
def handle_lesson_embedding(sender, instance, **kwargs):
    if os.getenv("ENABLE_EMBEDDINGS", "").strip() not in ("1", "true", "True", "yes", "YES"):
        return
    enqueue_lesson_embedding_update(instance.id)
