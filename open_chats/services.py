from django.db import transaction

from categories.services import CategoryService, get_category_service
from common.decorator import retryable
from common.exceptions import LockAcquireException, NotFoundException, TooManyCreateException
from common.repositories import LockRepository, get_lock_repository
from common.security import PasswordEncoder
from open_chats.dtos import CreateOpenChatRoomDto
from open_chats.models import OpenChatRoomUser
from open_chats.repositories import OpenChatRoomRepository, OpenChatRoomUserRepository, get_open_chat_room_repository, get_open_chat_room_user_repository

class OpenChatRoomService:
    MAX_CREATE_COUNT = 5

    def __init__(
            self, 
            open_chat_room_repository: OpenChatRoomRepository, 
            open_chat_room_user_repository: OpenChatRoomUserRepository,
            category_service: CategoryService,
            lock_repository: LockRepository
        ):
        self.open_chat_room_repository = open_chat_room_repository
        self.open_chat_room_user_repository = open_chat_room_user_repository
        self.category_service = category_service
        self.lock_repository = lock_repository
        self.lock_key_prefix = "open_chat_room_lock:"

    @transaction.atomic
    def create(self, user_id: int, dto: CreateOpenChatRoomDto) -> int:
        if not self.category_service.get_category(dto.category_id):
            raise NotFoundException(f"존재하지 않는 카테고리입니다. category_id: {dto.category_id}")
        
        open_chat_room = dto.to_model(
            user_id, 
            hashed_password=PasswordEncoder.encode(dto.password) if dto.password else None,
        )
        
        if(self.lock_repository.acquire_lock(self.generate_lock_key(user_id), str(open_chat_room.id), ex=1)):
            try:
                user_rooms = self.open_chat_room_user_repository.find_by_user_id(user_id)
                if len(user_rooms) >= self.MAX_CREATE_COUNT:
                    raise TooManyCreateException("채팅방 생성 횟수는 5개로 제한되어 있습니다.")
                
                self.open_chat_room_repository.save(open_chat_room)
                self.open_chat_room_user_repository.save(OpenChatRoomUser(user_id=user_id, open_chat_room=open_chat_room))
            finally:
                self.lock_repository.release_lock(self.generate_lock_key(user_id), str(open_chat_room.id))
        else: raise LockAcquireException(f"채팅방 생성 중 다른 작업이 진행 중입니다. user_id: {user_id}, room_id: {open_chat_room.id}")
        
        return open_chat_room.id

    def generate_lock_key(self, user_id: int, key: str = None) -> str:
        if key is None:
            return f"{self.lock_key_prefix}{user_id}"
        return f"{self.lock_key_prefix}{key}:{user_id}"
        
def get_open_chat_room_service_factory() -> OpenChatRoomService:
    _instance = None
    def get_instance() -> OpenChatRoomService:
        nonlocal _instance
        if _instance is None:
            _instance = OpenChatRoomService(
                open_chat_room_repository=get_open_chat_room_repository(),
                open_chat_room_user_repository=get_open_chat_room_user_repository(),
                category_service=get_category_service(),
                lock_repository=get_lock_repository()
            )
        return _instance
    return get_instance

get_open_chat_room_service = get_open_chat_room_service_factory()