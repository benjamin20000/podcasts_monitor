import os
from shared.elastic_dal import ElasticDal
from shared.mongo_dal import MongoDal
from shared.logger import Logger
import speech_recognition as sr
from shared.kafka_producer import Producer
from shared.config import stt_kafka_topic

class Processor:
    def __init__(self):
        self.elastic_dal = ElasticDal()
        self.mongo_dal = MongoDal()
        self.logger = Logger.get_logger()
        self.sudio_recognize = sr.Recognizer()
        self.kafka_producer = Producer()


    ##rename the file with the unique_id
    def rename_file(self, unique_id, file_path):
        file_name, file_format = os.path.splitext(file_path)
        directory_path = os.getenv("podcasts_dir")
        new_path = f"{directory_path}/{unique_id}{file_format}"
        try:
            os.rename(file_path, new_path)
            self.logger.info(f"file {file_path} rename to {new_path}")
        except Exception as e:
            self.logger.error(f"error occurred when trying to rename {file_path} file: {e}")
            print(f"error occurred when trying to rename {file_path} file: {e}")
        return new_path


    ## -- the combination of the device id with the inode number
    ## -- are uniquely identifying any file
    def create_unique_id(self, metadata):
        return f"{metadata["device_id"]}{metadata["inode"]}"


    ## with the new unique_id some updates are necessary
    ## 1. after we have unique_id we will save hime in the metadata
    ## 2. the new file name/path
    ## 3. delete the inode and device id unnecessary fields
    def update_metadata(self, unique_id, new_path, metadata):
        metadata["unique_id"] = unique_id
        metadata["current_path"] = new_path
        del metadata["inode"]
        del metadata["device_id"]


    ## use kafka for producing a request of a stt service
    def req_stt_service(self, unique_id):
        req = {"unique_id": unique_id}
        self.kafka_producer.produce(req, stt_kafka_topic)


    def process(self, metadata):
        unique_id = self.create_unique_id(metadata)
        new_path = self.rename_file(unique_id, metadata["original_file_path"])
        self.update_metadata(unique_id, new_path, metadata)
        self.elastic_dal.insert_metadata_doc(metadata, unique_id)
        self.mongo_dal.upload_file(new_path, unique_id)




