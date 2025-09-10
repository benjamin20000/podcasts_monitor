from kafka import KafkaConsumer
import json

from kafka.errors import NoBrokersAvailable

from shared.config import kafka_uri
from shared.logger import Logger

class Consumer:
    def __init__(self, topic_name):
        self.logger = Logger.get_logger()
        self.consumer = self.create_consumer(topic_name)


    def create_consumer(self, topic_name):
        try:
            consumer = KafkaConsumer(
                topic_name,
                bootstrap_servers=[kafka_uri],
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my_consumer_group',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            )
            self.logger.info(f"consumer with topic {topic_name} created")
            return consumer
        except NoBrokersAvailable as e:
            self.logger.error(f"failed to connect to Kafka brokers: {e}")
            raise NoBrokersAvailable(f"failed to connect to Kafka brokers: {e}")


    ## consume func get a callback_function
    ## for handling with the new message arrives
    def consume(self, callback_function):
        for message in self.consumer:
            self.logger.info(f"new message hase consume: {message.value}")
            callback_function(message.value)
        self.consumer.close()




