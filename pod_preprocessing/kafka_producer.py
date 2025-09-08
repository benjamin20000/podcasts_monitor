from kafka import KafkaProducer
import json
from logger import Logger

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.logger = Logger.get_logger()

    def produce(self, data):
        try:
            topic_name = 'pod_file_meta_data'
            self.producer.send(topic_name, data)
            self.logger.info(f"data: {data} sent to kafka topic: {topic_name}")
            self.producer.flush()
        except Exception as e:
            self.logger.error(f"error occurred when trying to send data: {data} to kafka: {e}")



