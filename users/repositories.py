from typing import Callable
from users.models import NotificationSetting, User

class UserRepository:
    def find_by_id(self, user_id: int) -> User | None:

        return User.objects.filter(id=user_id, deleted_at=None).first()
    
    def find_by_username(self, username: str) -> User | None:

        return User.objects.filter(username=username, deleted_at=None).first()
    
    def find_by_phone_number(self, phone_number: str) -> User | None:

        return User.objects.filter(phone_number=phone_number, deleted_at=None).first()
    
    def save(self, user: User) -> User:

        return user.save()
    
def user_repository_factory() -> Callable[[], UserRepository]:
    _instance = None
    def get_instance() -> UserRepository:
        nonlocal _instance
        if _instance is None:
            _instance = UserRepository()
        return _instance
    return get_instance

get_user_repository = user_repository_factory()

class NotificationSettingRepository:
    def find_by_user_id(self, user_id: int) -> NotificationSetting | None:

        return NotificationSetting.objects.filter(user_id=user_id, deleted_at=None).first()
    
    def save(self, notification_setting: NotificationSetting) -> NotificationSetting:

        return notification_setting.save()
    
def notification_setting_repository_factory() -> Callable[[], NotificationSettingRepository]:
    _instance = None
    def get_instance() -> NotificationSettingRepository:
        nonlocal _instance
        if _instance is None:
            _instance = NotificationSettingRepository()
        return _instance
    return get_instance

get_notification_setting_repository = notification_setting_repository_factory()