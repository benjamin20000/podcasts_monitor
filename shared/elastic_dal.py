from elasticsearch import Elasticsearch
from shared.logger import Logger
from shared.config import elastic_uri, elastic_metadata_index


class ElasticDal:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.es_client = self.create_connection()
        self.index_name = elastic_metadata_index
        self._create_index()


    def create_connection(self):
        es_client = Elasticsearch(elastic_uri)
        if es_client.ping():
            self.logger.info(f"connection establish to es")
            return es_client
        else:
            self.logger.error(f"cant connect to es")
            raise


    ## creating the index with schema in es only if index not exits
    ## this mapping needed especially for all date types
    ## to make sure es will not to save them as a string
    def _create_index(self):
        if self.es_client.indices.exists(index=self.index_name):
            return
        mapping = {
            "properties": {
                "bytes_size": {"type": "integer"},
                "creation_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "last_access_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "last_modification_time": {"type": "date", "format": "yyyy-MM-dd HH:mm:ss"},
                "original_file_path": {"type": "text"},
                "current_file_path": {"type": "text"},
                "pod_text":{"type": "text"},
            }
        }
        self.es_client.indices.create(index=self.index_name, body={"mappings": mapping}, ignore=400)


    def insert_metadata_doc(self, doc, unique_id):
        try:
            response = self.es_client.index(index=self.index_name, id=unique_id, body=doc)
            self.logger.info(f"new doc inserted into elastic with response: {response}")
            print(response)
        except Exception as e:
            self.logger.error(f"error occurred when trying to insert doc into elastic: {e}")
            print(f"error occurred when trying to insert doc into elastic: {e}")


    def update_doc(self, doc_id, update_body):
        try:
            response = self.es_client.update(index=self.index_name, id=doc_id, body=update_body)
            self.logger.info(f"elastic doc hase been updated with response: {response}")
        except Exception as e:
            self.logger.error(f"error occurred when trying to update a doc: {e}")


    def _delete_index(self):
        self.es_client.indices.delete(index=self.index_name, ignore_unavailable=True)


