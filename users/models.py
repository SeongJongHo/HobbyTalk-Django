from django.db import models

from common.models import BaseModel

class UserRole:
    UNKNOWN = 'UNKNOWN'
    ADMIN = 'ADMIN'
    USER = 'USER'

    _labels = {
            UNKNOWN: 'Unknown',
            ADMIN: 'Admin',
            USER: 'User',
        }
    
    _role_levels = {
        UNKNOWN: 0,
        USER: 1,
        ADMIN: 2,
    }

    @classmethod
    def has_permission(cls, user_role: str, required_role: str) -> bool:
        return cls._role_levels.get(user_role, -1) >= cls._role_levels.get(required_role, -1)

    @classmethod
    def choices(cls):
        return [(role, cls._labels[role]) for role in cls._role_levels.keys()]
    
class User(BaseModel):
    nickname = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=UserRole.choices(),
        default=UserRole.USER,)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=50, unique=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
    
class FreindStatus():
    FRIEND = 0
    BLOCK = 1

    _labels = {
        FRIEND: 'Friend',
        BLOCK: 'Blocked',
    }

    @classmethod
    def choices(cls):
        return [(value, cls._labels[value]) for value in cls._labels.keys()]
    
    @classmethod
    def label(cls, value):
        return cls._labels.get(value, 'Unknown')

class Friend(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name='friends')
    friend = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name='friend_of')
    status = models.IntegerField(choices=FreindStatus.choices(), default=FreindStatus.FRIEND)

    class Meta:
        unique_together = (('user', 'friend'),)
        db_table = 'friends'

    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"
    
class RequestStatus():
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    CANCELLED = 3

    _labels = {
        PENDING: 'Pending',
        ACCEPTED: 'Accepted',
        REJECTED: 'Rejected',
        CANCELLED: 'Cancelled',
    }

    @classmethod
    def choices(cls):
        return [(value, cls._labels[value]) for value in cls._labels.keys()]
    
    @classmethod
    def label(cls, value):
        return cls._labels.get(value, 'Unknown')

class FriendshipRequest(BaseModel):
    to_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name='received_requests')
    from_user = models.ForeignKey(User, on_delete=models.DO_NOTHING, db_constraint=False, related_name='sent_requests')
    status = models.IntegerField(choices=RequestStatus.choices(), default=RequestStatus.PENDING)
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)
        db_table = 'friendship_requests'

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username} ({self.get_status_display()})"
    
class NotificationSetting(BaseModel):
    user = models.OneToOneField(User, unique=True, on_delete=models.DO_NOTHING, db_constraint=False)
    chat = models.BooleanField(default=True)
    friendship = models.BooleanField(default=True)
    chat_room_membership_request = models.BooleanField(default=True)

    class Meta:
        db_table = 'notification_settings'

    def __str__(self):
        return f"Notification settings for {self.user.username}"