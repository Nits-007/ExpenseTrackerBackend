from django.contrib import admin
from expenses.models import Category, Expense, Budget, AIInsight


# Register your models here.
admin.site.register(Category)
admin.site.register(Expense)
admin.site.register(Budget)
admin.site.register(AIInsight)