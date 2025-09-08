from pymongo import MongoClient
from gridfs import GridFS
from dotenv import load_dotenv
import os


class MongoDal:
    def __init__(self):
        load_dotenv()
        uri = os.getenv("mongo_uri")
        client = MongoClient(uri)
        self.db = client["podcasts"]


    def insert_audio_file(self, file_path, unique_id):
        fs = GridFS(self.db)
        with open(file_path, 'rb') as f:
            try:
                fs.put(f, filename=unique_id, content_type='audio/wav')
            except Exception as e:
                print(f"error occurred when trying to insert file to mongo: {e}")




