from auth.services import AuthService, get_auth_service
from users.models import UserRole

class AuthMiddleware:
    def __init__(self, get_response, auth_service: AuthService=get_auth_service()):
        self.get_response = get_response
        self.auth_service = auth_service

    def __call__(self, request):
        
        access_token = request.headers.get('Authorization', None)
        refresh_token = request.COOKIES.get('refresh_token', None)

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