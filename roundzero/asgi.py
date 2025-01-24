"""
ASGI configuration for the RoundZero project.

This file sets up the ASGI application for the project, configuring both
HTTP and WebSocket protocols. It includes the middleware and routing for
handling WebSocket connections, and uses Channels for handling asynchronous
communication.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roundzero.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chatbot.routing import websocket_urlpatterns


django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)
