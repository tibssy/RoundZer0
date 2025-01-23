"""
Django application configuration for the chatbot module.

This module defines the configuration class for the 'chatbot' app, specifying
the default auto field type and the app's name. The app configuration is used
by Django to set up the application in the project.

Classes:
    ChatbotConfig: A configuration class for the chatbot app.
"""

from django.apps import AppConfig


class ChatbotConfig(AppConfig):
    """
    Configuration for the 'chatbot' app.

    This class specifies the default auto field and the name of the app,
    ensuring the chatbot app is properly configured in the Django project.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "chatbot"
