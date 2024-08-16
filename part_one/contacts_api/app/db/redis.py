import redis.asyncio as redis
from app.settings import settings


async def get_redis():
    # pool = redis.ConnectionPool.from_url(settings.db_url, decode_responses=True)
    client = redis.Redis.from_url(settings.db_url, decode_responses=True)
    try:
        yield client
    finally:
        await client.close()