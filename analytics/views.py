from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .services import monthly_summary
from datetime import date

class MonthlyAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = date.today()
        data = monthly_summary(request.user, today.month, today.year)
        return Response(data)
    

