import unittest
import sys
import cv2
import os
import pymongo
import pickle
import numpy as np
from kafka import KafkaConsumer
import time

my_path = os.path.dirname(os.path.realpath(__file__))
path_to_streaming_project = os.path.dirname(my_path)
sys.path.append(path_to_streaming_project)
sys.path.append(os.path.join(path_to_streaming_project,'streaming-scraper','app'))

from streaming_scraper.app.StreamingScraper import *

url_yt = "https://youtu.be/1EiC9bvVGnk"
url_agh = "http://live.uci.agh.edu.pl/video/stream3.cgi?"
number = np.random.randint(100000)

class MyTest(unittest.TestCase):
    def testing_01_yt_cam_init(self):
        res = cam_init(url_yt)
        self.assertEqual(res.isOpened(),True)

    def testing_02_agh_cam_init(self):
        res = cam_init(url_agh)
        self.assertEqual(res.isOpened(),True)

    def testing_03_yt_connection(self):
        self.assertEqual(test_connection(url_yt), "passed")

    def testing_04_stream_connection(self):
        self.assertEqual(test_connection(url_agh), "passed")

    def testing_05_mongo_connection(self):
        db = init_mongo('localhost:27017')
        collections=set([*db.list_collection_names()])
        expected = set(['photos', 'labels_comments', 'app_settings'])
        self.assertEqual(collections,expected)

    def testing_06_mongo_input(self):
        db = init_mongo('localhost:27017')
        collection = db['labels_comments']
        collection.insert_one({"test":number})
        print(f"###############{number}")
        self.assertEqual(bool([*collection.find({
            "test":number})]),True)

    def testing_07_mongo_delete(self):
        db = init_mongo('localhost:27017')
        collection = db['labels_comments']

        found_num_befor_del = bool([*collection.find(
            {"test":number})])

        collection.delete_many({"test":number})
 
        found_num_after_del = bool([*collection.find(
            {"test":number})])

        self.assertEqual((found_num_befor_del and
         not found_num_after_del),True)
    
    def testing_08_kafka_init(self):
        init_without_errors = True
        try:
            producer = init_kafka('localhost:9092')
        except Exception as e:
            print(e.args)
            init_without_errors = False
        self.assertEqual(init_without_errors,True)

    def testing_09_kafka_connection(self):
        producer = init_kafka('localhost:9092')
        consumer = KafkaConsumer(
            'test',
            bootstrap_servers=['localhost:9092'],
                  auto_offset_reset='earliest',
      enable_auto_commit=True,
            consumer_timeout_ms=1000
        )

        producer.send('test',pickle.dumps(number))
        got_number = False
        for i in consumer:
            if pickle.loads(i.value)==number:
                got_number = True
                break
        
        self.assertEqual(got_number,True)


    def testing_10_initialization(self):
        init_without_errors = True
        try:
            StreamingScraper("localhost:27017",'localhost:9092')
        except Exception as e:
            print(e.args)
            init_without_errors = False
        self.assertEqual(init_without_errors,True)


if __name__ == '__main__':
    mongo_up_command = ("docker-compose -f " +  
        os.path.join(path_to_streaming_project,
        'docker-compose.yaml') +
        " up -d mongo1 kafka")

    os.system("docker stop mongo1 kafka zookeeper")
    os.system("docker rm mongo1 kafka zookeeper")
    os.system(mongo_up_command)

    time.sleep(5)
    unittest.main()

    os.system("docker stop mongo1 kafka zookeeper")
    os.system("docker rm mongo1 kafka zookeeper")
