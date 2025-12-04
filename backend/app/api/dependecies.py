from functools import lru_cache
from fastapi import Depends
from redis import Redis

from backend.app.config import settings
from backend.app.core.shortener import Shortener


@lru_cache()
def get_db() -> Redis:
    return Redis.from_url(url=settings.REDIS_URL, decode_responses = True)


@lru_cache()
def get_shortener(db: Redis = Depends(get_db)) -> Shortener:
    return Shortener(db)