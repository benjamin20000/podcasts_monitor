from elasticsearch import Elasticsearch
from shared.logger import Logger
from shared.config import elastic_uri


class ElasticDal:
    def __init__(self):
        self.es_client = Elasticsearch(elastic_uri)
        self.index_name = "files_metadata"
        self.logger = Logger.get_logger()

    def insert_metadata_doc(self, doc, unique_id ):
        try:
            response = self.es_client.index(index=self.index_name, id=unique_id, body=doc)
            self.logger.info(f"new doc inserted into elastic with response: {response}")
            print(response)
        except Exception as e:
            self.logger.errpr(f"error occurred when trying to insert doc into elastic: {e}")
            print(f"error occurred when trying to insert doc into elastic: {e}")