import os
from pathlib import Path
from datetime import datetime
from kafka_producer import Producer
from shared.logger import Logger
from shared.config import directory_path

class PodPreProcess:
    def __init__(self):
        self.files = []
        self.logger = Logger.get_logger()


    def _load_files_from_dir(self):
        try:
            for entry in os.listdir(directory_path):
                full_path = os.path.join(directory_path, entry)
                if os.path.isfile(full_path):
                    self.files.append(f"{directory_path}/{entry}")
            self.logger.info(f"the directory {directory_path} loaded successfully")
        except Exception as e:
            self.logger.error(f"error occurred when trying to insert load {directory_path} folder: {e}")


    def _parse_file(self, path):
        result = {}
        file_path = Path(path)
        file_stats = file_path.stat() #get statistic of the file
        result["bytes_size"] =  file_stats.st_size
        result["creation_time"] = self._unix_timestamp_to_datetime(file_stats.st_ctime)
        result["last_access_time"] = self._unix_timestamp_to_datetime(file_stats.st_atime)
        result["last_modification_time"] = self._unix_timestamp_to_datetime(file_stats.st_mtime)
        ## 2 fields for path needed
        ## 1. original path - not going to change
        ## 2. for current file path - could change
        result["original_file_path"] = path
        result["current_file_path"] = path

        ##------  3 more fields needed letter (next service) for the unique id ------
        result["unique_id"] = None
        result["inode"] = file_stats.st_ino
        result["device_id"] = file_stats.st_dev
        return result


    def _unix_timestamp_to_datetime(self, unix_timestamp ):
        return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')


    def preprocess(self):
        kafka_producer = Producer()
        self._load_files_from_dir()
        for file in self.files:
            metadata = self._parse_file(file)
            kafka_producer.produce(metadata)













