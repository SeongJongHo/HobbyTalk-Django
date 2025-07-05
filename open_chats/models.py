from django.db import models

from categories.models import Category
from common.models import BaseCacheModel, BaseModel
from users.models import User

class OpenChatRoom(BaseModel):
    title = models.CharField(max_length=255)
    notice = models.CharField(max_length=255, blank=True, null=True)
    manager = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, db_constraint=False)
    maximum_capacity = models.IntegerField(default=2)
    current_attendance = models.IntegerField(default=1)
    password = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = (('manager', 'title'),)
        indexes = [
            models.Index(fields=['category']),
        ]
        db_table = 'open_chat_rooms'

    def __str__(self):
        return f"{self.title} ({self.manager.username})"
    
class OpenChatRoomUser(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False)
    open_chat_room = models.ForeignKey(OpenChatRoom, on_delete=models.DO_NOTHING, db_constraint=False)
    last_exit_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('user', 'open_chat_room'),)
        db_table = 'open_chat_room_users'

    def __str__(self):
        return f"{self.user.username} in {self.open_chat_room.title}"
    
class chatRoomMembershipRequestStatus:
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3

    _labels = {
        PENDING: 'Pending',
        ACCEPTED: 'Accepted',
        REJECTED: 'Rejected'
    }

    @classmethod
    def choices(cls):
        return [(value, cls._labels[value]) for value in cls._labels.keys()]
    
    @classmethod
    def label(cls, value):
        return cls._labels.get(value, 'Unknown')
    
class OpenChatRoomMembershipRequest(BaseModel):
    requester = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False)
    open_chat_room = models.ForeignKey(OpenChatRoom, on_delete=models.DO_NOTHING, db_constraint=False)
    message = models.CharField(max_length=255)
    status = models.IntegerField(choices=chatRoomMembershipRequestStatus.choices(), default=chatRoomMembershipRequestStatus.PENDING)

    class Meta:
        unique_together = (('requester', 'open_chat_room'),)
        db_table = 'open_chat_room_membership_requests'

    def __str__(self):
        return f"{self.requester.username} requests to join {self.open_chat_room.title}: {self.message[:20]}..."

class ChatMessageType:
    TEXT = 1
    IMAGE = 2
    VIDEO = 3
    FILE = 4

    _labels = {
        TEXT: 'Text',
        IMAGE: 'Image',
        VIDEO: 'Video',
        FILE: 'File'
    }

    @classmethod
    def choices(cls):
        return [(value, cls._labels[value]) for value in cls._labels.keys()]
    
    @classmethod
    def label(cls, value):
        return cls._labels.get(value, 'Unknown')

class OpenChat(BaseModel):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False)
    open_chat_room = models.ForeignKey(OpenChatRoom, on_delete=models.DO_NOTHING, db_constraint=False)
    message = models.TextField()
    message_type = models.IntegerField(choices=ChatMessageType.choices(), default=ChatMessageType.TEXT)

    class Meta:
        db_table = 'open_chats'

    def __str__(self):
        return f"{self.sender.username} in {self.open_chat_room.title}: {self.message[:20]}..."

class OpenChatCache(BaseCacheModel):
    sender_id: int
    open_chat_room_id: int
    message: str
    message_type: int

    def __init__(self, sender_id: int, open_chat_room_id: int, message: str, message_type: int, id=None, created_at=None, updated_at=None, deleted_at=None):
        super().__init__(id=id, created_at=created_at, updated_at=updated_at, deleted_at=deleted_at)
        self.sender_id = sender_id
        self.open_chat_room_id = open_chat_room_id
        self.message = message
        self.message_type = message_type
