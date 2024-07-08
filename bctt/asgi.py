"""
ASGI config for bctt project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from transaction import routing
from channels.auth import AuthMiddlewareStack

django_asgi_app = get_asgi_application()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bctt.settings')

application = ProtocolTypeRouter({
    "http" : django_asgi_app,
    "websocket" : AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns
        )
    )
})

