from redis.asyncio import Redis
from typing import Any
import json


class Redis:

    @staticmethod
    async def set_redis_cache(redis: Redis, key: str, value: Any, expire: int):
        await redis.setex(key, expire, json.dumps(value))

    @staticmethod
    async def get_redis_cache(redis: Redis, key: str) -> Any:
        cache = await redis.get(key)
        if cache:
            return json.loads(cache)
        return None
