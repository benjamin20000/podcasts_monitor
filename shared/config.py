import os
from dotenv import load_dotenv

load_dotenv()
directory_path = os.getenv("podcasts_dir")
elastic_uri = os.getenv("elastic_uri")
mongo_uri = os.getenv("mongo_uri")
elastic_metadata_index = "files_metadata"