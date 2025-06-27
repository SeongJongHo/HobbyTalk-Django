from collections.abc import Callable
from categories.models import Category

class CategoryRepository:
    def find_by_id(self, category_id: int) -> Category | None:
        return Category.objects.filter(id=category_id, deleted_time=None).first()
    
    def find_all(self) -> list[Category]:
        return list(Category.objects.filter(deleted_time=None).order_by('-created_at'))

def categoryRepositoryFactory() ->  Callable[[], CategoryRepository]:
    _instance = None
    def get_instance() -> CategoryRepository:
        nonlocal _instance
        if _instance is None:
            _instance = CategoryRepository()
        return _instance
    return get_instance
    
get_category_repository = categoryRepositoryFactory()