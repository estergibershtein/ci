from utils.azLogger import create_logger
from utils.const import QueueNames, ColonyConfig
from utils.rabbitmq_actions import RabbitmqActions
from utils.redis_actions import RedisActions

logger = create_logger(__name__)


def ALL_flight_handling(flight_message: dict) -> None:
    rabbitmq = RabbitmqActions()
    try:
        parent_name = flight_message["payload"]["folder"]
        logger.info(f"Starting Handling sub-flight of {parent_name}.")
        redis = RedisActions()
        count_failed_children = len(redis.get_names_failed_children(parent_name))
        count_sub_flight = redis.update_count_sub_flight(parent_name)
        if count_sub_flight == 0 and count_failed_children != 0:
            handle_failed_flight(flight_message, rabbitmq, redis, parent_name)
        if count_sub_flight == 0 and count_failed_children == 0:
            handle_success_flight(flight_message, rabbitmq, redis, parent_name)
    except Exception as error:
        parent_name = flight_message["payload"]["folder"]
        logger.error(f"Handling sub-flight of {parent_name} failed flight - {error}.")
        flight_message["error"] = {flight_message["flightData"]["flightPath"]: f"ALL_flight_handling service- {error}."}
        rabbitmq.publish(flight_message, QueueNames.ERROR_QUEUE)


def handle_failed_flight(
    flight_message: dict, rabbitmq: RabbitmqActions, redis: RedisActions, parent_name: str
) -> None:
    flight_message["payload"] = update_flight_message_to_error(flight_message, redis, parent_name)
    logger.error(f"The flight {parent_name} has been sent to colony queue.")
    rabbitmq.publish_to_colony(flight_message)
    redis.delete_data_flight(parent_name)


def handle_success_flight(
    flight_message: dict, rabbitmq: RabbitmqActions, redis: RedisActions, parent_name: str
) -> None:
    flight_message["flightData"] = update_flight_message(parent_name)
    logger.info(f"The flight {parent_name} has been sent to skyline queue.")
    rabbitmq.publish(flight_message, QueueNames.SEND_TO_SKYLINE_QUEUE)
    redis.delete_data_flight(parent_name)


def update_flight_message_to_error(flight_message: dict, redis: RedisActions, parent_name: str) -> dict:
    failed_children_and_error_description = redis.get_failed_children_and_error_description(parent_name)
    flight_message["payload"]["errorDescription"] = "There are sub-flight that failed"
    flight_message["payload"]["failuresChildren"] = failed_children_and_error_description
    flight_message["payload"]["mailTo"] = ColonyConfig.EMAILS
    flight_message.pop("flightData")
    return flight_message["payload"]


def update_flight_message(flight_name: dict) -> dict:
    return {
        "flightPath": flight_name,
        "flightFormat": "ALL",
        "flightType": "NAVAD",
        "flightName": flight_name,
        "parent": None,
    }
