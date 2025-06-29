import datetime
from django.db.models import Prefetch, Max, Q, F
from django.db.models.functions import Coalesce
from django.db.models import DateTimeField
from open_chats.models import OpenChat, OpenChatRoom, OpenChatRoomUser

class OpenChatRoomRepository:
    def find_by_id(self, room_id: int):
        return OpenChatRoom.objects.filter(id=room_id, deleted_at=None).first()
    
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
class ReadOpenChatRoomRepository:

    def find_by_user_id(self, user_id: int, last_created_at: str, limit: int):
        no_offset = 0
        qs = OpenChatRoom.objects.raw("""
            SELECT 
                ocr.*,
                oc.message AS last_chat,
                COALESCE(oc.created_at, ocr.created_at) AS last_activity
            FROM open_chat_rooms ocr
            INNER JOIN open_chat_room_users ocru 
                ON ocru.open_chat_room_id = ocr.id 
                AND ocru.user_id = %s 
                AND ocru.deleted_at IS NULL
            LEFT JOIN open_chats oc 
                ON oc.id = (
                    SELECT id 
                    FROM open_chats 
                    WHERE open_chat_room_id = ocr.id
                    AND deleted_at IS NULL
                    ORDER BY created_at DESC 
                    LIMIT 1
                )
            WHERE
                ocr.created_at < %s 
                AND ocr.deleted_at IS NULL
            ORDER BY last_activity DESC
            LIMIT %s OFFSET %s
        """, [user_id, last_created_at, limit, no_offset])

        qs = qs.prefetch_related(
            Prefetch(
                'openchatroomuser_set',
                queryset=OpenChatRoomUser.objects
                    .filter(deleted_at=None)
                    .select_related('user')
                    .order_by('-created_at')[:5],
                to_attr='recent_members'
            ),
        )

        return list(qs)
    
    def find_by_category_id(self, category_id: int, user_id: int, last_created_at: str, limit: int):
        no_offset = 0
        qs = OpenChatRoom.objects
        if category_id: qs = qs.filter(category_id=category_id, deleted_at=None)
        else: qs = OpenChatRoom.objects.filter(deleted_at=None)
        
        qs = qs.annotate(
            is_joined=Max(
                'openchatroomuser__user_id',
                filter=Q(openchatroomuser__user_id=user_id, openchatroomuser__deleted_at=None)
            )
        )
        qs = qs.select_related('category')
        qs = qs.filter(created_at__lt=last_created_at, is_joined__isnull=True).order_by('-created_at')[no_offset:limit]
        
        return list(qs)

def get_read_open_chat_room_repository_factory() -> ReadOpenChatRoomRepository:
    _instance = None
    def get_instance() -> ReadOpenChatRoomRepository:
        nonlocal _instance
        if _instance is None:
            _instance = ReadOpenChatRoomRepository()
        return _instance
    return get_instance

get_read_open_chat_room_repository = get_read_open_chat_room_repository_factory()

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