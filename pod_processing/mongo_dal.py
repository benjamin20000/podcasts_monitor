from pymongo import MongoClient
from gridfs import GridFS
import os


class MongoDal:
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        self.db = client["podcasts"]
        # self.collection = db["audio"]


    def insert_audio_file(self, file_path, unique_id):
        fs = GridFS(self.db)
        with open(file_path, 'rb') as f:
            file_id = fs.put(f, filename=unique_id, content_type='audio/wav')
            print(f"File '{unique_id}' stored with ID: {file_id}")




