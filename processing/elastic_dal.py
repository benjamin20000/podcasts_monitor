from elasticsearch import Elasticsearch
from shared.logger import Logger
from shared.config import elastic_uri, elastic_metadata_index


class ElasticDal:
    def __init__(self):
        self.es_client = Elasticsearch(elastic_uri)
        self.index_name = elastic_metadata_index
        self.logger = Logger.get_logger()
        self._create_index()


    ## creating the index with schema in es only if index not exits
    def _create_index(self):
        if self.es_client.indices.exists(index=self.index_name):
            return
        mapping = {
            "properties": {
                "MB_size": {"type": "float"},
                "creation_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "last_access_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "last_modification_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "original_file_path": {"type": "text"},
                "current_file_path": {"type": "text"},
                "stt":{"type": "text"}
            }
        }
        self.es_client.indices.create(index=self.index_name, body={"mappings": mapping}, ignore=400)


    def insert_metadata_doc(self, doc, unique_id ):
        try:
            response = self.es_client.index(index=self.index_name, id=unique_id, body=doc)
            self.logger.info(f"new doc inserted into elastic with response: {response}")
            print(response)
        except Exception as e:
            self.logger.error(f"error occurred when trying to insert doc into elastic: {e}")
            print(f"error occurred when trying to insert doc into elastic: {e}")

    def _delete_index(self):
        self.es_client.indices.delete(index=self.index_name, ignore_unavailable=True)
