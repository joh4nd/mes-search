
import logging
from elasticsearch import Elasticsearch
import json

logging.basicConfig(level=logging.INFO)

class Search:
    def __init__(self):
        self.es = Elasticsearch('http://host.docker.internal:9200')
        #, retry_on_timeout=True) 
        #, http_compress=True)
        #, request_timeout=30)
        client_info = self.es.info()
        logging.info("Connected to Elasticsearch!")
        logging.info(json.dumps(client_info.body, indent = 4))


# https://www.elastic.co/search-labs/tutorials/search-tutorial/full-text-search/connect-python#connect-to-a-self-hosted-elasticsearch-docker-container
# https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/config.html#timeouts
# https://www.elastic.co/guide/en/elasticsearch/reference/current/cat-health.html
# https://elasticsearch-py.readthedocs.io/en/v8.13.0/async.html