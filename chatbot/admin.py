from django.contrib import admin
from .models import EvaluationRubric, InterviewPreparation

@admin.register(EvaluationRubric)
class EvaluationRubricAdmin(admin.ModelAdmin):
    list_display = ('criterion', 'job_post', 'weight', 'created_on')
    list_filter = ('job_post',)
    search_fields = ('criterion', 'scoring_guide')


@admin.register(InterviewPreparation)
class InterviewPreparationAdmin(admin.ModelAdmin):
    list_display = ('job_post', 'interview_duration', 'created_on')
    list_filter = ('job_post',)
    search_fields = ('job_post__title',)
    fieldsets = (
        (None, {
            'fields': ('job_post', 'interview_duration', 'questions')
        }),
    )
    readonly_fields = ('created_on',)