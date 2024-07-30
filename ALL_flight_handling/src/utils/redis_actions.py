import json
import redis

from utils.azLogger import create_logger
from utils.const import RedisConfig

logger = create_logger(__name__)


class RedisActions:
    def __init__(self) -> None:
        try:

            self.redis_config = RedisConfig()
            self.connect_redis = redis.Redis(host=self.redis_config.HOST, port=self.redis_config.PORT)
            logger.info(self.connect_redis ,"Connection to redis successfully completed.")
            # TODO  username="default",  password="secret"
            logger.info("Connection to redis successfully completed.")
        except Exception as error:
            logger.error(f"Failed to initialize variables in the RedisActions class - {error}")
            raise ValueError(f"Failed to initialize variables in the RedisActions class - {error}")

    def get_names_failed_children(self, flight_name: str) -> list:
        try:
            data_flight = self.get_json_data(flight_name)
            return data_flight["FailuresChildren"]
        except Exception as error:
            logger.error(f"Failed to get names failed child - {error}")
            raise ValueError(f"Failed to get names failed child - {error}")

    def update_count_sub_flight(self, flight_name: str) -> int:
        try:
            data_flight = self.get_json_data(flight_name)
            data_flight["CountSubFlight"] -= 1
            self.connect_redis.set(flight_name, json.dumps(data_flight))
            return data_flight["CountSubFlight"]
        except Exception as error:
            logger.error(f"Failed to update count sub flight - {error}")
            raise ValueError(f"Failed to update count sub flight - {error}")

    def get_json_data(self, flight_name: str) -> json.loads:
        try:
            return json.loads(self.connect_redis.get(flight_name))
        except Exception as error:
            logger.error(f"Failed to get flight - {error}")
            raise ValueError(f"Failed to get flight - {error}")

    def get_failed_children_and_error_description(self, flight_name: str):
        try:
            data_flight = self.get_json_data(flight_name)
            return data_flight["FailuresChildren"]
        except Exception as error:
            logger.error(f"Failed to get errors description - {error}")
            raise ValueError(f"Failed to get errors description - {error}")

    def delete_data_flight(self, flight_name: str):
        try:
            self.connect_redis.delete(flight_name)
            logger.info(f"Deleted data for flight {flight_name} from redis.")
        except Exception as error:
            logger.error(f"Failed to delete data for {flight_name} - {error}")
            raise ValueError(f"Failed to delete data for {flight_name} - {error}")
