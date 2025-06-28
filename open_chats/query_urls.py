from django.urls import path
from open_chats.views import ReadCategoryOpenChatRoomViewV1, ReadMyOpenChatRoomViewV1

urlpatterns = [
    path('/my', ReadMyOpenChatRoomViewV1.as_view(), name='chat-room-list'),
    path('', ReadCategoryOpenChatRoomViewV1.as_view(), name='category-chat-room-list'),
]