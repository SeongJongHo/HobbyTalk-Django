from collections.abc import Callable
from django.db import transaction
from auth.dtos import SignUpDto
from auth.models import CurrentUser
from auth.repositories import CurrentUserRepository, get_current_user_repository
from common.exceptions import InvalidValueException, NotFoundException, UnauthorizedException
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
                'is_access_token': is_access,
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
    def __init__(self, user_service: UserService, token_service: TokenService, current_user_repository: CurrentUserRepository):
        self.user_service = user_service
        self.token_service = token_service
        self.current_user_repository = current_user_repository
    
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
    
    def sign_in(self, username: str, password: str) -> dict:
        user = self.user_service.user_repository.find_by_username(username)
        if not user:
            raise NotFoundException(f"존재하지 않는 유저네임입니다. username: {username}")
        if not PasswordEncoder.verify(password, user.password):
            raise UnauthorizedException("비밀번호가 일치하지 않습니다.")
        
        access_token = self.token_service.generate_access_token(user_id=user.id, user_role=user.role)
        refresh_token = self.token_service.generate_refresh_token(user_id=user.id, user_role=user.role)
        current_user = CurrentUser.of({
            'user_id': user.id,
            'role': user.role,
            'refresh_token': refresh_token
        })
        self.current_user_repository.save(current_user)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }
    
def auth_service_factory() -> Callable[[], AuthService]:
    _instance = None
    def get_instance() -> AuthService:
        nonlocal _instance
        if _instance is None:
            _instance = AuthService(
                user_service=get_user_service(), 
                token_service=get_token_service(), 
                current_user_repository=get_current_user_repository())
        return _instance
    return get_instance

get_auth_service = auth_service_factory()