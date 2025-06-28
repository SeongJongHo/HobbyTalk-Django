from django.views import View

from auth.dtos import SignInDto, SignUpDto
from auth.services import AuthService, get_auth_service
from common.decorator import validate_body
from common.response import ResponseGenerator, ResponseMsg

class AuthViewV1(View):
    def __init__(self, auth_service: AuthService=get_auth_service()):
        self.auth_service = auth_service

    @validate_body(SignUpDto)
    def post(self, request):
        return ResponseGenerator.build(
            message=ResponseMsg.CREATED,
            data={ 'user_id': self.auth_service.sign_up(request.validated) },
            status=201
        )
    
    def get(self, request):
        refresh_token = request.COOKIES.get('refresh_token', None)
        token_set = self.auth_service.refresh_token(refresh_token)
        
        return ResponseGenerator.build(
            message=ResponseMsg.SUCCESS,
            data={ 'access_token': token_set['access_token'] },
            status=200,
            refresh_token=token_set.get('refresh_token', None)
        )

class SignInViewV1(View):
    def __init__(self, auth_service: AuthService=get_auth_service()):
        self.auth_service = auth_service
    
    @validate_body(SignInDto)
    def post(self, request):
        token_set = self.auth_service.sign_in(request.validated.username, request.validated.password)

        return ResponseGenerator.build(
            message=ResponseMsg.SUCCESS,
            data={ 'access_token': token_set['access_token'] },
            status=200,
            refresh_token=token_set.get('refresh_token', None)
        )