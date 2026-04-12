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
        fields = ("id", "quiz", "topic", "difficulty", "text", "options", "points")

    def get_options(self, obj):
        opts = list(
            DiagnosticOption.objects.filter(question=obj)
            .order_by("id")  # Always stable order — matches correct_index
            .values("id", "text")
        )
        if not opts:
            raw = obj.options or []
            opts = [{"id": f"raw-{obj.id}-{i}", "text": str(t)} for i, t in enumerate(raw)]
        return opts


class DiagnosticQuizAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticQuizAttempt
        fields = "__all__"


class AssessmentInteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentInteraction
        fields = "__all__"
