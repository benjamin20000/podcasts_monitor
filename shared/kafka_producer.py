from kafka import KafkaProducer
import json
from shared.logger import Logger
from shared.config import kafka_uri


class Producer:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.producer = self.create_producer()

    def create_producer(self):
        try:
            producer = KafkaProducer(
                bootstrap_servers=[kafka_uri],
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            self.logger.info(f"producer created")
            return producer
        except Exception as e:
            self.logger.error(f"failed to connect to Kafka brokers: {e}")
            raise Exception(f"failed to connect to Kafka brokers: {e}")




    def produce(self, data, topic_name):
        try:
            self.producer.send(topic_name, data)
            self.logger.info(f"data: {data} sent to kafka topic: {topic_name}")
            self.producer.flush()
        except Exception as e:
            self.logger.error(f"error occurred when trying to send data: {data} to kafka: {e}")



