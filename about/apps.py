"""
Configuration module for the 'about' app.

This module defines the AboutConfig class, which provides
configuration settings for the 'about' app, including the
default auto field and the app's name.
"""

from django.apps import AppConfig


class AboutConfig(AppConfig):
    """
    Configuration class for the 'about' app.

    :ivar default_auto_field: The default auto-generated primary key field type.
    :vartype default_auto_field: str
    :ivar name: The name of the app.
    :vartype name: str
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "about"
