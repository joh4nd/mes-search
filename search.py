
# requires local ES running e.g. in Docker

import logging
from elasticsearch import Elasticsearch #, helpers
from pprint import pprint
import pandas as pd
import json
import certifi
certifi.where()
from ssl import create_default_context

logging.basicConfig(level=logging.INFO)


isis = pd.read_csv('./data/tweets.csv', usecols=['username','tweets','time']) 
isis = isis.to_dict(orient='records')


# context = create_default_context(cafile = "")
es_client = Elasticsearch(["https://elastic:OVrhW0=_cH_vMh_vW1w-@localhost:9200"],
                          ca_certs='/etc/elasticsearch/certs/http_ca.crt') #,
                          # verify_certs=False) # requires ES in Docker
es_client.info()
es_client_info = es_client.info()

logging.info("Connected to Elasticsearch!")
pprint(es_client_info.body)

es_client.indices.create(index="tweets")
es_client.index(index="tweets", body=isis)


test = Elasticsearch(['https://localhost:9200'],basic_auth=('elastic', 'OVrhW0=_cH_vMh_vW1w-'), ca_certs='/etc/elasticsearch/certs/http_ca.crt')
test.info()

# class Search(object):

#     def __init__(self):
#         """ https://www.elastic.co/search-labs/tutorials/search-tutorial/full-text-search/connect-python """
        
#         self.es = Elasticsearch("http://localhost:9200") # local service via Docker
#         client_info = self.es.info()
#         logging.info("Connected to Elasticsearch!")
#         pprint(client_info.body)


#     def create_index(self, index_name='my_documents'):
#         """ https://www.elastic.co/search-labs/tutorials/search-tutorial/full-text-search/create-index """

#         self.es.indices.delete(index=index_name, ignore_unavailable=True) # useful during dev
#         self.es.indices.create(index=index_name)

#     def insert_documents(self, document):
#         """
#         https://www.elastic.co/search-labs/tutorials/search-tutorial/full-text-search/create-index#add-documents-to-the-index

#         Documents are the data
#         """
#         return self.es.index(index=self.index_name, body=document)



# # index isis
# isis = pd.read_csv('./data/tweets.csv', usecols=['username','tweets','time']) 
# isis = isis.to_dict(orient='records')
# es_client = Search()
# es_client.create_index('communication') # es_client.es.indices.
# es_client.insert_documents(index='communication', body=isis) # es_client.es.index(index='communication', body=isis)

