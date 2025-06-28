from django.urls import path

from open_chats.views import OpenChatRoomViewV1

urlpatterns = [
    path('', OpenChatRoomViewV1.as_view(), name='chat-room-create'),
]