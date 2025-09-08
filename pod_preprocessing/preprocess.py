import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from kafka_producer import Producer

class PodPreProcess:
    def __init__(self):
        self.files = []


    def _load_files_from_dir(self):
        load_dotenv()
        directory_path = os.getenv("podcasts_dir")
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                self.files.append(f"{directory_path}/{entry}")


    def _parse_file(self, path):
        result = {}
        file_path = Path(path)
        file_stats = file_path.stat() #get statistic of the file
        result["MB_size"] =  self._bytes_to_megabytes(file_stats.st_size)
        result["creation_time"] = self._unix_timestamp_to_datetime(file_stats.st_ctime)
        result["last_access_time"] = self._unix_timestamp_to_datetime(file_stats.st_atime)
        result["last_modification_time"] = self._unix_timestamp_to_datetime(file_stats.st_mtime)
        ##---- the *original* in the field name because later the file name will change
        result["original_file_path"] = path
        ##------  2 more fields needed letter for the unique id ------
        result["inode"] = file_stats.st_ino
        result["device_id"] = file_stats.st_dev
        return result


    def _unix_timestamp_to_datetime(self, unix_timestamp ):
        return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')


    def _bytes_to_megabytes(self, bytes_value):
        megabytes = bytes_value / (1024 * 1024)
        return megabytes


    def preprocess(self):
        kafka_producer = Producer()
        self._load_files_from_dir()
        for file in self.files:
            metadata = self._parse_file(file)
            kafka_producer.produce(metadata)













