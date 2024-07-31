import logging
from inf_rabbit_utils.producer import Producer
from inf_rabbit_utils.consumer import Consumer

from utils.const import RabbitMQConfig, RabbitMQConfigOuter, QueueNames


class RabbitmqActions:
    def __init__(self) -> None:
        self.rabbitmq_host = RabbitMQConfig.HOST
        self.rabbitmq_port = RabbitMQConfig.PORT
        self.username = RabbitMQConfig.USER
        self.password = RabbitMQConfig.PASSWORD

        self.producers: dict[QueueNames, Producer] = {}
        self.colony_producer: Producer = None

    def publish(self, message, queue_name) -> None:
        try:
            producer = self.get_producer(queue_name)
            producer.publish(message)
            logging.info(f"publish to {queue_name} successfully completed")
        except Exception as error:
            logging.error(f"Failed to publish to {queue_name} - {error}")
            raise ValueError(f"Failed to publish to {queue_name} - {error}")

    def publish_to_colony(self, message) -> None:
        try:
            colony_producer = self.get_colony_producer()
            colony_producer.publish(message)
            logging.info(f"publish to {QueueNames.COLONY_QUEUE} successfully completed")
        except Exception as error:
            logging.error(f"Failed to publish to {QueueNames.COLONY_QUEUE} - {error}")
            raise ValueError(f"Failed to publish to {QueueNames.COLONY_QUEUE} - {error}")

    def consume(self, start_process, queue_name) -> None:
        consumer = Consumer(
            queue_name,
            start_process,
            QueueNames.ERROR_QUEUE,
            self.rabbitmq_host,
            self.rabbitmq_port,
            self.username,
            self.password,
        )
        consumer.consume()

    def get_producer(self, queue_name: str) -> Producer:
        producer = self.producers.get(queue_name)
        if producer is None:
            producer = self.add_producer(queue_name)
        return producer

    def add_producer(self, queue_name) -> Producer:
        producer = self.create_producer(
            queue_name, self.rabbitmq_host, self.rabbitmq_port, self.username, self.password
        )
        self.producers[queue_name] = producer
        return producer

    def get_colony_producer(self) -> Producer:
        if self.colony_producer is None:
            self.init_colony_producer()
        return self.colony_producer

    def init_colony_producer(self) -> None:
        self.colony_producer = self.create_producer(
            QueueNames.COLONY_QUEUE,
            RabbitMQConfigOuter.HOST,
            RabbitMQConfigOuter.PORT,
            RabbitMQConfigOuter.USER,
            RabbitMQConfigOuter.PASSWORD,
        )

    def create_producer(self, queue_name, host, port, username, password) -> Producer:
        try:
            return Producer(queue_name, host, port, username, password)
        except Exception as error:
            logging.error(f"Failed to create producer: {queue_name} - {error}")
            raise ValueError(f"Failed to create producer: {queue_name} - {error}")
