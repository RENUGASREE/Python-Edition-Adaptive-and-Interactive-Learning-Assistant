import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import mastery_progression, learning_gain, strongest_weakest_topics, engagement_index, risk_score, interaction_mastery_series
from .models import SkillGapAnalysis, LearningPlan
from .services.skill_analysis import analyze_user_skill_gaps

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
                "skillGaps": [
                    {"topic": g.topic, "accuracy": g.accuracy, "status": g.status}
                    for g in SkillGapAnalysis.objects.filter(user=request.user).order_by('topic')
                ],
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
                "skillGaps": [],
            })


class SkillGapView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        gaps_qs = SkillGapAnalysis.objects.filter(user=request.user).order_by('topic')
        if not gaps_qs.exists():
            analyze_user_skill_gaps(request.user)
            gaps_qs = SkillGapAnalysis.objects.filter(user=request.user).order_by('topic')
        weak = []
        improving = []
        strong = []
        for g in gaps_qs:
            if g.status == "WEAK":
                weak.append(g.topic)
            elif g.status == "IMPROVING":
                improving.append(g.topic)
            elif g.status == "STRONG":
                strong.append(g.topic)
        return Response({
            "weak_topics": weak,
            "improving_topics": improving,
            "strong_topics": strong,
        })


class LearningPlanView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        plan = LearningPlan.objects.filter(user=request.user).order_by("-generated_at").first()
        if not plan:
            analyze_user_skill_gaps(request.user)
            plan = LearningPlan.objects.filter(user=request.user).order_by("-generated_at").first()
        if not plan:
            return Response({
                "recommendedModules": [],
                "recommendedLessons": [],
                "reasoning": "",
                "generatedAt": None,
            })
        return Response({
            "recommendedModules": plan.recommended_modules,
            "recommendedLessons": plan.recommended_lessons,
            "reasoning": plan.reasoning or "",
            "generatedAt": plan.generated_at.isoformat(),
        })
