import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import mastery_progression, learning_gain, strongest_weakest_topics, engagement_index, risk_score, interaction_mastery_series

logger = logging.getLogger("analytics.views")


class AnalyticsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            weakest, strongest = strongest_weakest_topics(request.user)
            return Response({
                "masteryProgression": mastery_progression(request.user),
                "interactionSeries": interaction_mastery_series(request.user),
                "learningGain": learning_gain(request.user),
                "weakestTopic": weakest,
                "strongestTopic": strongest,
                "engagementIndex": engagement_index(request.user),
                "riskScore": risk_score(request.user),
            })
        except Exception:
            logger.exception("analytics_view_failed", extra={"user_id": request.user.id})
            return Response({
                "masteryProgression": [],
                "interactionSeries": [],
                "learningGain": 0.0,
                "weakestTopic": None,
                "strongestTopic": None,
                "engagementIndex": 0.0,
                "riskScore": 0.0,
            })
