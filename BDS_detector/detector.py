from shared.config import black_list_path, grey_list_path
from shared.logger import Logger
import base64

class Detector:
    def __init__(self):
        self.logger = Logger.get_logger()


    def get_list(self, path):
        try:
            with open(path, "r") as file:
                file = file.read()
            decoded_file = base64.b64decode(file).decode('utf-8')
            self.logger.info(f"file {path} loaded and decoded successfully")
            return decoded_file
        except Exception as e:
            self.logger.error(f"error occurred during file loading {e}")

    def detect(self):
        black_list = self.get_list(black_list_path)
        grey_list = self.get_list(grey_list_path)
        print(black_list)
        print(grey_list)


        pass