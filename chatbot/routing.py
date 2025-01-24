"""
WebSocket routing for the chatbot application.

This module defines the WebSocket URL patterns for the chatbot, mapping
the WebSocket connection to the corresponding consumer. In this case,
the 'ws/voice/' endpoint is mapped to the VoiceConsumer, which handles
the WebSocket connection for voice-related interactions.
"""

from django.urls import path
from .consumers import VoiceConsumer


websocket_urlpatterns = [
    # WebSocket URL pattern for voice communication
    path('ws/voice/', VoiceConsumer.as_asgi()),
]
