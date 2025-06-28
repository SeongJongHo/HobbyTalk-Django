from auth.models import CurrentUser
from common.infra import RedisClient, get_redis_client


class CurrentUserRepository:
    def __init__(self, redis_client: RedisClient):
        self._redis_client = redis_client
        self._key_prefix = 'current_user:'
        self._ttl = 60 * 60 * 24 * 30

    def findById(self, user_id: int) -> CurrentUser | None:
        return CurrentUser.from_json(self._redis_client.get(self._generate_key(user_id)))
    
    def save(self, current_user: CurrentUser):
        self._redis_client.set(
            key=self._generate_key(current_user.user_id),
            value=current_user.to_json(),
            ex=self._ttl
        )
        
    def _generate_key(self, user_id: int) -> str:
        return f"{self._key_prefix}{user_id}"

def current_user_repository_factory() -> CurrentUserRepository:
    _instance = None
    def get_instance() -> CurrentUserRepository:
        nonlocal _instance
        if _instance is None:
            _instance = CurrentUserRepository(get_redis_client())
        return _instance
    return get_instance

get_current_user_repository = current_user_repository_factory()