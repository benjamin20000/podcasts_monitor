import os
from dotenv import load_dotenv

class PodLoader:
    def get_files_in_directory(self, directory_path):
        load_dotenv()
        pod_dir = os.getenv("podcasts_dir")
        files = []
        for entry in os.listdir(directory_path):
            full_path = os.path.join(directory_path, entry)
            if os.path.isfile(full_path):
                files.append(entry)
        return files

