import datetime
import bcrypt
import jwt

from common.exceptions import InvalidTokenException
from config.settings import ALGORITHM, SECRET_KEY
from users.models import UserRole


class PasswordEncoder:
    @staticmethod
    def encode(password: str) -> str:

        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(8)).decode()
    
    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:

        return bcrypt.checkpw(password.encode(), hashed_password.encode())

class TokenPayload:
    user_id: int
    role: str
    is_access_token: bool
    exp: datetime.datetime
    def __init__(self, user_id: int, role: str, is_access_token: bool, exp: int):
        self.user_id = user_id
        self.role = role
        self.is_access_token = is_access_token
        self.exp = exp

    def to_dict(self) -> dict:
        return {
            'user_id': self.user_id,
            'role': self.role,
            'is_access_token': self.is_access_token,
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=self.exp) if self.exp else None
        }
    
    @staticmethod
    def of(dict: dict) -> 'TokenPayload':
        return TokenPayload(
            user_id=dict.get('user_id'),
            role=dict.get('role'),
            is_access_token=dict.get('is_access_token'),
            exp=dict.get('exp')
        )


class TokenProvider:
    @staticmethod
    def encode(payload: TokenPayload) -> str:
        return jwt.encode(payload.to_dict(), SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode(token: str) -> TokenPayload:
        try:
            return TokenPayload.of(jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM))
        except jwt.ExpiredSignatureError:
            raise InvalidTokenException("토큰이 만료되었습니다.", status=401)
        except jwt.InvalidTokenError:
            raise InvalidTokenException("유효하지 않은 토큰입니다.", status=401)