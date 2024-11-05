from typing import AsyncIterator
from config import settings
import aioredis


async def get_redis_pool() -> AsyncIterator[aioredis.Redis]:
    redis = aioredis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    try:
        yield redis
    finally:
        await redis.close()
