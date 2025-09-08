from gridfs.errors import FileExists
from pymongo import MongoClient
from gridfs import GridFS
from shared.logger import Logger
from shared.config import mongo_uri


class MongoDal:
    def __init__(self):
        client = MongoClient(mongo_uri)
        self.db = client["podcasts"]
        self.logger = Logger.get_logger()
        self.fs = GridFS(self.db)



    def insert_audio_file(self, file_path, unique_id):
        with open(file_path, 'rb') as f:
            try:
                file_id = self.fs.put(f, filename=unique_id, _id=unique_id, content_type='audio/wav')
                self.logger.info(f"file uploaded with with file id: {file_id}")
            except FileExists:
                print(f"the file {file_path} already uploaded into mongodb")
                self.logger.error(f"the file {file_path} already uploaded into mongodb")
            except Exception as e:
                print(f"error occurred when trying to insert file to mongo: {e}")
                self.logger.error(f"error occurred when trying to insert file to mongo: {e}")




