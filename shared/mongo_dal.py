from gridfs.errors import FileExists
from pymongo import MongoClient, errors
from gridfs import GridFS
from pymongo.errors import ServerSelectionTimeoutError

from shared.logger import Logger
from shared.config import mongo_uri


class MongoDal:
    def __init__(self):
        self.logger = Logger.get_logger()
        client = self.create_connection()
        self.db = client["podcasts"]
        self.fs = GridFS(self.db)


    def create_connection(self):
        try:
            client = MongoClient(mongo_uri)
            client.server_info()
            self.logger.info(f"connection establish to mongo")
            return client
        except ServerSelectionTimeoutError as e:
            self.logger.error(f"error occurred when trying to connect to mongo {e}")
            raise ServerSelectionTimeoutError("No MongoDB servers found within the specified timeout.")


    def upload_file(self, file_path, unique_id):
        with open(file_path, 'rb') as f:
            try:
                file_id = self.fs.put(f, filename=unique_id, _id=unique_id, content_type='audio/wav')
                self.logger.info(f"file uploaded with with file id: {file_id}")
            except FileExists:
                self.logger.error(f"the file {file_path} already uploaded into mongodb")
            except Exception as e:
                self.logger.error(f"error occurred when trying to insert file to mongo: {e}")


    def load_file(self, file_id):
        try:
            file = self.fs.get(file_id).read()
            self.logger.info(f"file {file_id} hase been load from mongo")
            return file
        except Exception as e:
            self.logger.error(f"error occurred when trying to load the file from mongo: {e}")
            return None





