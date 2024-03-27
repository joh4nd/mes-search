
import logging
from elasticsearch import Elasticsearch
import json

logging.basicConfig(level=logging.INFO)

# https://www.elastic.co/search-labs/tutorials/search-tutorial/full-text-search/connect-python#connect-to-a-self-hosted-elasticsearch-docker-container

class Search:
    def __init__(self):
        self.es = Elasticsearch('http://172.19.0.3:9200') # docker inspect mes-search-es-client-1
        client_info = self.es.info()
        logging.info("Connected to Elasticsearch!")
        logging.info(json.dumps(client_info.body, indent = 4))

