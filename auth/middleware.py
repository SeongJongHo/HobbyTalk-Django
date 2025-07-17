from auth.services import AuthService, get_auth_service
from users.models import UserRole
from channels.db import database_sync_to_async

class AuthMiddleware:
    def __init__(self, get_response, auth_service: AuthService=get_auth_service()):
        self.get_response = get_response
        self.auth_service = auth_service

    def __call__(self, request):
        
        access_token = request.headers.get('Authorization', None)
        refresh_token = request.COOKIES.get('refresh_token', None)
        print(f"Access Token: {access_token}, Refresh Token: {refresh_token}")
        print(request.headers.get('cookie'))
        try:
            user = self.auth_service.authenticate(access_token, refresh_token)
            request.user = {
                'user_id': user.get('user_id', 0),
                'role': user.get('role', UserRole.UNKNOWN),
            }
        except Exception as e:
            request.user = self.get_unknown_user()

        response = self.get_response(request)

        return response
    
    def get_unknown_user(self):
        return {
            'user_id': None,
            'role': UserRole.UNKNOWN,
        }
    
def parse_cookies(headers: list[tuple[bytes, bytes]]) -> dict:
    cookies = {}
    for name, value in headers:
        if name == b"cookie":
            cookie_str = value.decode()
            items = cookie_str.split(";")
            for item in items:
                if "=" in item:
                    k, v = item.strip().split("=", 1)
                    cookies[k] = v
    return cookies

class WebSocketAuthMiddleware:
    def __init__(self, inner, auth_service: AuthService = get_auth_service()):
        self.inner = inner
        self.auth_service = auth_service

    def __call__(self, scope):
        return WebSocketAuthMiddlewareInstance(scope, self.inner, self.auth_service)

class WebSocketAuthMiddlewareInstance:
    def __init__(self, scope, inner, auth_service):
        self.scope = scope
        self.inner = inner
        self.auth_service = auth_service

    async def __call__(self, receive, send):
        headers = dict((k.decode(), v.decode()) for k, v in self.scope["headers"])
        cookies = parse_cookies(self.scope["headers"])

        access_token = headers.get("authorization")
        refresh_token = cookies.get("refresh_token")

        try:
            user = await self.authenticate_async(access_token, refresh_token)
            self.scope["user"] = {
                "user_id": user.get("user_id", 0),
                "role": user.get("role", UserRole.UNKNOWN),
            }
        except Exception:
            await send({
                "type": "websocket.close",
                "status": 4401
            })
            return

        return await self.inner(self.scope, receive, send)

    @database_sync_to_async
    def authenticate_async(self, access_token, refresh_token):
        return self.auth_service.authenticate(access_token, refresh_token)

    def get_unknown_user(self):
        return {
            "user_id": None,
            "role": UserRole.UNKNOWN,
        }