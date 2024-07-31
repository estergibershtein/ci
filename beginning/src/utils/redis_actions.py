import json
from utils.const import RedisConfig
import redis
from utils.azLogger import create_logger

logger = create_logger(__name__)


class RedisActions:
    def __init__(self) -> None:
        try:
            self.redis_config = RedisConfig()
            self.connect_redis = redis.Redis(host=self.redis_config.HOST, port=self.redis_config.PORT)
            # TODO  username="default",  password="secret"
            logger.info("Connection to redis successfully completed.")
        except Exception as error:
            logger.error(f"Failed to initialize variables in the RedisActions class - {error}")
            raise ValueError(f"Failed to initialize variables in the RedisActions class - {error}")

    def save_data_flight(self, flight_name: str, sum_folders: int) -> None:
        try:
            value = {"CountSubFlight": sum_folders, "FailuresChildren": []}
            self.connect_redis.set(flight_name, json.dumps(value))
            logger.info(f"Data saved to redis for flight {flight_name}")
        except Exception as error:
            logger.error(f"Failed to save data to redis for flight {flight_name} - {error}")
            raise ValueError(f"Failed to save data to redis for flight {flight_name} - {error}")
