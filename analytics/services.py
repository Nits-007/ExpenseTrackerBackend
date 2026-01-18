from expenses.models import Expense
from django.db.models import Sum

def monthly_summary(user, month, year):
    expenses = Expense.objects.filter(user = user, created_at__month = month, created_at__year = year)
    total = expenses.aggregate(total = Sum('amount'))['total'] or 0
    by_category = expenses.values('category__name').annotate(total = Sum('amount'))

    return {
        'total_spent' : total,
        'category_breakdown' : by_category
    }
