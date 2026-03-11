import csv
import logging
from io import StringIO
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import system_evaluation_metrics, export_system_metrics, system_evaluation_summary

logger = logging.getLogger("evaluation.views")


class SystemEvaluationView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            output_format = request.query_params.get("format")
            if output_format == "csv":
                rows = export_system_metrics()
                buffer = StringIO()
                writer = csv.writer(buffer)
                for row in rows:
                    writer.writerow(row)
                return Response(buffer.getvalue(), content_type="text/csv")
            return Response(system_evaluation_metrics())
        except Exception:
            logger.exception("system_evaluation_view_failed", extra={"user_id": request.user.id})
            return Response(system_evaluation_metrics())


class SystemEvaluationSummaryView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            return Response(system_evaluation_summary())
        except Exception:
            logger.exception("system_evaluation_summary_failed", extra={"user_id": request.user.id})
            return Response({
                "summary_text": "Evaluation summary unavailable due to insufficient data.",
                "better_group": {"learning_gain": None, "mastery_slope": None, "engagement_growth": None, "overall": None},
                "practical_significance": {"learning_gain": None, "mastery_slope": None},
                "p_values": {
                    "learning_gain": {"value": None, "insufficient_data": True},
                    "mastery_slope": {"value": None, "insufficient_data": True},
                    "engagement_growth": {"value": None, "insufficient_data": True},
                },
                "effect_sizes": {
                    "learning_gain": {"cohen_d": None, "insufficient_data": True},
                    "mastery_slope": {"cohen_d": None, "insufficient_data": True},
                },
                "confidence_intervals": {
                    "mean_learning_gain": {"interval": None, "insufficient_data": True},
                    "mean_time_to_mastery": {"interval": None, "insufficient_data": True},
                },
                "ab_group_comparison": {},
                "data_snapshot": {
                    "total_users": 0,
                    "total_recommendations": 0,
                    "total_difficulty_shifts": 0,
                    "evaluation_time_range": {"start": None, "end": None},
                },
            })
