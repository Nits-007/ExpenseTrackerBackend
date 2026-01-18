from django.urls import path
from .views import MonthlyAnalyticsView

urlpatterns = [
    path('monthly/', MonthlyAnalyticsView.as_view()),
]
