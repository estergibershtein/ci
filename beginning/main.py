from beginning import beginning
from utils.azLogger import create_logger
from utils.rabbitmq_actions import RabbitmqActions
from utils.const import QueueNames

logger = create_logger(__name__)


def main():
    rabbitmq = RabbitmqActions()
    rabbitmq.consume(beginning, QueueNames.INFINITY_IN_QUEUE)
