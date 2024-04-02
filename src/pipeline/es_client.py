
import logging
from elasticsearch import Elasticsearch
import time
import json

logging.basicConfig(level=logging.INFO)

class Search:
    def __init__(self):

        self.es = Elasticsearch('http://host.docker.internal:9200')

        retries=0
        max_retries=12
        
        while retries < max_retries:
            try:
                # time.sleep(10)
                client_info = self.es.info()
                logging.info("Connected to Elasticsearch!")
                logging.info(json.dumps(client_info.body, indent = 4))
                break
            except Exception as e:
                time.sleep(10)
                retries += 1
                logging.info(f"Waiting {retries}/{max_retries} 10 more seconds for Elasticsearch...")
                if retries == max_retries:
                    raise e


# https://www.elastic.co/search-labs/tutorials/search-tutorial/full-text-search/connect-python#connect-to-a-self-hosted-elasticsearch-docker-container
# https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/config.html#timeouts
# https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-health.html
# https://elasticsearch-py.readthedocs.io/en/v8.13.0/async.html

      
