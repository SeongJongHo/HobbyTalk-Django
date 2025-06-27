from collections.abc import Callable
from common.exceptions import AlreadyExistsException
from users.commands import CreateUserCommand
from users.models import NotificationSetting
from users.repositories import NotificationSettingRepository, UserRepository, get_notification_setting_repository, get_user_repository

class UserService:
    def __init__(self, user_repository: UserRepository, notification_setting_repository: NotificationSettingRepository):
        self.user_repository = user_repository
        self.notification_setting_repository = notification_setting_repository

    def create(self, user: CreateUserCommand) -> int:
        if self.user_repository.find_by_username(user.username):
            raise AlreadyExistsException(f"이미 존재하는 유저네임입니다. username: {user.username}")
        if self.user_repository.find_by_phone_number(user.phone_number):
            raise AlreadyExistsException(f"이미 존재하는 전화번호입니다. phone_number: {user.phone_number}")
        
        new_user = user.to_model()
        self.user_repository.save(new_user)
        self.notification_setting_repository.save(notification_setting=NotificationSetting(user=new_user))

        return new_user.id
    
def get_user_service_factory() -> Callable[[], UserService]:
    _instance = None
    def get_instance() -> UserService:
        nonlocal _instance
        if _instance is None:
            _instance = UserService(
                user_repository=get_user_repository(),
                notification_setting_repository=get_notification_setting_repository()
            )
        return _instance
    return get_instance

get_user_service = get_user_service_factory()