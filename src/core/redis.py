from contextlib import asynccontextmanager
from typing import AsyncIterator
from redis.asyncio import Redis
from config import settings


@asynccontextmanager
async def redis_connection() -> AsyncIterator[Redis]:
    redis = Redis.from_url(
        settings.REDIS_URL, decode_responses=True, max_connections=30, socket_connect_timeout=0.5
    )

    try:
        yield redis
    finally:
        await redis.close()


async def get_redis_pool() -> Redis:
    async with redis_connection() as redis:
        return redis
