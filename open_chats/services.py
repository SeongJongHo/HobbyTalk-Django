from django.db import transaction

from categories.services import CategoryService
from common.decorator import retryable
from common.exceptions import LockAcquireException, NotFoundException, RetryException, TooManyCreateException
from common.repositories import LockRepository, get_lock_repository
from common.security import PasswordEncoder
from open_chats.dtos import CreateOpenChatRoomDto
from open_chats.models import OpenChatRoomUser
from open_chats.repositories import OpenChatRoomRepository, OpenChatRoomUserRepository

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

    @retryable(max_retries=3)
    @transaction.atomic
    def create(self, user_id: int, dto: CreateOpenChatRoomDto) -> int:
        if not self.category_service.get_category(dto.category_id):
            raise NotFoundException(f"존재하지 않는 카테고리입니다. category_id: {dto.category_id}")
        
        open_chat_room = dto.to_model(
            user_id, 
            hashed_password=PasswordEncoder.encode(dto.password) if dto.password else None,
        )
        
        if(self.lock_repository.acquire_lock(self.generate_lock_key(user_id), str(open_chat_room.id), ex=3)):
            try:
                user_rooms = self.open_chat_room_user_repository.find_by_user_id(user_id)
                if len(user_rooms) >= self.MAX_CREATE_COUNT:
                    raise TooManyCreateException("채팅방 생성 횟수는 5개로 제한되어 있습니다.")
                
                self.open_chat_room_repository.save(open_chat_room)
                self.open_chat_room_user_repository.save(OpenChatRoomUser(user_id=user_id, open_chat_room=open_chat_room))
            finally:
                self.lock_repository.release_lock(self.generate_lock_key(user_id), str(open_chat_room.id))
        else: raise RetryException("채팅방 생성 중 잠금 획득 실패")
        
        return open_chat_room.id

    def generate_lock_key(self, user_id: int, key: str = None) -> str:
        if key is None:
            return f"{self.lock_key_prefix}{user_id}"
        return f"{self.lock_key_prefix}{key}:{user_id}"
        