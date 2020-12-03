__author__ = "Adam Klekowski"

import yaml
import time
from kafka import KafkaProducer
import cv2
import pickle
import logging
import pafy

logging.basicConfig(level=logging.INFO, format='%(message)s')

time.sleep(30)
class StreamingScraper(object):
    def __init__(self):
        with open("scraper_config.yaml") as yaml_file:
            config_dict = yaml.load(yaml_file)["config_dictionary"]

        self._url = config_dict["url"]
        self.vPafy = pafy.new(self._url)
        self.play = self.vPafy.getbest()
        self.vidcap = cv2.VideoCapture(self.play.url)
        self.sample_period = 1/config_dict['sample_freq_Hz']

        self.producer = KafkaProducer(bootstrap_servers=['kafka:9093'])  

    def start(self):
        capture_time = time.time()
        while True:
            success,image = self.vidcap.read()
            if capture_time<time.time():
                if success:
                    image = cv2.resize(image,(540,360))
                    timestamp = round(time.time(),2)
                    msg = pickle.dumps((timestamp, image))
                    self.producer.send('topictest', msg)
                    logging.info('Frame captured and sent')
                capture_time=self.sample_period+time.time()



if __name__ == "__main__":
    streaming_scraper = StreamingScraper()
    streaming_scraper.start()
