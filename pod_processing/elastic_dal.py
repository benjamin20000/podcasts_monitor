from elasticsearch import Elasticsearch, helpers



class ElasticDal:
    def __init__(self):
        self.es_client = Elasticsearch("http://localhost:9200")
        self.index_name = "files_metadata"

    def insert_metadata_doc(self, doc, unique_id ):
        try:
            response = self.es_client.index(index=self.index_name, id=unique_id, body=doc)
            print(response)
        except Exception as e:
            print(f"error occurred when trying to insert doc into elastic: {e}")