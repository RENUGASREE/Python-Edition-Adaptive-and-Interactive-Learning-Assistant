from django.db import models
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserBadge, XpEvent, Streak


class GamificationSummaryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        badges = list(UserBadge.objects.filter(user=request.user).select_related("badge"))
        xp_total = XpEvent.objects.filter(user=request.user).aggregate(total_points=models.Sum("points")).get("total_points") or 0
        streak = Streak.objects.filter(user=request.user).first()
        return Response({
            "badges": [{"code": badge.badge.code, "title": badge.badge.title} for badge in badges],
            "xp": xp_total,
            "streak": {
                "current": streak.current_streak if streak else 0,
                "longest": streak.longest_streak if streak else 0,
            },
        })
