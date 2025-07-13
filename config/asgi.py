"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

django_asgi_app = get_asgi_application()

from auth.middleware import WebSocketAuthMiddleware
from open_chats.comsumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/open-chat-rooms/(?P<room_id>\d+)/join/?$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": WebSocketAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    ),
})