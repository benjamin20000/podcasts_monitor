from kafka import KafkaProducer
import json

class Producer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce(self, data):
        topic_name = 'pod_file_meta_data'
        self.producer.send(topic_name, data)
        self.producer.flush()