from pymongo import MongoClient
from gridfs import GridFS
import os


class MongoDal:
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        self.db = client["podcasts"]


    def insert_audio_file(self, file_path, unique_id):
        fs = GridFS(self.db)
        with open(file_path, 'rb') as f:
            try:
                fs.put(f, filename=unique_id, content_type='audio/wav')
            except Exception as e:
                print(f"error occurred when trying to insert file to mongo: {e}")




