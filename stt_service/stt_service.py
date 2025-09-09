import speech_recognition as sr
from shared.logger import Logger
from shared.mongo_dal import MongoDal
from shared.config import temp_folder_path
from shared.elastic_dal import ElasticDal
import os


class SttService:
    def __init__(self):
        self.audio_recognize = sr.Recognizer()
        self.logger = Logger.get_logger()
        self.mongo_dal = MongoDal()
        self.elastic_dal = ElasticDal()


    def download_audio(self, file_id):
        try:
            audio_bytes = self.mongo_dal.load_file(file_id)
            file_temp_path = f"{temp_folder_path}{file_id}.wav"
            with open(file_temp_path, "wb") as file:
                file.write(audio_bytes)
            self.logger.info(f"file {file_temp_path} has been temporarily downloaded")
            return file_temp_path
        except Exception as e:
            self.logger.info(f"error occurred when trying to download audio file: {e}")


    def stt_logic(self, file_path, file_id):
        try:
            audiofile = sr.AudioFile(file_path)
            with audiofile as source:
                audio = self.audio_recognize.record(source)
                text = self.audio_recognize.recognize_google(audio)
                self.logger.info(f"file {file_id} has been converted to text")
                return text
        except Exception as e:
            self.logger.error(f"file {file_id} convertion to text hase been failed")


    def remove_file(self, temp_file_path):
        try:
            os.remove(temp_file_path)
            self.logger.info(f"file {temp_file_path} has been removed successfully")
        except Exception as e:
            self.logger.error(f"error occurred when trying to remove file: {e}")


    ## -- update the metadata in elastic using elastic dal
    ## -- with the new stt text
    def update_metadata(self, doc_id, text):
        update_body = {
            "doc": {
                "stt": text
            }
        }
        self.elastic_dal.update_doc(doc_id, update_body)


    def stt(self, file_id):
        temp_file_path = self.download_audio(file_id)
        text = self.stt_logic(temp_file_path, file_id)
        self.remove_file(temp_file_path)
        self.update_metadata(file_id, text)
        # return text