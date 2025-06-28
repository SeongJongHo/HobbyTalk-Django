from common.infra import RedisClient, get_redis_client


class LockRepository:
    def __init__(self, redis_client: RedisClient):
        self._redis_client = redis_client

    def acquire_lock(self, key: str, value: str, ex: int = 10) -> bool:
        
        return self._redis_client.set(key, value, ex=ex, nx=True)
    
    def release_lock(self, key: str, value: str):
        if self._redis_client.get(key) == value:
            self._redis_client.delete(key)

def lock_repository_factory() -> LockRepository:
    _instance = None
    def get_instance() -> LockRepository:
        nonlocal _instance
        if _instance is None:
            _instance = LockRepository(get_redis_client())
        return _instance
    return get_instance

get_lock_repository = lock_repository_factory()