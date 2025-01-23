"""
Configuration module for the 'home' app.

This module defines the HomeConfig class, which provides
configuration settings for the 'home' app, including the
default auto field and the app's name.
"""

from django.apps import AppConfig


class HomeConfig(AppConfig):
    """
    Configuration class for the 'home' app.

    :ivar default_auto_field: The default auto-generated primary key field type.
    :vartype default_auto_field: str
    :ivar name: The name of the app.
    :vartype name: str
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "home"
