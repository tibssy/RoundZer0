"""
This module defines the URL patterns for the 'jobposts' app.

It maps URLs to their corresponding view functions, handling
requests for job listings, individual job details, and initiating
interviews.
"""

from . import views
from django.urls import path


urlpatterns = [
    # URL pattern for the job list view.
    path(
        '',
        views.JobList.as_view(),
        name='jobs'
    ),
    # URL pattern for the job detail view.
    path(
        'job/<int:pk>/',
        views.JobDetailView.as_view(),
        name='job_detail'
    ),
    # URL pattern for initiating an interview.
    path(
        'job/<int:job_post_id>/start_interview/',
        views.redirect_to_chatbot_index,
        name='start_interview'
    ),
]
