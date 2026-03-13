import redis

from django.conf import settings

class RedisClient:

    def __init__(self):

        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )

    def set(self, key, value, expire=None):

        self.client.set(key, value, ex=expire)

    def get(self, key):

        return self.client.get(key)

    def increment(self, key):

        return self.client.incr(key)