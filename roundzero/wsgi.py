"""
WSGI configuration for the RoundZero project.

This file contains the WSGI application configuration to deploy the Django
application using a WSGI server.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roundzero.settings')
application = get_wsgi_application()
