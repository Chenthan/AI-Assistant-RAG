from backend.cache.cache_client import client
from backend.utils.logger import logger


def get_cached_response(key: str):
    try:
        data = client.get(key)
        if data:
            resp = data.decode('utf-8')
            logger.info(f"Cache hit for key: {key}")
            return resp
    except Exception as e:
        logger.warning(f"Cache get failed: {e}")
    return None


def cache_response(key: str, response: str, ttl: int = 86400):
    try:
        client.set(key, response, ex=ttl)
        logger.info(f"Cached response for key: {key}")
    except Exception as e:
        logger.warning(f"Cache set failed: {e}")