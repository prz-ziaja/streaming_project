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

logging.basicConfig(level=logging.INFO, format='%(message)s')

#time.sleep(30)
class StreamingScraper(object):
    def __init__(self):
        with open("scraper_config.yaml") as yaml_file:
            config_dict = yaml.load(yaml_file)["config_dictionary"]

        self._url = config_dict["url"]
        self.cam_init()

        self.db = pymongo.MongoClient(
                    'mongo1:27017',
                    username=config_dict['mongo_user'],
                    password=config_dict['mongo_password'],
                    authSource=config_dict['mongo_database'],
                    authMechanism='SCRAM-SHA-256')[config_dict['mongo_database']]
        try:
            self.db.list_collections()
        except Exception as e:
            logging.error(f"Problem with connection to MongoDB\n{e.args}")
            sys.exit(2)
        self.collection = self.db[config_dict['collection']]
        self.sample_period = 1/config_dict['sample_freq_Hz']
        self.producer = KafkaProducer(bootstrap_servers=['kafka:9093'])  
    
    def cam_init(self):
        try:
            if 'youtu' in self._url:
                self.vPafy = pafy.new(self._url)
                self.play = self.vPafy.getbest(preftype='mp4')
                self.vidcap = cv2.VideoCapture(self.play.url)
            else:
                self.vidcap = cv2.VideoCapture(self._url)
        except Exception as e:
            logging.error(f"Problem occured during establishing connection to camera\n{e.args}")
            sys.exit(1)

    def start(self):
        capture_time = time.time()
        while True:
            if capture_time<time.time():
                timestamp = round(time.time(),2)
                self.cam_init()
                success,image = self.vidcap.read()
                if success:
                    image = cv2.resize(image, (1280,720))
                    id = str(int(timestamp))+f'_{np.random.randint(999):0=3d}'
                    msg = pickle.dumps((id,timestamp))
                    self.collection.insert({'id':id,'timestamp':timestamp,'photo':pickle.dumps(image)})
                    self.producer.send('topictest', msg)
                    logging.info('Frame captured and sent')
                capture_time=self.sample_period+time.time()



if __name__ == "__main__":
    streaming_scraper = StreamingScraper()
    streaming_scraper.start()