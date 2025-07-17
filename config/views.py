from django.views import View

from common.response import ResponseGenerator, ResponseMsg

class HealthView(View):
    
    def get(self, request):
        return ResponseGenerator.build(
            message=ResponseMsg.SUCCESS,
            status=200
        )