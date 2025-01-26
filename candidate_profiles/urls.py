"""
URL configuration for the candidate profiles app.

Defines URL patterns for candidate profile views and actions,
including editing profiles, viewing history, and managing interviews.
"""

from django.urls import path
from . import views

urlpatterns = [
    # View candidate profile
    path(
        'profile/',
        views.candidate_profile,
        name='candidate_profile'
    ),
    # Edit candidate profile
    path(
        'profile/edit/',
        views.edit_candidate_profile,
        name='edit_candidate_profile'
    ),
    # View candidate interview history
    path(
        'profile/history/',
        views.candidate_history,
        name='candidate_history'
    ),
    # Delete candidate profile
    path(
        'delete_profile/',
        views.delete_candidate_profile,
        name='delete_candidate_profile'
    ),
    # Delete an interview record
    path(
        'interview/delete/<int:interview_id>/',
        views.delete_interview,
        name='delete_interview'
    ),
]
