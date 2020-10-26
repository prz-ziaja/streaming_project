__author__ = "Adam Klekowski"

import yaml
import time
from kafka import KafkaProducer
import cv2
import pickle
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

class StreamingScraper(object):
    def __init__(self):
        with open("scraper_config.yaml") as yaml_file:
            config_dict = yaml.load(yaml_file)["config_dictionary"]
            self._url = config_dict["url"]
            self.vidcap = cv2.VideoCapture(self._url)
            self.sample_period = 1/config_dict['sample_freq_Hz']
            self.producer = KafkaProducer(bootstrap_servers=['kafka:9093'])  

    def start(self):
        while True:
            success,image = self.vidcap.read()
            if success:
                timestamp = round(time.time(),2)
                msg = pickle.dumps((timestamp, image))
                self.producer.send('topic_test', msg)
                logging.info('Frame captured and sent')
                time.sleep(self.sample_period)


if __name__ == "__main__":
    streaming_scraper = StreamingScraper()
    streaming_scraper.start()
