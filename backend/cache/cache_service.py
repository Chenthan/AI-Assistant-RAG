from backend.cache.cache_client import client
from backend.utils.logger import logger


def get_cached_response(key: str):
    """
    Retrieve a cached response from Redis by key.
    Args:
        key (str): The cache key.
    Returns:
        str or None: The cached response if found, else None.
    """
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
    """
    Cache a response in Redis with a given key and TTL.
    Args:
        key (str): The cache key.
        response (str): The response to cache.
        ttl (int, optional): Time-to-live in seconds. Defaults to 86400 (1 day).
    """
    try:
        client.set(key, response, ex=ttl)
        logger.info(f"Cached response for key: {key}")
    except Exception as e:
        logger.warning(f"Cache set failed: {e}")