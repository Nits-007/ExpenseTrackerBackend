from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from analytics.services import monthly_summary
from .tasks import generate_monthly_insight
from .services import generate_financial_insights
from expenses.models import AIInsight
from datetime import date



class TriggerAIInsightView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        today = date.today()
        task = generate_monthly_insight.delay(request.user.id)
        AIInsight.objects.update_or_create(
            user=request.user,
            month=today.month,
            year=today.year,
            defaults={
                'celery_task_id': task.id,
                'content': ""  # Empty content means "still working"
            }
        )
        return Response({
            "task_id": task.id,
            "status": "processing"
        })
    
class FetchAIInsightView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        today = date.today()
        insight = AIInsight.objects.filter(
            user=request.user,
            month=today.month,
            year=today.year
        ).first()

        if not insight:
            return Response({"status": "not_ready"})
        
        return Response({
            "status": "ready",
            "insight": insight.content
        })
    
class AIResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            # Assuming task_id is actually AIInsight id
            insight = AIInsight.objects.get(celery_task_id=task_id, user=request.user)

            if not insight.content:
                return Response({
                    "status": "processing",
                    "insight": None
                })

            return Response({
                "status": "ready",
                "insight": insight.content
            })
        except AIInsight.DoesNotExist:
            return Response({
                "status": "pending",
                "insight": None
            }, status=404)
        except Exception as e:
            # Catch other errors (like ValueErrors if the ID format is weird)
            return Response({"error": str(e)}, status=400)




