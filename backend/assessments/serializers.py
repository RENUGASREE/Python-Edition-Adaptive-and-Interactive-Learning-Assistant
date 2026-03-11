from rest_framework import serializers
from .models import DiagnosticQuiz, DiagnosticQuestion, DiagnosticQuizAttempt, AssessmentInteraction, DiagnosticOption


class DiagnosticQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticQuiz
        fields = "__all__"


class DiagnosticQuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    class Meta:
        model = DiagnosticQuestion
        fields = ("id", "quiz", "topic", "difficulty", "text", "options", "correct_index", "points")

    def get_options(self, obj):
        # Prefer related DiagnosticOption records; fallback to JSONField if present
        opts = list(DiagnosticOption.objects.filter(question=obj).values("text", "is_correct"))
        if opts:
            return opts
        raw = obj.options or []
        return [{"text": str(t), "is_correct": (i == obj.correct_index)} for i, t in enumerate(raw)]


class DiagnosticAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticQuizAttempt
        fields = "__all__"


class AssessmentInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentInteraction
        fields = "__all__"
