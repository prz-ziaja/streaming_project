__author__ = "Adam Klekowski"

import requests
import yaml


class StreamingScraper(object):
    def __init__(self):
        with open("scraper_config.yaml") as yaml_file:
            config_dict = yaml.load(yaml_file)["config_dictionary"]
            self._url = config_dict["url"]
            self._size = config_dict["size"]

    def start(self, chunk_size=1024):
        saved_bytes = 0
        local_filename = self._url.split('/')[-1]
        with requests.get(self._url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size):
                    f.write(chunk)
                    saved_bytes += chunk_size
                    if saved_bytes >= self._size:
                        return


if __name__ == "__main__":
    streaming_scraper = StreamingScraper()
    streaming_scraper.start()
