from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from auth.middleware import WebSocketAuthMiddleware
from open_chats.comsumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'^ws/open-chat-rooms/(?P<room_id>\d+)/join/?$', ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebSocketAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    )
})