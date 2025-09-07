from pymongo import MongoClient


class MongoDal:
    def __init__(self):
        uri = "mongodb://localhost:27017/"
        client = MongoClient(uri)
        db = client["podcasts"]
        self.collection = db["audio"]




