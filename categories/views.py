from django.views import View

from categories.services import get_category_service
from common.response import ResponseGenerator, ResponseMsg

class CategoryViewV1(View):
    def __init__(self, category_service=get_category_service()):
        self.category_service = category_service

    def get(self, request, category_id=None):
        result = None
        if category_id:
            result = self.category_service.get_category(category_id)
        else: result = self.category_service.get_categories()

        return ResponseGenerator.build(message=ResponseMsg.SUCCESS, data=result, status=200)

class TrendingCategoryViewV1(View):
    def __init__(self, category_service=get_category_service()):
        self.category_service = category_service

    def get(self, request):
        result = self.category_service.get_trending_categories()
        
        return ResponseGenerator.build(message=ResponseMsg.SUCCESS, data=result, status=200)