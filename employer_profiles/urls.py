"""
URL configuration for employer profiles.

This file contains URL patterns for the employer-related views such as viewing
and editing employer profiles, managing job posts, and handling job
applications.
"""

from django.urls import path
from . import views
from candidate_profiles import views as candidate_views
from jobposts import views as jobpost_views


urlpatterns = [
    # Employer profile page
    path(
        'profile/',
        views.employer_profile,
        name='employer_profile'
    ),
    # Edit employer profile
    path(
        'profile/edit/',
        views.edit_employer_profile,
        name='edit_employer_profile'
    ),
    # Delete employer profile
    path(
        'delete_profile/',
        views.delete_employer_profile,
        name='delete_employer_profile'
    ),
    # Employer job listings page
    path(
        'my_jobs/',
        views.my_jobs,
        name='employer_jobs'
    ),
    # Create a new job posting
    path(
        'my_jobs/create/',
        views.create_job,
        name='create_job'
    ),
    # View job details
    path(
        'my_jobs/view/<int:pk>/',
        jobpost_views.JobDetailView.as_view(),
        name='view_my_job'
    ),
    # Edit a specific job posting
    path(
        'my_jobs/edit/<int:job_id>/',
        views.edit_my_jobs,
        name='edit_my_jobs'
    ),
    # Delete a specific job posting
    path(
        'my_jobs/delete/<int:job_id>/',
        views.delete_my_job,
        name='delete_my_job'
    ),
    # View job applications
    path(
        'my_jobs/applications/<int:job_id>/',
        views.job_applications,
        name='job_applications'
    ),
    # View candidate profile
    path(
        'candidate/<int:candidate_id>/',
        candidate_views.candidate_profile_view,
        name='candidate_profile_view'
    ),
]
