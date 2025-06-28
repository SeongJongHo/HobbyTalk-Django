from open_chats.models import OpenChatRoom, OpenChatRoomUser

class OpenChatRoomRepository:
    def find_by_id(self, room_id: int):
        return OpenChatRoom.objects.filter(id=room_id, deleted_at=None).first()
    
    def find_by_user_id(self, user_id: int):
        return list(OpenChatRoom.objects.filter(user_id=user_id, deleted_at=None).all())
    
    def save(self, open_chat_room: OpenChatRoom):
        return open_chat_room.save()

def get_open_chat_room_repository_factory() -> OpenChatRoomRepository:
    _instance = None
    def get_instance() -> OpenChatRoomRepository:
        nonlocal _instance
        if _instance is None:
            _instance = OpenChatRoomRepository()
        return _instance
    return get_instance

get_open_chat_room_repository = get_open_chat_room_repository_factory()

class OpenChatRoomUserRepository:
    def find_by_room_id_and_user_id(self, room_id: int, user_id: int):
        return OpenChatRoomUser.objects.filter(id=room_id, user_id=user_id, deleted_at=None).first()
    
    def find_by_user_id(self, user_id: int):
        return list(OpenChatRoomUser.objects.filter(user_id=user_id, deleted_at=None).all())
    
    def save(self, open_chat_room_user: OpenChatRoomUser):
        return open_chat_room_user.save()
    
def get_open_chat_room_user_repository_factory() -> OpenChatRoomUserRepository:
    _instance = None
    def get_instance() -> OpenChatRoomUserRepository:
        nonlocal _instance
        if _instance is None:
            _instance = OpenChatRoomUserRepository()
        return _instance
    return get_instance

get_open_chat_room_user_repository = get_open_chat_room_user_repository_factory()