from rest_framework import viewsets, permissions, status
from .models import Expense, Category, Budget
from .serializers import ExpenseSerializer, CategorySerializer, BudgetSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_class = [permissions.IsAuthenticated]

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class =BudgetSerializer
    permission_class = [permissions.IsAuthenticated]
    
    def get_query(self):
        return Budget.objects.filter(user = self.request.user)
    
    def create(self, request, *args, **kwargs):
        category_id = request.data.get('category')
        limit = request.data.get('monthly_limit') 
        # This logic updates if exists, creates if not (Upsert)
        obj, created = Budget.objects.update_or_create(
            user=request.user,
            category_id=category_id,
            defaults={'monthly_limit': limit}
        )
        serializer = self.get_serializer(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)