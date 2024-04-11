
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
        
        # https://www.elastic.co/search-labs/tutorials/search-tutorial/semantic-search/elser-model
        self.es.indices.create(index = indexname, mappings = {
            'properties': {'embedding': {'type': 'dense_vector'}, # vector
                           'elser_embedding': {'type': 'sparse_vector'}}}, # semantic
                           settings = {'index': {'default_pipeline': 'elster-ingest-pipeline'}}) # see deploy_elser()
                
        self.es.indices.exists(index=indexname, pretty=True, human=True)
        logging.info(f'Recreated {indexname}!')
    
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

    def search(self, **query_args):
        """
        Search the only available index
        
        Combines sematic/vector with full-text search

        refs: 
        https://www.elastic.co/search-labs/tutorials/search-tutorial/semantic-search/hybrid-search
        """
        
        if 'from_' in query_args:
            query_args['from'] = query_args['from_']
            del query_args['from_']

        # Assumes only one index
        indexname = list(self.es.indices.get_alias(index="*").keys())[0]

        return self.es.perform_request(
            'GET',
            f'/{indexname}/_search',
            body = json.dumps(query_args),
            headers = {'Content-Type': 'application/json',
                       'Accept': 'application/json'}
        )

    
    def retrieve_message(self, id):

        indexname = list(self.es.indices.get_alias(index="*").keys())[0]

        logging.info(f'Retrieving doc {id}...')
        return self.es.get(index=indexname, id=id)
    

    def deploy_elser(self):
        """
        Vectorize documents when added.

        Model name: .elser_model_2

        Pipeline name: elser-ingest-pipeline

        Pipeline runs on field doctype (tweets/name) and outputs to the elser_embedding field
        """

        logging.info('Loading elser model...')
        self.es.ml.put_trained_model(model_id = '.elser_model_2',
                                     input = {'field_names': ['text_field']})
        
        while True:
            status = self.es.ml.get_trained_models(model_id = '.elser_model_2',
                                                   include = 'definition_status')
            if status['trained_model_configs'][0]['fully_defined']:
                break
            time.sleep(1) # asynchronous thus sleep
        
        logging.info('Deploying elser model...')
        self.es.ml.start_trained_model_deployment(model_id = '.elser_model_2')

        indexname = list(self.es.indices.get_alias(index="*").keys())[0]
        if indexname == "isis_docs":
            doctype = 'tweets'
        elif indexname == "documents":
            doctype = 'name'
        else:
            pass

        logging.info('Pipe docs through elser model to create embeddings...')
        self.es.ingest.put_pipeline(id = 'elser-ingest-pipeline',
                                    processors = [{'inference':
            {'model_id': '.elser_model_2',
            'input_output': [{'input_field': doctype,
                              'output_field': 'elser_embedding'}]}}])
        
        logging.info('Elser done!!!')
