from django.contrib import admin
from .models import EvaluationRubric

@admin.register(EvaluationRubric)
class EvaluationRubricAdmin(admin.ModelAdmin):
    list_display = ('criterion', 'job_post', 'weight', 'created_on')
    list_filter = ('job_post',)
    search_fields = ('criterion', 'scoring_guide')
