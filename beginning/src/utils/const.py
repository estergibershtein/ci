from pydantic import BaseModel
from typing import Optional
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()


class QueueNames:
    INFINITY_IN_QUEUE = "infinity"
    PROCESS_QUEUE = "process_queue_name"
    ERROR_QUEUE = "inner_error_queue_name"
    COLONY_QUEUE = "colony_queue_name"


class RabbitMQConfig:
    HOST = os.getenv("RABBITMQ_HOST")
    PORT = os.getenv("RABBITMQ_PORT")
    USER = os.getenv("RABBITMQ_USER")
    PASSWORD = os.getenv("RABBITMQ_PASSWORD")


class RabbitMQConfigOuter:
    HOST = os.getenv("OUTER_RABBITMQ_HOST")
    PORT = os.getenv("OUTER_RABBITMQ_PORT")
    USER = os.getenv("OUTER_RABBITMQ_USER")
    PASSWORD = os.getenv("OUTER_RABBITMQ_PASSWORD")


class AzureConfig:
    CONNECTION_STRING = os.getenv("CONNECTION_STRING")


class RedisConfig:
    HOST = os.getenv("REDIS_HOST")
    PORT = os.getenv("REDIS_PORT")


class FlightType(Enum):
    NAVAD: str = "NAVAD"
    TELEM: str = "TELEM"


class FlightFormat(Enum):
    MERGE: str = "MERGE"
    ONE: str = "ONE"
    ALL: str = "ALL"


class DataFlight(BaseModel):
    flight_type: str
    flight_format: Optional[str]


class ColonyConfig:
    EMAILS = os.getenv("EMAILS")
