from django.contrib import admin
from .models import Employer, InterviewFeedback

@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'user', 'phone', 'created_on']
    search_fields = ['company_name', 'user__username', 'user__email']
    list_filter = ("created_on",)


@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(admin.ModelAdmin):
    list_display = ['job_post', 'candidate', 'created_on']
    list_filter = ['job_post', 'candidate', 'created_on']
    search_fields = [
        'job_post__title',
        'candidate__user__username',
        'candidate__user__first_name',
        'candidate__user__last_name',
    ]
    readonly_fields = ['created_on']