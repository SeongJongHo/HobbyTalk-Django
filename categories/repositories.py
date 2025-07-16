from collections.abc import Callable
from categories.models import Category

class CategoryRepository:
    def find_by_id(self, category_id: int) -> Category | None:
        return Category.objects.filter(id=category_id, deleted_at=None).first()
    
    def find_all(self) -> list[Category]:
        return list(Category.objects.filter(deleted_at=None).order_by('-created_at'))
    
    def find_trending_categories(self) -> list[dict]:
        trending_categories = Category.objects.raw(
            """
            SELECT 
                c.id,
                c.name,
                COUNT(ocr.id) AS open_chat_room_count
            FROM categories as c
            INNER JOIN open_chat_rooms as ocr 
                ON c.id = ocr.category_id
                AND ocr.deleted_at IS NULL
            WHERE c.deleted_at IS NULL
            GROUP BY c.id
            ORDER BY open_chat_room_count DESC
            LIMIT 5
        """)

        return list(trending_categories)

def categoryRepositoryFactory() ->  Callable[[], CategoryRepository]:
    _instance = None
    def get_instance() -> CategoryRepository:
        nonlocal _instance
        if _instance is None:
            _instance = CategoryRepository()
        return _instance
    return get_instance
    
get_category_repository = categoryRepositoryFactory()