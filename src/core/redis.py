from typing import AsyncIterator
from redis.asyncio import Redis
from config import settings


async def get_redis_pool() -> AsyncIterator[Redis]:
    redis = redis.from_url(
        settings.REDIS_URL,
        decode_responses=True
    )
    try:
        yield redis
    finally:
        await redis.close()
