import unittest
import sys
import cv2
import os

my_path = os.path.dirname(os.path.realpath(__file__))
path_to_streaming_project = os.path.dirname(my_path)
sys.path.append(path_to_streaming_project)
sys.path.append(os.path.join(path_to_streaming_project,'streaming-scraper','app'))

from streaming_scraper.app.StreamingScraper import *

url_yt = "https://youtu.be/1EiC9bvVGnk"
url_agh = "http://live.uci.agh.edu.pl/video/stream3.cgi?"

class MyTest(unittest.TestCase):

    def testing_yt_connection(self):
        self.assertEqual(test_connection(url_yt), "passed")

    def testing_stream_connection(self):
        self.assertEqual(test_connection(url_agh), "passed")

if __name__ == '__main__':
    unittest.main()
