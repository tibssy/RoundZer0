"""
This module defines the URL patterns for the 'about' app.

It maps the root URL ('') to the 'about' view function,
providing access to the about page.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Maps the root URL to the about view.
    path('', views.about, name='about'),
]