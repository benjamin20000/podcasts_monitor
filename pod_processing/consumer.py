from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
import os
from processor import Processor


class ConsumeMetadata:
    def __init__(self):
        load_dotenv()
        topic_name = 'pod_file_meta_data'
        kafka_uri = os.getenv("kafka_uri")
        self.consumer = KafkaConsumer(
            topic_name,
            bootstrap_servers=[kafka_uri],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='my_consumer_group',
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=5000
        )

    def consume(self):
        processor = Processor()
        for message in self.consumer:
            processor.process(message.value)


