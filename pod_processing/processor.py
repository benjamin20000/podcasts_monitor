import os
from dotenv import load_dotenv
from elastic_dal import ElasticDal

class Processor:
    def __init__(self):
        self.elastic_dal = ElasticDal()


    def rename_file(self, unique_id, file_path):
        file_name, file_format = os.path.splitext(file_path)
        directory_path = os.getenv("podcasts_dir")
        new_name = f"{directory_path}/{unique_id}{file_format}"
        os.rename(file_path, new_name)

    ## -- the combination of the device id with the inode number
    ## -- are uniquely identifying any file
    def create_unique_id(self, message):
        return f"{message["device_id"]}{message["inode"]}"


    def process(self, message):
        unique_id = self.create_unique_id(message)
        self.rename_file(unique_id, message["file_path"])
        self.elastic_dal.insert_metadata_doc(message, unique_id)




