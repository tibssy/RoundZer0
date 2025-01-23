"""
Django admin configuration for the chatbot app's models.

This module configures the admin interface for the `EvaluationRubric` and
`InterviewPreparation` models, allowing for an easy-to-use interface to manage
evaluation criteria, scoring, and interview preparations. It includes custom
display settings, filters, and search fields for each model.

Classes:
    EvaluationRubricAdmin: Admin interface configuration for the
    EvaluationRubric model. InterviewPreparationAdmin: Admin interface
    configuration for the InterviewPreparation model.
"""

from django.contrib import admin
from .models import EvaluationRubric, InterviewPreparation

@admin.register(EvaluationRubric)
class EvaluationRubricAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the EvaluationRubric model.

    Customizes the display of the `EvaluationRubric` model in the Django admin
    interface, including fields for searching, filtering, and displaying
    relevant data such as job posts and scoring guides.
    """

    list_display = ('criterion', 'job_post', 'weight', 'created_on')
    list_filter = ('job_post',)
    search_fields = ('criterion', 'scoring_guide')


@admin.register(InterviewPreparation)
class InterviewPreparationAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the InterviewPreparation model.

    Customizes the display of the `InterviewPreparation` model in the Django
    admin interface, focusing on fields related to interview duration,
    job posts, and interview questions.
    """

    list_display = ('job_post', 'interview_duration', 'created_on')
    list_filter = ('job_post',)
    search_fields = ('job_post__title',)
    fieldsets = (
        (None, {
            'fields': ('job_post', 'interview_duration', 'questions')
        }),
    )
    readonly_fields = ('created_on',)
