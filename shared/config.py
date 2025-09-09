import os
from dotenv import load_dotenv

load_dotenv()
directory_path = os.getenv("podcasts_dir")
elastic_uri = os.getenv("elastic_uri")
mongo_uri = os.getenv("mongo_uri")
kafka_uri = os.getenv("kafka_uri")
elastic_metadata_index = "files_metadata"
temp_folder_path = "../data/temp"
processing_kafka_topic = "metadata_topic"
stt_kafka_topic = "stt_topic"
black_list_path = "../data/black_list.txt"
grey_list_path = "../data/grey_list.txt"