from functools import lru_cache

import redis

from app.core.config import settings


@lru_cache
def get_redis():
    return redis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
    )


redis_client = get_redis()


def redis_ping() -> bool:
    return bool(redis_client.ping())


def redis_set(key: str, value: str, ex: int | None = None) -> bool:
    return bool(redis_client.set(key, value, ex=ex))


def redis_get(key: str):
    return redis_client.get(key)


def redis_delete(key: str) -> int:
    return redis_client.delete(key)
