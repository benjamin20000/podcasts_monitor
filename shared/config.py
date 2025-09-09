import os
from dotenv import load_dotenv

load_dotenv()

## hosts
elastic_uri = os.getenv("elastic_uri")
mongo_uri = os.getenv("mongo_uri")
kafka_uri = os.getenv("kafka_uri")

## kafka topics
processing_kafka_topic = "metadata_topic"
stt_kafka_topic = "stt_topic"
bds_kafka_topic = "bds_topic"

# paths
directory_path = os.getenv("podcasts_dir")
temp_folder_path = "../data/temp"
black_list_path = "../data/black_list.txt"
grey_list_path = "../data/grey_list.txt"

# es indexes
elastic_metadata_index = "files_metadata"
