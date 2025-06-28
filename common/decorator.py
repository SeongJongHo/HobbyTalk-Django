import json
from functools import wraps
from time import time

from common.exceptions import JsonDecodeException, UnauthorizedException, ValidationException
from pydantic import ValidationError, BaseModel
from users.models import UserRole

def require_role(required_role: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user_role = getattr(request, 'role', None)
            if user_role is None:
                raise UnauthorizedException("권한이 없습니다. 로그인 후 다시 시도해주세요.")

            if not UserRole.has_permission(user_role, required_role):
                raise UnauthorizedException(f"권한이 없습니다. 현재 권한: {user_role}, 필요한 권한: {required_role}")

            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator

def validate_body(schema_cls: type[BaseModel]):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            try:
                raw = json.loads(request.body)
                validated = schema_cls(**raw)
                request.validated = validated
            except ValidationException as e:
                raise ValidationException(f"유효하지 않은 요청 본문입니다. {e}", status=400)
            except ValidationError as e:
                raise ValidationException(f"유효하지 않은 요청 본문입니다. {e.errors}", status=400)
            except json.JSONDecodeError:
                raise JsonDecodeException(f"유효하지 않은 요청 본문입니다. {request.body}", status=400)

            return view_func(self, request, *args, **kwargs)
        return wrapper
    return decorator

def guarded_by_role(required_role: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = getattr(request, 'user', None)
            if user is None:
                raise UnauthorizedException("권한이 없습니다. 로그인 후 다시 시도해주세요.")
            if not UserRole.has_permission(user.get('role', None), required_role):
                raise UnauthorizedException(f"권한이 없습니다. 현재 권한: {user.get('role', None)}, 필요한 권한: {required_role}")
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator

def retryable(max_retries: int = 3, delay: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(self, *args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator
