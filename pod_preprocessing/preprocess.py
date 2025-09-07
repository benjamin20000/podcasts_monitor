import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
from kafka_producer import Producer

class PodPreProcess:
    def __init__(self):
        self.files = []


    def load_files_from_dir(self):
        load_dotenv()
        directory_path = os.getenv("podcasts_dir")
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                self.files.append(f"{directory_path}/{entry}")


    def rename_files(self):
        load_dotenv()
        directory_path = os.getenv("podcasts_dir")
        for file_inx in range(len(self.files)):
            file_name, file_format = os.path.splitext(self.files[file_inx])
            old_name = f"{file_name}{file_format}"
            new_name = f"{directory_path}/file_number_{file_inx}{file_format}"
            os.rename(old_name, new_name)


    def parse_file(self, path):
        result = {}
        file_path = Path(path)
        file_stats = file_path.stat() #get statistic of the file
        result["file_path"] = path
        print(file_stats)
        result["MB_size"] =  self.bytes_to_megabytes(file_stats.st_size)
        result["creation_time"] = self.unix_timestamp_to_datetime(file_stats.st_ctime)
        result["last_access_time"] = self.unix_timestamp_to_datetime(file_stats.st_atime)
        result["last_modification_time"] = self.unix_timestamp_to_datetime(file_stats.st_mtime)

        ##------  2 more fields needed letter for the unique id ------
        result["inode"] = self.unix_timestamp_to_datetime(file_stats.st_mtime)
        result["device_id"] = self.unix_timestamp_to_datetime(file_stats.st_dev)
        return result


    def unix_timestamp_to_datetime(self, unix_timestamp ):
        return datetime.fromtimestamp(unix_timestamp).strftime('%Y-%m-%d %H:%M:%S')


    def bytes_to_megabytes(self, bytes_value):
        megabytes = bytes_value / (1024 * 1024)
        return megabytes


    def preprocess(self):
        kafka_producer = Producer()
        self.load_files_from_dir()
        for file in self.files:
            metadata = self.parse_file(file)
            kafka_producer.produce(metadata)













