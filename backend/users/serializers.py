from rest_framework import serializers
from core.models import User


class UserMetricsSerializer(serializers.ModelSerializer):
    masteryVector = serializers.JSONField(source="mastery_vector", required=False)

    class Meta:
        model = User
        fields = ("id", "email", "level", "masteryVector", "engagement_score", "diagnostic_completed", "has_taken_quiz", "learning_velocity")
