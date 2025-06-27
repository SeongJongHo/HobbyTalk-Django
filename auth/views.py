from django.views import View

from auth.dtos import SignUpDto
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