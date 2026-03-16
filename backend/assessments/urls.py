from django.urls import path
from .views import DiagnosticQuizView, DiagnosticSubmitView, DiagnosticStartView, DiagnosticCancelView


urlpatterns = [
    path("diagnostic/", DiagnosticQuizView.as_view(), name="diagnostic_quiz"),
    path("diagnostic/submit/", DiagnosticSubmitView.as_view(), name="diagnostic_submit_v2"),
    path("diagnostic/start/", DiagnosticStartView.as_view(), name="diagnostic_start"),
    path("diagnostic/cancel/", DiagnosticCancelView.as_view(), name="diagnostic_cancel"),
]
