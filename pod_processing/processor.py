import os
from dotenv import load_dotenv
from elastic_dal import ElasticDal
from mongo_dal import MongoDal
class Processor:
    def __init__(self):
        self.elastic_dal = ElasticDal()
        self.mongo_dal = MongoDal()

    ##rename the file with the unique_id
    def rename_file(self, unique_id, file_path):
        file_name, file_format = os.path.splitext(file_path)
        directory_path = os.getenv("podcasts_dir")
        new_path = f"{directory_path}/{unique_id}{file_format}"
        try:
            os.rename(file_path, new_path)
        except Exception as e:
            print(f"error occurred when trying to rename {file_path} file: {e}")
        return new_path

    ## -- the combination of the device id with the inode number
    ## -- are uniquely identifying any file
    def create_unique_id(self, metadata):
        return f"{metadata["device_id"]}{metadata["inode"]}"


    ## with the new unique_id some updates are necessary
    ## 1. after we have unique_id we will save hime in the metadata
    ## 2. the new file name/path
    def update_metadata(self, unique_id, new_path, metadata):
        metadata["unique_id"] = unique_id
        metadata["current_path"] = new_path


    def process(self, metadata):
        unique_id = self.create_unique_id(metadata)
        new_path = self.rename_file(unique_id, metadata["original_file_path"])
        self.update_metadata(unique_id, new_path, metadata)
        self.elastic_dal.insert_metadata_doc(metadata, unique_id)
        self.mongo_dal.insert_audio_file(new_path, unique_id)




