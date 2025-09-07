import os
# from importlib.metadata import files
from dotenv import load_dotenv
from pathlib import Path


class PodPreProcess:
    def __init__(self):
        self.files = []

    def get_files_in_directory(self):
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
        file_stats = file_path.stat()

        result["mb_size"] =  self.bytes_to_megabytes(file_stats.st_size)
        print(result)

        print(file_stats.st_mode)

    def bytes_to_megabytes(self, bytes_value):
        megabytes = bytes_value / (1024 * 1024)
        return megabytes





