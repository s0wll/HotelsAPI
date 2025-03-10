import logging

import redis.asyncio as redis


class RedisConnector:  # Класс с ф-ями для подключения асинхронного редиса
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.redis = None

    async def connect(self):
        logging.info(f"Начинаю поддключение к Redis, host={self.host}, port={self.port}")
        self.redis = await redis.Redis(host=self.host, port=self.port)
        logging.info(f"Успешное поддключение к Redis, host={self.host}, port={self.port}")

    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.redis.set(key, value, ex=expire)
        else:
            await self.redis.set(key, value)

    async def get(self, key: str):
        value = await self.redis.get(key)
        return value

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def close(self):
        await self.redis.close()
