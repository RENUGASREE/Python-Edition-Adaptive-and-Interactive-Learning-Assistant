from django.urls import path
from .views import UserMetricsView


urlpatterns = [
    path("metrics/", UserMetricsView.as_view(), name="user_metrics"),
]
