from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import LessonProfileSerializer, LessonDetailSerializer
from .services import get_lessons_by_difficulty, upsert_lesson_profile
from .models import LessonProfile
from ai_engine.services import enqueue_lesson_embedding_update
from core.models import Lesson


class LessonProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, lesson_id: int):
        profile = LessonProfile.objects.filter(lesson_id=lesson_id).first()
        if not profile:
            return Response({"message": "Lesson profile not found"}, status=404)
        return Response(LessonProfileSerializer(profile).data)

    def post(self, request, lesson_id: int):
        topic = request.data.get("topic")
        difficulty = request.data.get("difficulty")
        prerequisites = request.data.get("prerequisites", [])
        embedding_vector = request.data.get("embeddingVector", [])
        if not topic or not difficulty:
            return Response({"message": "topic and difficulty are required"}, status=400)
        profile = upsert_lesson_profile(lesson_id, topic, difficulty, prerequisites, embedding_vector)
        lesson = Lesson.objects.filter(id=lesson_id).first()
        if lesson:
            enqueue_lesson_embedding_update(lesson_id)
        return Response(LessonProfileSerializer(profile).data)


class LessonByDifficultyView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        difficulty = request.query_params.get("difficulty", "Beginner")
        lessons = get_lessons_by_difficulty(difficulty)
        return Response(LessonDetailSerializer(lessons, many=True).data)
