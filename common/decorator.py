from functools import wraps

from common.exceptions import UnauthorizedException
from users.models import UserRole

def require_role(required_role: str):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = getattr(request, 'role', None)
            if user_role is None:
                raise UnauthorizedException("권한이 없습니다. 로그인 후 다시 시도해주세요.")

            if not UserRole.has_permission(user_role, required_role):
                raise UnauthorizedException(f"권한이 없습니다. 현재 권한: {user_role}, 필요한 권한: {required_role}")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator