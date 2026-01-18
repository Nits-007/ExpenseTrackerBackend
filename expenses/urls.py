from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, CategoryViewSet, BudgetViewSet

router = DefaultRouter()
router.register('expenses', ExpenseViewSet, basename='expenses')
router.register('categories', CategoryViewSet)
router.register('budgets', BudgetViewSet)

urlpatterns = router.urls
