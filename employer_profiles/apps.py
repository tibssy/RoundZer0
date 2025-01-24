"""
Django application configuration for the employer_profiles app.

This module contains the configuration for the employer_profiles app,
which defines the default primary key field type and the app's name.
"""

from django.apps import AppConfig


class EmployerProfilesConfig(AppConfig):
    """
    Configuration for the employer_profiles Django app.

    This class sets the default primary key field type and the name of
    the application for Django's app registry.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "employer_profiles"
