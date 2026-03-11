from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .serializers import DiagnosticQuizSerializer, DiagnosticQuestionSerializer
from .models import DiagnosticQuiz, DiagnosticQuestion, DiagnosticQuizAttempt
from .services import score_diagnostic


class DiagnosticQuizView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        quiz = (
            DiagnosticQuiz.objects.filter(title__iexact="Python Placement Diagnostic").order_by("-id").first()
            or DiagnosticQuiz.objects.order_by("-id").first()
        )
        if not quiz:
            return Response({"message": "No diagnostic quiz found"}, status=404)
        questions = DiagnosticQuestion.objects.filter(quiz=quiz)
        attempt = DiagnosticQuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by("-id").first()
        return Response({
            "quiz": DiagnosticQuizSerializer(quiz).data,
            "questions": DiagnosticQuestionSerializer(questions, many=True).data,
            "attemptMeta": {
                "attemptId": attempt.id if attempt else None,
                "startTime": attempt.start_time.isoformat() if attempt and attempt.start_time else None,
                "durationSeconds": attempt.duration_seconds if attempt else 900,
                "completedAt": attempt.completed_at.isoformat() if attempt and attempt.completed_at else None,
                "violationCount": attempt.violation_count if attempt else 0,
                "locked": bool(attempt.locked) if attempt else False,
            }
        })


class DiagnosticSubmitView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        quiz_id = request.data.get("quizId")
        answers = request.data.get("answers", [])
        violation_count = int(request.data.get("violationCount", 0) or 0)
        if not quiz_id:
            return Response({"message": "quizId is required"}, status=400)
        quiz = DiagnosticQuiz.objects.filter(id=int(quiz_id)).first()
        if not quiz:
            return Response({"message": "Quiz not found"}, status=404)
        attempt = DiagnosticQuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by("-id").first()
        now = timezone.now()
        if not attempt:
            attempt = DiagnosticQuizAttempt.objects.create(
                user=request.user,
                quiz=quiz,
                start_time=now,
                duration_seconds=900,
                violation_count=violation_count,
            )
        if attempt.locked or attempt.completed_at:
            return Response({"message": "Quiz already submitted"}, status=409)
        attempt.violation_count = violation_count
        # Violation auto-complete
        if violation_count >= 3:
            attempt.status = "violated"
            # proceed to scoring; treat as completed
        # Timer enforcement
        start = attempt.start_time or now
        deadline = start + timezone.timedelta(seconds=attempt.duration_seconds or 900)
        time_up = now > deadline
        module_scores, raw_score, weighted, tier = score_diagnostic(request.user, int(quiz_id), answers, violation_count=violation_count)
        attempt.module_scores = module_scores
        attempt.overall_score = raw_score
        attempt.raw_score = raw_score
        attempt.weighted_score = weighted
        attempt.difficulty_tier = tier
        attempt.completed_at = now
        attempt.locked = True
        attempt.save(update_fields=["module_scores", "overall_score", "raw_score", "weighted_score", "difficulty_tier", "completed_at", "locked", "status", "violation_count"])
        return Response({
            "moduleScores": module_scores,
            "overallScore": raw_score,
            "weightedScore": weighted,
            "difficultyTier": tier,
            "masteryVector": request.user.mastery_vector or {},
            "timeUp": time_up,
            "violations": violation_count,
        })

class DiagnosticStartView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        quiz = (
            DiagnosticQuiz.objects.filter(title__iexact="Python Placement Diagnostic").order_by("-id").first()
            or DiagnosticQuiz.objects.order_by("-id").first()
        )
        if not quiz:
            return Response({"message": "No diagnostic quiz found"}, status=404)
        attempt = DiagnosticQuizAttempt.objects.filter(user=request.user, quiz=quiz).order_by("-id").first()
        now = timezone.now()
        if attempt and (attempt.locked or attempt.completed_at):
            return Response({"message": "Quiz already submitted", "attemptMeta": {
                "startTime": attempt.start_time.isoformat() if attempt.start_time else None,
                "durationSeconds": attempt.duration_seconds,
                "completedAt": attempt.completed_at.isoformat() if attempt.completed_at else None,
                "violationCount": attempt.violation_count,
                "locked": bool(attempt.locked),
            }}, status=409)
        if not attempt or not attempt.start_time:
            attempt = attempt or DiagnosticQuizAttempt.objects.create(user=request.user, quiz=quiz)
            attempt.start_time = now
            attempt.duration_seconds = attempt.duration_seconds or 900
            attempt.violation_count = 0
            attempt.status = "active"
            attempt.save(update_fields=["start_time", "duration_seconds", "violation_count", "status"])
        return Response({
            "attemptMeta": {
                "attemptId": attempt.id,
                "startTime": attempt.start_time.isoformat(),
                "durationSeconds": attempt.duration_seconds,
                "locked": bool(attempt.locked),
                "violationCount": attempt.violation_count,
            }
        })
