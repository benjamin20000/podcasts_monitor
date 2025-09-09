from kafka import KafkaConsumer
import json
from shared.config import kafka_uri
from shared.logger import Logger

class Consumer:
    def __init__(self, topic_name):
        self.logger = Logger.get_logger()
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=[kafka_uri],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my_consumer_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=5000
        )

    ## consume func get a callback_function
    ## for handling with the new message arrives
    def consume(self, callback_function):
        for message in self.consumer:
            self.logger.info(f"new message hase consume: {message.value}")
            callback_function(message.value)
        self.consumer.close()




