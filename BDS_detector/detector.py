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
            with open(path, "r") as file:
                file = file.read()
                decoded_file = base64.b64decode(file).decode('utf-8')
                list =  decoded_file.split(",")
            self.logger.info(f"file {path} loaded and decoded successfully")
            return list
        except FileNotFoundError:
            self.logger.error(f"file {path} was not found")
            raise FileNotFoundError(f"file {path} was not found")
        except Exception as e:
            self.logger.error(f"error occurred during file loading {e}")
            raise Exception(f"error occurred during file loading {e}")


    # TODO: use the capabilities of es to match words and score docs.
    # for now i am making a painless script,
    # that will run on es server/container,
    # in order to reduce the use of this service resources,
    # and to make this service faster
    # ----------------------------------------------------
    # the logic of BDS scoring is to count the black and grey words,
    # when black word count as 1,
    # and grey word count as 1/2.
    # then the counter result will be divided by the amount of the podcast's words
    #-----------------------------------------------------
    # As for the is_bds threshold - in case of pod that have 2 or 3 hours of random talk
    # if this pod have 1 minute of BDS comment
    # i still want to determine this pod as promoting BDS
    # so the threshold going to be low - 4%  for now
    #-----------------------------------------------------
    # AS for the bds_threat_level:
    # bds_percent < 3%  ==> none
    # 3% < bds_percent =< 6%  ==> medium
    # 6% < bds_percent  ==> high
    def detect(self, req):
        pod_id = req["pod_id"]
        body_script = {
            "script": {
                "lang": "painless",
                "source":
                    """
                    String suspicious_text = ctx._source.pod_text.toLowerCase();
                    int word_amount = ctx._source.text_words_count;
                    List black_list = params.black_list;
                    List grey_list = params.grey_list;
                    float counter = 0;
                    for (word in black_list) {
                        if (suspicious_text.contains(word.toLowerCase())) {
                            counter += 1;                                                    
                        }
                    }
                    for (word in grey_list) {
                        if (suspicious_text.contains(word.toLowerCase())) {
                            counter += 0.5;                                                    
                        }
                    }
                    float bds_percent = 100 * counter / word_amount;
                    if(bds_percent > params.bds_threshold){
                        ctx._source.is_bds = true
                    }
                    else{
                        ctx._source.is_bds = false
                    }
                    
                    if(bds_percent < params.bds_medium_threshold){
                        ctx._source.bds_threat_level = "none"
                    }
                    else if(bds_percent < params.bds_none_high){
                            ctx._source.bds_threat_level = "medium"
                        }
                    else{
                        ctx._source.bds_threat_level = "high"
                    }        
                    """,
                "params": {
                    "black_list": self.black_list,
                    "grey_list": self.grey_list,
                    "bds_threshold": 4,
                    "bds_medium_threshold": 3,
                    "bds_none_high": 6,

                }
            }
        }
        self.es_dal.update_doc(pod_id, body_script)



