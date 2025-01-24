"""
App configuration for the Candidate Profiles application.

This module defines the configuration for the Candidate Profiles app,
specifying its name and default settings.
"""

from django.apps import AppConfig


class CandidateProfilesConfig(AppConfig):
    """
    Configuration class for the Candidate Profiles app.

    Attributes:
        default_auto_field (str): The type of auto-generated field for
        primary keys.
        name (str): The name of the application.
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'candidate_profiles'
