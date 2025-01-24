"""
This module defines the Django admin configuration for the 'jobposts' app.

It registers the 'JobPost' model with the admin interface and customizes
its appearance and functionality using 'SummernoteModelAdmin'.
"""

from django.contrib import admin
from .models import JobPost
from django_summernote.admin import SummernoteModelAdmin


@admin.register(JobPost)
class PostAdmin(SummernoteModelAdmin):
    """
    Admin configuration for the 'JobPost' model.

    Inherits from 'SummernoteModelAdmin' to provide Summernote rich text
    editing capabilities for the 'description' field. Also customizes
    the list display, search fields, filters, and prepopulated fields.
    """

    list_display = ('title', 'company_name', 'location')
    search_fields = ['title']
    list_filter = ('location',)
    prepopulated_fields = {'company_name': ('title',)}
    summernote_fields = ('description',)
