from django.contrib import admin
from .models import JobPost
from django_summernote.admin import SummernoteModelAdmin


@admin.register(JobPost)
class PostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'company_name', 'location')
    search_fields = ['title']
    list_filter = ('location',)
    prepopulated_fields = {'company_name': ('title',)}
    summernote_fields = ('description',)


# Register your models here.
# admin.site.register(JobPost)