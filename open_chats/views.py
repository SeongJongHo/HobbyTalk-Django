from django.views import View

from common.decorator import guarded_by_role, validate_body
from common.response import ResponseGenerator, ResponseMsg
from open_chats.dtos import CreateOpenChatRoomDto
from open_chats.services import OpenChatRoomService, get_open_chat_room_service
from users.models import UserRole

class OpenChatRoomViewV1(View):
    def __init__(self, open_chat_room_service: OpenChatRoomService = get_open_chat_room_service()):
        self.open_chat_room_service = open_chat_room_service

    @guarded_by_role(UserRole.USER)
    @validate_body(CreateOpenChatRoomDto)
    def post(self, request):
        user_id = request.user.get('user_id', None)

        return ResponseGenerator.build(
            message=ResponseMsg.CREATED,
            data={ 'open_chat_room_id': self.open_chat_room_service.create(user_id, request.validated) },
            status=201
        )