from django.contrib import admin
from .models import Candidate, InterviewHistory


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "created_on")
    search_fields = ("user__first_name", "user__last_name", "user__email")
    list_filter = ("created_on",)


@admin.register(InterviewHistory)
class InterviewHistoryAdmin(admin.ModelAdmin):
    list_display = ("candidate", "company_name", "interview_date")
    search_fields = ("candidate__user__first_name", "candidate__user__last_name", "company_name")
    list_filter = ("interview_date",)
