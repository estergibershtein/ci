from azure_operations.azure_connection import AzureContainer
from utils.azLogger import create_logger
from utils.redis_actions import RedisActions
from utils.check_type import get_flight_type
from utils.azure import get_container
from utils.const import QueueNames, ColonyConfig
from utils.rabbitmq_actions import RabbitmqActions

logger = create_logger(__name__)


def beginning(flight_message: dict) -> None:
    rabbitmq = RabbitmqActions()
    flight_name = flight_message["payload"]["folder"]
    try:
        logger.info(f"Starting beginning process {flight_name}")
        container = get_container(flight_message["payload"]["container"])
        flight_message["flightData"] = get_flight_data(container, flight_name)

        if flight_message["flightData"]["flightFormat"] != "ALL":
            logger.info(f"The flight {flight_name} has been sent to process queue.")
            rabbitmq.publish(flight_message, QueueNames.PROCESS_QUEUE)
        else:
            all_flights_management(container, rabbitmq, flight_message)
    except Exception as error:
        logger.error(f"The flight {flight_name} has been sent to error queue - {error}.")
        flight_message = update_before_publish_to_colony(flight_message, error)
        rabbitmq.publish_to_colony(flight_message)


def get_flight_data(container: AzureContainer, flight_name: str, parent_name=None) -> dict:
    flight_path = f"{parent_name}/{flight_name}" if parent_name is not None else flight_name
    flight_type = get_flight_type(container, flight_path)
    return {
        "flightPath": flight_path,
        "flightType": flight_type.flight_type,
        "flightFormat": flight_type.flight_format,
        "flightName": flight_name,
        "parent": parent_name,
    }


def update_before_publish_to_colony(flight_message, error) -> dict:
    flight_message["action"] = "VerifyError"
    flight_message["payload"]["errorDescription"] = {flight_message["payload"]["folder"]: f"beginner - {error}"}
    flight_message["payload"]["mailTo"] = ColonyConfig.EMAILS
    if "flightData" in flight_message:
        flight_message.pop("flightData")
    return flight_message


def all_flights_management(container: AzureContainer, rabbitmq: RabbitmqActions, flight_message: str) -> None:
    parent_name = flight_message["payload"]["folder"]
    flight_list = container.get_folders_from_external_folder(parent_name)
    redis = RedisActions()
    redis.save_data_flight(parent_name, len(flight_list))
    for flight_name in flight_list:
        handle_sub_flight(container, rabbitmq, flight_message, parent_name, flight_name)


def handle_sub_flight(
    container: AzureContainer, rabbitmq: RabbitmqActions, flight_message: dict, parent_name: str, flight_name: str
) -> None:
    try:
        flight_message["flightData"] = get_flight_data(container, flight_name, parent_name)
        logger.info(f"The flight {flight_name} has been sent to process queue.")
        rabbitmq.publish(flight_message, QueueNames.PROCESS_QUEUE)
    except Exception as error:
        logger.error(f"The flight {flight_name} has been sent to error queue - {error}")
        flight_message["error"] = {flight_message["flightData"]["flightPath"]: f"beginning service- {error}"}
        flight_message["flightData"]["parent"] = parent_name
        rabbitmq.publish(flight_message, QueueNames.ERROR_QUEUE)
