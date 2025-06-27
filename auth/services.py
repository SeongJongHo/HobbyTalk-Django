from collections.abc import Callable
from django.db import transaction
from auth.dtos import SignUpDto
from common.exceptions import InvalidValueException
from common.security import PasswordEncoder, TokenPayload, TokenProvider
from users.models import UserRole
from users.services import UserService, get_user_service

class TokenService:
    REFRESH_TOKEN_EXPIRATION_MINUTES = 60 * 24 * 30
    ACCESS_TOKEN_EXPIRATION_MINUTES = 10
    
    def generate_access_token(self, user_id: int, user_role: str) -> str:
        return TokenProvider.encode(self._get_payload(user_id, user_role, True))
    
    def generate_refresh_token(self, user_id: int, user_role: str) -> str:
        return TokenProvider.encode(self._get_payload(user_id, user_role, False))
    
    def decode_token(self, token: str) -> dict:
        return TokenProvider.decode(token).to_dict()
    
    def _get_payload(self, user_id: str, role: str, is_access: bool) -> TokenPayload:
            return TokenPayload.of({
                'user_id': user_id,
                'role': role,
                'is_accessToken': is_access,
                'exp': self.ACCESS_TOKEN_EXPIRATION_MINUTES if is_access else self.REFRESH_TOKEN_EXPIRATION_MINUTES
            })
    
def token_service_factory() -> Callable[[], TokenService]:
    _instance = None
    def get_instance() -> TokenService:
        nonlocal _instance
        if _instance is None:
            _instance = TokenService()
        return _instance
    return get_instance

get_token_service = token_service_factory()

class AuthService:
    def __init__(self, user_service: UserService, token_service: TokenService):
        self.user_service = user_service
        self.token_service = token_service
    
    @transaction.atomic
    def sign_up(self, user: SignUpDto) -> int:
        if user.password != user.password_confirm:
            raise InvalidValueException("비밀번호가 일치하지 않습니다.", status=400)
        if self.user_service.user_repository.find_by_username(user.username):
            raise InvalidValueException(f"이미 존재하는 유저네임입니다. username: {user.username}", status=400)
        if user.role not in UserRole._labels and user.role == UserRole.UNKNOWN:
            raise InvalidValueException(f"유효하지 않은 역할입니다. role: {user.role}", status=400)
        
        command_user = user.to_command(hashed_password=PasswordEncoder.encode(user.password))
        user_id = self.user_service.create(command_user)

        return user_id
    
def auth_service_factory() -> Callable[[], AuthService]:
    _instance = None
    def get_instance() -> AuthService:
        nonlocal _instance
        if _instance is None:
            _instance = AuthService(user_service=get_user_service(), token_service=get_token_service())
        return _instance
    return get_instance

get_auth_service = auth_service_factory()