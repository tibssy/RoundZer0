from django.contrib import admin
from .models import Employer

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'phone', 'created_on']
    search_fields = ['company_name', 'user__username', 'user__email']
    list_filter = ("created_on",)
