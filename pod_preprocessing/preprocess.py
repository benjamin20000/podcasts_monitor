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





