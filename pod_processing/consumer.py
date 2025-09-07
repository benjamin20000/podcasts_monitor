from kafka import KafkaConsumer
import json
from dotenv import load_dotenv
import os


class ConsumeMetaData:
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
        )

    def consume(self):
        for message in self.consumer:
            print(message)



a = ConsumeMetaData()
a.consume()

