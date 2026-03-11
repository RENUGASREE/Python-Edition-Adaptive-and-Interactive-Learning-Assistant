from django.urls import path
from .views import SystemEvaluationView, SystemEvaluationSummaryView

urlpatterns = [
    path("system-evaluation/", SystemEvaluationView.as_view(), name="system_evaluation"),
    path("system-evaluation/summary/", SystemEvaluationSummaryView.as_view(), name="system_evaluation_summary"),
]
