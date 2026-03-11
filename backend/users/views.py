import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserMetricsSerializer
from .services import update_engagement, update_learning_velocity

logger = logging.getLogger("users.metrics")


class UserMetricsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(UserMetricsSerializer(request.user).data)
        except Exception:
            logger.exception("user_metrics_get_failed", extra={"user_id": request.user.id})
            return Response({
                "id": request.user.id,
                "email": request.user.email,
                "level": request.user.level,
                "masteryVector": request.user.mastery_vector or {},
                "engagement_score": request.user.engagement_score or 0.0,
                "diagnostic_completed": request.user.diagnostic_completed,
                "has_taken_quiz": request.user.has_taken_quiz,
                "learning_velocity": request.user.learning_velocity or 0.0,
            })

    def post(self, request):
        try:
            engagement_delta = request.data.get("engagementDelta")
            lesson_minutes = request.data.get("lessonMinutes")
            if engagement_delta is not None:
                update_engagement(request.user, float(engagement_delta))
            if lesson_minutes is not None:
                update_learning_velocity(request.user, float(lesson_minutes))
            return Response(UserMetricsSerializer(request.user).data)
        except Exception:
            logger.exception("user_metrics_post_failed", extra={"user_id": request.user.id})
            return Response(UserMetricsSerializer(request.user).data)
