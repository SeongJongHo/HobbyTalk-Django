import datetime
import bcrypt
import jwt

from config.settings import ALGORITHM, SECRET_KEY


class PasswordEncoder:
    @staticmethod
    def encode(password: str) -> str:

        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(8)).decode('utf-8')
    
    @staticmethod
    def verify(password: str, hashed_password: str) -> bool:

        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

class TokenProvider:
    @staticmethod
    def encode(payload: dict, expire_minutes: int = 10) -> str:
        if 'exp' not in payload:
            payload['exp'] = datetime.utcnow() + datetime.timedelta(minutes=expire_minutes)

        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def decode(token: str) -> dict:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)