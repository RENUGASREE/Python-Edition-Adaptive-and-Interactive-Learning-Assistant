from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import answer_with_rag


class AiTutorView(APIView):
    permission_classes = (IsAuthenticated,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "ai"

    def post(self, request):
        query = request.data.get("query")
        topic = request.data.get("topic")
        if not query:
            return Response({"message": "query is required"}, status=400)
        result = answer_with_rag(query, topic=topic)
        return Response(result)
