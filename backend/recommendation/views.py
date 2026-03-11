from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import recommend_next


class RecommendNextView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not (getattr(request.user, "has_taken_quiz", False) or getattr(request.user, "diagnostic_completed", False)):
            return Response(
                {"message": "Complete the placement quiz to unlock personalized recommendations."},
                status=403,
            )
        return Response(recommend_next(request.user))
