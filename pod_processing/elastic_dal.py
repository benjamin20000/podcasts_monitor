from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os


class ElasticDal:
    def __init__(self):
        load_dotenv()
        uri = os.getenv("elastic_uri")
        self.es_client = Elasticsearch(uri)
        self.index_name = "files_metadata"

    def insert_metadata_doc(self, doc, unique_id ):
        try:
            response = self.es_client.index(index=self.index_name, id=unique_id, body=doc)
            print(response)
        except Exception as e:
            print(f"error occurred when trying to insert doc into elastic: {e}")