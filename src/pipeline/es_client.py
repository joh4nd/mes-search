
import logging
from elasticsearch import Elasticsearch # https://elasticsearch-py.readthedocs.io/en/stable/api/indices.html#elasticsearch.client.IndicesClient.exists
import time
import json
import inspect
from sentence_transformers import SentenceTransformer

logging.basicConfig(level=logging.INFO)

class Search:
    
    def __init__(self):
        """
        Connects to Elasticsearch at host.docker.internal.
        
        Loads vector model.
        """

        self.model = SentenceTransformer('all-MiniLM-L6-v2') # https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/store-embeddings

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
        Deletes and recreates an index

        There will be only one index

        ref: https://elasticsearch-py.readthedocs.io/en/stable/api/indices.html#indices
        """
        
        # while dev: delete and create
        # https://www.elastic.co/guide/en/elasticsearch/reference/current/index-management-settings.html#action.destructive_requires_name
        clsettings = {"persistent": {"action.destructive_requires_name": False}} 
        self.es.cluster.put_settings(body = clsettings)

        # https://elasticsearch-py.readthedocs.io/en/stable/api/indices.html#elasticsearch.client.IndicesClient.delete
        self.es.indices.delete(index = "_all", ignore_unavailable = True)
        
        # https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/store-embeddings
        self.es.indices.create(index = indexname, mappings = {
            'properties': {'embedding': {'type': 'dense_vector'}}})
                
        self.es.indices.exists(index=indexname, pretty=True, human=True)
        logging.info(f'Recreated {indexname}!')
    
    def get_embedding(self, text):
        """Encodes msgs with vector model"""
        return self.model.encode(text)

    def add_documents(self, json_docs=None):
        """
        Index json documents (a dict of key-value fields) with their embeddings in an index named after themselves.

        refs:
         - https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-types.html
         - https://elasticsearch-py.readthedocs.io/en/stable/quickstart.html#indexing-documents
         - https://elasticsearch-py.readthedocs.io/en/stable/api.html#elasticsearch.Elasticsearch.bulk
         - https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/store-embeddings
        """

        # retrieve passed name of json_docs as index_name
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

        # use index_name to set search key
        if index_name == "isis_docs":
                doctype = 'tweets'
        elif index_name == "documents":
                doctype = 'name'
        else:
            pass

        # bulk and dict-unpacking adds docs and embeddings
        operations = []
        for doc in json_docs:
            operations.append({'index': {'_index': index_name}})
            operations.append({**doc,
                               'embedding': self.get_embedding(doc[doctype])})        
        return self.es.bulk(operations=operations)

    def search(self, **query_args):
        """
        Search msgs in the only available index.
        
        Enables vector search and full-text search.

        refs: 
        - https://www.elastic.co/search-labs/tutorials/search-tutorial/vector-search/nearest-neighbor-search
        """

        # Assumes only one index
        # indexname = list(self.es.indices.get_alias(index="*").keys())[0]

        return self.es.search(**query_args)
    
    def retrieve_message(self, id):

        indexname = list(self.es.indices.get_alias(index="*").keys())[0]

        logging.info(f'Retrieving doc {id}...')
        return self.es.get(index=indexname, id=id)
    

