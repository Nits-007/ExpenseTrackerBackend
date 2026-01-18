from django.urls import path
from .views import TriggerAIInsightView, FetchAIInsightView, AIResultView

urlpatterns = [
    path('generate/', TriggerAIInsightView.as_view()),
    path('result/', FetchAIInsightView.as_view()),
    path('result/<str:task_id>/', AIResultView.as_view(), name='ai-result'),
]
