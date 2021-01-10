__author__ = "Adam Klekowski"

import yaml
import time
from kafka import KafkaProducer
import cv2
import pickle
import logging
import pafy
import pymongo
import numpy as np
import sys
import threading
import os 

logging.basicConfig(level=logging.INFO, format='%(message)s')

path_of_script = os.path.dirname(os.path.realpath(__file__))
config_file = os.path.join(path_of_script,"scraper_config.yaml")
with open(config_file) as yaml_file:
    config_dict = yaml.load(yaml_file)["config_dictionary"]


def init_mongo(mongo_location):
    db = pymongo.MongoClient(
                mongo_location,
                username=config_dict['mongo_user'],
                password=config_dict['mongo_password'],
                authSource=config_dict['mongo_database'],
                authMechanism='SCRAM-SHA-256')[config_dict['mongo_database']]
    
    return db

def init_kafka(kafka_location):
    return KafkaProducer(bootstrap_servers=[kafka_location])

def cam_init(_url):
    try:
        if 'youtu' in _url:
            vPafy = pafy.new(_url)
            play = vPafy.getbest(preftype='mp4')
            vidcap = cv2.VideoCapture(play.url)
        else:
            vidcap = cv2.VideoCapture(_url)
    except Exception as e:
        logging.error(f"Problem occured during establishing connection to camera\n{e.args}")
        return None
    
    return vidcap

def test_connection(_url):
    try:
        vidcap = cam_init(_url)
    except Exception as e:
        return "vidcap initialization problem"
    
    if vidcap is None:
        return "empty vidcap object"
    
    success,image = vidcap.read()
    if not success or image is None:
        return "can not get frame from stream"

    return "passed"

class StreamingScraper(object):
    def __init__(self,mongo_location="mongo1:27017",kafka_location='kafka:9093'):
        self.db = init_mongo(mongo_location)
        try:
            self.db.list_collections()
        except Exception as e:
            logging.error(f"Problem with connection to MongoDB\n{e.args}")
            sys.exit(2)
        self.collection = self.db[config_dict['collection']]
        self.sample_period = 1/config_dict['sample_freq_Hz']
        self.producer = init_kafka(kafka_location)
    

    def start(self,_url,lock,threads):
        capture_time = time.time()
        while _url in threads:
            if capture_time<time.time():
                timestamp = round(time.time(),2)
                vidcap = cam_init(_url)
                if vidcap is None:
                    logging.error(f"can not establish connection {_url}")
                    continue
                success,image = vidcap.read()
                if success:
                    image = cv2.resize(image, (1280,720))
                    id = str(int(timestamp))+f'_{np.random.randint(999):0=3d}'
                    msg = pickle.dumps((id,timestamp,_url))
                    with lock:
                        self.collection.insert({'id':id,'timestamp':timestamp,'photo':pickle.dumps(image)})
                        self.producer.send('topictest', msg)
                    logging.info(f'Frame captured and sent {id} from {_url}')
                capture_time=self.sample_period+time.time()
            time.sleep(0.5)
    

    
    def start_manager(self):
        lock = threading.Lock()
        settings = self.db["app_settings"]
        threads = {}
        while True:
            logging.info(f"running threads {[*threads.keys()]}")
            links = [*settings.find()]
            urls = [i["url"] for i in links]
            current_run_urls = [*threads.keys()]
            for i in current_run_urls:
                if i not in urls:
                    temp = threads[i]
                    del(threads[i])
                    temp.join()
            current_run_urls = [*threads.keys()]
            for i in urls:
                logging.info("checking urls from database")
                if i not in current_run_urls:
                    if test_connection(i)=="passed":
                        threads[i] = threading.Thread(target=self.start,args=(i,lock,threads))
                        threads[i].start()
                        settings.update({"url":i}, {"$set":{"Status":"Up"}})
                    else:
                        settings.delete_many({"url":i})
            time.sleep(10)




        



if __name__ == "__main__":
    streaming_scraper = StreamingScraper()
    streaming_scraper.start_manager()