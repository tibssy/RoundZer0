"""
URL configuration for the chatbot application.

This module defines the URL patterns for the chatbot views, including the
index page, the interview page, and the interview conclusion page. Each URL
pattern is mapped to a corresponding class-based view.

URLs:
- 'index/': Renders the chatbot welcome page.
- 'interview/': Renders the chatbot interview page.
- 'interview/end/': Renders the chatbot interview end page.
"""

from django.urls import path
from .views import (
    ChatbotIndexView,
    ChatbotInterviewView,
    ChatbotInterviewEndView
)


urlpatterns = [
    # pattern for the chatbot index page, welcoming the user to the interview
    path(
        'index/', ChatbotIndexView.as_view(), name='chatbot-index'
    ),

    # pattern for the chatbot interview page, where the interview takes place
    path(
        'interview/', ChatbotInterviewView.as_view(), name='chatbot-interview'
    ),

    # pattern for the end of the interview, showing the conclusion page
    path(
        'interview/end/', ChatbotInterviewEndView.as_view(),
        name='chatbot-interview-end'
    ),
]
