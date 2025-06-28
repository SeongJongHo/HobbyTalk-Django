from django.urls import path

from open_chats.views import OpenChatRoomViewV1, ReadOpenChatRoomViewV1

urlpatterns = [
    path('/my', ReadOpenChatRoomViewV1.as_view(), name='chat-room-list'),
    path('', OpenChatRoomViewV1.as_view(), name='chat-room-create'),
]