"""
ASGI config for a_core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'a_core.settings')

# Handles regular HTTP requests
django_asgi_app = get_asgi_application()
from a_rtchat import routing

# Main ASGI application
application = ProtocolTypeRouter({
    "http": django_asgi_app ,  # HTTP goes to regular Django views
    "websocket": AllowedHostsOriginValidator(  # Validates host headers for security
        AuthMiddlewareStack(  # Adds Django auth support to WebSocket
            URLRouter(
                routing.websocket_urlpatterns  # Routes WebSocket paths
            )
        )
    ),
})
