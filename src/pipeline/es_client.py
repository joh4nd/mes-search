
import logging
from elasticsearch import Elasticsearch # https://elasticsearch-py.readthedocs.io/en/stable/api/indices.html#elasticsearch.client.IndicesClient.exists
import time
import json
import inspect

logging.basicConfig(level=logging.INFO)

class Search:
    
    def __init__(self):
        """connects to Elasticsearch at host.docker.internal"""

        self.es = Elasticsearch('http://host.docker.internal:9200') # https://www.elastic.co/guide/en/elasticsearch/client/python-api/current/config.html#timeouts

        retries=0
        max_retries=12
        delay=10
        
        while retries < max_retries:
            try:
                # time.sleep(10)
                client_info = self.es.info()
                logging.info("Connected to Elasticsearch!")
                logging.info(json.dumps(client_info.body, indent = 4))
                break
            except Exception as e:
                time.sleep(delay)
                retries += 1
                logging.info(f"Waiting {retries}/{max_retries} {delay} more seconds for Elasticsearch...")
                if retries == max_retries:
                    raise e

    def create_index(self, indexname=None):
        """
        Deletes and recreates my_index

        my_index is the only index

        ref: https://elasticsearch-py.readthedocs.io/en/stable/api/indices.html#indices
        """

        # while dev
        self.es.indices.delete(index=indexname, ignore_unavailable=True)
        self.es.indices.create(index=indexname)
        
        self.es.indices.exists(index=indexname, pretty=True, human=True)
        logging.info('Recreated my_index!')
    
    def add_documents(self, json_docs=None):
        """
        Index json documents (a dict of key-value fields) in an index named after themselves.
        
        "Fields that have a string value are automatically indexed for full-text and keyword search, but in addition to strings you can use other field types such as numbers, dates and booleans, which are also indexed for efficient operations such as filtering."

        refs:
         - https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html
         - https://elasticsearch-py.readthedocs.io/en/stable/quickstart.html#indexing-documents
        """

        frame = inspect.currentframe()
        frame = inspect.getouterframes(frame)[1]
        string = inspect.getframeinfo(frame[0]).code_context[0].strip()
        del frame
        args = string[string.find('(') + 1:-1].split(',')
        del string
        for arg in args:
            if arg.find('docs') != -1:
                index_name = arg.split('=')[1].strip()
            else:
                pass
        del args

        self.create_index(index_name)

        #self.es.index(index=index, body=json_docs)

        # https://elasticsearch-py.readthedocs.io/en/stable/api.html#elasticsearch.Elasticsearch.bulk
        operations = []
        for doc in json_docs:
            operations.append({'index': {'_index': index_name}})
            operations.append(doc)        
        return self.es.bulk(operations=operations)

    # @app.cli.command()
    # def reindex():
    #     pass