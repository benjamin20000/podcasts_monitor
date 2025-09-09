from shared.config import black_list_path, grey_list_path
from shared.logger import Logger
from shared.elastic_dal import ElasticDal
import base64

class Detector:
    def __init__(self):
        self.logger = Logger.get_logger()
        self.es_dal = ElasticDal()
        self.black_list = self.get_list(black_list_path)
        self.grey_list = self.get_list(grey_list_path)


    def get_list(self, path):
        try:
            list = []
            with open(path, "r") as file:
                for line in file:
                    decoded_line = base64.b64decode(line).decode('utf-8')
                    list.append(decoded_line)
            self.logger.info(f"file {path} loaded and decoded successfully")
            return list
        except FileNotFoundError:
            self.logger.error(f"file {path} was not found")
            raise FileNotFoundError(f"file {path} was not found")
        except Exception as e:
            self.logger.error(f"error occurred during file loading {e}")
            raise Exception(f"error occurred during file loading {e}")



    ## create script with the logic of bds fields
    def get_es_script(self):
        return {
            "script": {
                "lang": "painless",
                "source": """
                        ctx._source.bds_percent = 1
                                              # List black_list = params.black_list;
                                              # List grey_list = params.grey_list;                                           
                                              # String text = ctx._source.pod_text.toLowerCase();
                                              # float counter = 0;
                                              # for (word in black_list) {
                                              #     if (text.contains(word.toLowerCase())) {
                                              #       counter +=1                                                      
                                              #     }
                                              # }
                                              #  for (word in grey_list) {
                                              #     if (text.contains(word.toLowerCase())) {
                                              #       counter += 0.5                                                     
                                              #     }
                                              # }
                                              # String[] words = text.split("\\s+"); 
                                              # ctx._source.bds_percent = counter / words.length
                                          """,
                "params": {
                    "black_list": self.black_list,
                    "grey_list": self.grey_list
                }
            }
        }


    def detect(self, pod_id):
        # body_script = self.get_es_script()

        body_script = {
            "script": {
                "lang": "painless",
                "source":
                    """
                    String my_text_field = "aba"
                    int wordCount = 0;
                    wordCount = doc['my_text_field'].value.split(/\s+/).length;


                    """,
                "params": {
                    "text": "aba aba aima",
                    "increment_by": 1,
                    "black_list": self.black_list,
                    "grey_list": self.grey_list
                }

            }
        }

        self.es_dal.update_doc(pod_id, body_script)



