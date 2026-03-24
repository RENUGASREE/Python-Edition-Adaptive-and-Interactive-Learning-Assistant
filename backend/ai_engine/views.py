from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
from rest_framework.views import APIView
from .services import answer_with_rag


class AiTutorView(APIView):
    permission_classes = ()
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = "ai"

    def post(self, request):
        message = request.data.get("message")
        topic = request.data.get("topic")
        if not message:
            return Response({"message": "message is required"}, status=400)
        result = answer_with_rag(message, topic=topic)
        return Response(result)
