"""Redis connector"""

from redis import Redis
from redis.exceptions import ConnectionError, RedisError


class RedisDB:
    __redis: Redis | None = None

    def __init__(self, host: str = "localhost", port: int = 6379) -> None:
        self.__redis = Redis(host=host, port=port)

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
            raise RedisError("Redis not initialized")

        self.__redis.json().set(key, "$", obj=obj)

    def get(self, key: str, field: str | None = None) -> list:
        """Retrives an item in the cache"""
        if self.__redis is None:
            raise RedisError("Redis not initialized")

        obj = self.__redis.json().get(key, f'${"" if field is None else f".{field}"}')

        if obj is None:
            raise KeyError(f"Key {key} is not present")

        print(obj)
        return obj

    def delete(self, key: str) -> None:
        """Delete an item from the cache"""
        if self.__redis is None:
            raise RedisError("Redis not initialized")

        self.__redis.json().delete(key, "$")

    def append(self, key: str, field: str, *val):
        """Append a value to an array field in the cache.

        The field must a field present in the json object
        """
        if self.__redis is None:
            raise RedisError("Redis not initialized")

        self.__redis.json().arrappend(key, f"$.{field}", *val)

    def remove(self, key: str, field: str, _id: str):
        """Remove an item from an object field.

        The field must a field present in the json object
        """
        if self.__redis is None:
            raise RedisError("Redis not initialized")
        self.__redis.json().delete(key, f"$.{field}.{_id}")

    def insert(self, key: str, field: str, _id: str):
        """Insert a value to a object field in the cache.

        The field must a field present in the json object
        """
        if self.__redis is None:
            raise RedisError("Redis not initialized")

        self.__redis.json().set(key, f"$.{field}", {_id: 1})

    def exist(self, key: str, field: str, _id: str) -> bool:
        """Check if an item is present in a field with id."""
        if self.__redis is None:
            raise RedisError("Redis not initialized")
        return len(self.__redis.json().get(key, f"$.{field}.{_id}")) != 0
