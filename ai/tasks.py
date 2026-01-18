from celery import shared_task
from analytics.services import monthly_summary
from .services import generate_financial_insights
from expenses.models import AIInsight
from django.contrib.auth.models import User
from datetime import date

@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 3, 'countdown': 5})
def generate_monthly_insight(self, user_id):
    user = User.objects.get(id=user_id)
    today = date.today()
    summary = monthly_summary(user, today.month, today.year)
    insight_text = generate_financial_insights(summary)
    try:
        insight = AIInsight.objects.get(celery_task_id=self.request.id)
        insight.content = insight_text
        insight.save()
    except AIInsight.DoesNotExist:
        # Fallback in case the view failed to create it (rare)
        AIInsight.objects.create(
            user=user,
            month=today.month,
            year=today.year,
            content=insight_text,
            celery_task_id=self.request.id
        )
    return self.request.id