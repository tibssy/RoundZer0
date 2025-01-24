"""
Admin configuration for the Candidate and InterviewHistory models.

This module defines admin interfaces for the Candidate and InterviewHistory
models, customizing the fields displayed, searchable fields, and filters
available in the Django admin panel.
"""

from django.contrib import admin
from .models import Candidate, InterviewHistory


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    """
    Admin interface for managing Candidate objects.

    Attributes:
        list_display (tuple): Fields displayed in the admin list view.
        search_fields (tuple): Fields used for the search functionality
        in the admin.
        list_filter (tuple): Fields used for filtering in the admin list view.
    """

    list_display = (
        'user',
        'phone',
        'created_on'
    )
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email'
    )
    list_filter = (
        'created_on',
    )


@admin.register(InterviewHistory)
class InterviewHistoryAdmin(admin.ModelAdmin):
    """
    Admin interface for managing InterviewHistory objects.

    Attributes:
        list_display (tuple): Fields displayed in the admin list view.
        search_fields (tuple): Fields used for the search functionality
        in the admin.
        list_filter (tuple): Fields used for filtering in the admin list view.
    """

    list_display = (
        'candidate',
        'company_name',
        'interview_date'
    )
    search_fields = (
        'candidate__user__first_name',
        'candidate__user__last_name',
        'company_name'
    )
    list_filter = (
        'interview_date',
    )
