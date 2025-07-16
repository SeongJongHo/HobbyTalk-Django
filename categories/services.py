from typing import Callable
from categories.repositories import CategoryRepository, get_category_repository
from common.exceptions import NotFoundException

class CategoryService:
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    def get_category(self, category_id: int) -> dict:
        category = self.category_repository.find_by_id(category_id)
        if not category:
            raise NotFoundException(f"존재하지 않는 카테고리 입니다. id: {category_id}")
        
        return {
            "id": category.id,
            "name": category.name,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
        }
    
    def get_categories(self) -> list[dict]:
        categories = self.category_repository.find_all()

        return [
            {
                "id": category.id,
                "name": category.name,
                "created_at": category.created_at,
                "updated_at": category.updated_at,
            }
            for category in categories
        ]
    
    def get_trending_categories(self) -> list[dict]:
        return [
            {   
                "id": category.id,
                "name": category.name,
                "open_chat_room_count": category.open_chat_room_count   
            }
            for category in self.category_repository.find_trending_categories()
        ]

def categoryServiceFactory() -> Callable[[], CategoryService]:
    _instance = None
    def get_instance() -> CategoryService:
        nonlocal _instance
        if _instance is None:
            _instance = CategoryService(get_category_repository())
        return _instance
    return get_instance

get_category_service = categoryServiceFactory()