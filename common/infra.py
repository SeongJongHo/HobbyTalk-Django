from collections.abc import Callable
from typing import List, Optional, Union
from venv import logger

from redis import RedisError
from config.settings import REDIS_CONFIG

class RedisClient:
    def __init__(self):
        import redis
        self._redis = redis.Redis(
            host=REDIS_CONFIG['host'],
            port=REDIS_CONFIG['port'],
            db=REDIS_CONFIG['db'],
            username=REDIS_CONFIG['username'],
            password=REDIS_CONFIG['password']
        )

    def set(self, key: str, value: Union[str, bytes], ex: Optional[int] = None, nx: bool = None) -> bool:
        return self._redis.set(name=key, value=value, ex=ex, nx=nx)

    def get(self, key: str) -> Optional[str]:
        return self._redis.get(name=key)

    def delete(self, *keys: str) -> int:
        return self._redis.delete(*keys)            

    def exists(self, key: str) -> bool:
        return self._redis.exists(key) > 0

    def expire(self, key: str, seconds: int) -> bool:
        return self._redis.expire(key, seconds)

    def incr(self, key: str, amount: int = 1) -> int:
        return self._redis.incr(key, amount)

    def decr(self, key: str, amount: int = 1) -> int:
        return self._redis.decr(key, amount)

    def lpush(self, key: str, *values: Union[str, bytes]) -> int:
        return self._redis.lpush(key, *values)

    def rpush(self, key: str, *values: Union[str, bytes]) -> int:
        return self._redis.rpush(key, *values)

    def lpop(self, key: str, count: int=None) -> Optional[bytes | List[bytes]]:
        return self._redis.lpop(key, count=count)

    def rpop(self, key: str, count: int=None) -> Optional[bytes | List[bytes]]:
        return self._redis.rpop(key, count=count)

    def llen(self, key: str) -> int:
        return self._redis.llen(key)

    def lrange(self, key: str, start: int, end: int) -> List[str]:
        return self._redis.lrange(key, start, end)

    def publish(self, channel: str, message: Union[str, bytes]) -> int:
        return self._redis.publish(channel, message)

    def subscribe(self, *channels: str):
        pubsub = self._redis.pubsub()
        pubsub.subscribe(*channels)
        return pubsub

    def pipeline(self, transaction: bool = True):
        return self.try_catch(func=self._redis.pipeline, transaction=transaction)
    
def redis_client_factory() -> Callable[[], RedisClient]:
    _instance = None
    def get_instance() -> RedisClient:
        nonlocal _instance
        if _instance is None:
            _instance = RedisClient()
        return _instance
    return get_instance

get_redis_client = redis_client_factory()