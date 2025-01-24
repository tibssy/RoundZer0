"""
URL configuration for the project.

This file includes the URL patterns for various apps such as the admin panel,
summernote editor, job posts, chatbot, authentication, home page, about page,
candidate profiles, and employer profiles.
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # Admin panel URL
    path(
        'admin/',
        admin.site.urls
    ),
    # Summernote editor URL
    path(
        'summernote/',
        include('django_summernote.urls')
    ),
    # Job posts URLs
    path(
        'jobs/',
        include('jobposts.urls'),
        name='jobposts-urls'
    ),
    # Chatbot URLs
    path(
        'chatbot/',
        include('chatbot.urls'),
        name='chatbot-urls'
    ),
    # User authentication URLs
    path(
        'accounts/',
        include('allauth.urls')
    ),
    # Home page URL
    path(
        '',
        include('home.urls'),
        name='home-urls'
    ),
    # About page URL
    path(
        'about/',
        include('about.urls'),
        name='about-urls'
    ),
    # Candidate profile URLs
    path(
        'candidate/',
        include('candidate_profiles.urls'),
        name='candidate-urls'
    ),
    # Employer profile URLs
    path(
        'employer/',
        include('employer_profiles.urls'),
        name='employer-urls'
    ),
]
