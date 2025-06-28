from django.http import JsonResponse

class ResponseMsg:
    SUCCESS = "Success"
    CREATED = "Created"
    FAILED = "Failed"

class ResponseGenerator:
    @staticmethod
    def build(message=ResponseMsg.SUCCESS, data=None, status=200, **kwargs):
        response_body = {
            'message': message,
            'status': status,
        }
        if data is not None:
            response_body['data'] = data

        response = JsonResponse(response_body, status=status)
        if kwargs.get('refresh_token') is not None:
            response.set_cookie('refresh_token', kwargs.get('refresh_token'), httponly=True, secure=True, samesite='Strict')
            
        return response