from ALL_flight_handling import ALL_flight_handling
from utils.azLogger import create_logger
from utils.rabbitmq_actions import RabbitmqActions
from utils.const import QueueNames

logger = create_logger(__name__)


def main():
    rabbitmq = RabbitmqActions()
    rabbitmq.consume(ALL_flight_handling, QueueNames.END_PROCESS_QUEUE)
