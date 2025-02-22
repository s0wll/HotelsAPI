from src.connectors.redis_connector import RedisConnector
from src.config import settings

redis_connector = RedisConnector(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
)
