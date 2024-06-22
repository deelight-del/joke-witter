"""Redis connector"""
from redis import Redis
from redis.exceptions import ConnectionError, RedisError


class RedisDB:
    __redis: Redis | None = None

    def __init__(self) -> None:
        self.__redis = Redis()

        try:
            if not self.__redis.ping():
                self.__redis = None
        except ConnectionError:
            self.__redis = None

    def connected(self) -> bool:
        """Checks if the redis database is active and connected to"""
        return self.__redis is not None

    def set(self, key: str, obj: dict):
        """Sets a new item in the hash cache"""
        if self.__redis is None:
            raise RedisError

        self.__redis.json().set(key, '$', obj=obj)

    def get(self, key: str) -> list:
        """Retrives an item in the cache"""
        if self.__redis is None:
            raise RedisError

        obj = self.__redis.json().get(key, '$')

        if obj is None:
            raise KeyError(f'Key {key} is not present')

        return obj

    def delete(self, key: str) -> None:
        """Delete an item from the cache"""
        if self.__redis is None:
            raise RedisError

        self.__redis.json().delete(key, '$')
