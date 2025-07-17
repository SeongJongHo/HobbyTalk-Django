from django.urls import re_path
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

from auth.middleware import WebSocketAuthMiddleware

websocket_urlpatterns = [
]

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": WebSocketAuthMiddleware(
        URLRouter(websocket_urlpatterns)
    )
})