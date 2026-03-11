from rest_framework import serializers
from core.models import Lesson
from .models import LessonProfile, LessonChunk


class LessonProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProfile
        fields = "__all__"


class LessonChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonChunk
        fields = "__all__"


class LessonDetailSerializer(serializers.ModelSerializer):
    topic = serializers.SerializerMethodField()
    prerequisites = serializers.SerializerMethodField()
    embeddingVector = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = ("id", "module_id", "title", "slug", "content", "order", "difficulty", "duration", "topic", "prerequisites", "embeddingVector")

    def _profile(self, obj):
        return LessonProfile.objects.filter(lesson_id=obj.id).first()

    def get_topic(self, obj):
        profile = self._profile(obj)
        return profile.topic if profile else None

    def get_prerequisites(self, obj):
        profile = self._profile(obj)
        return profile.prerequisites if profile else []

    def get_embeddingVector(self, obj):
        profile = self._profile(obj)
        return profile.embedding_vector if profile else []
