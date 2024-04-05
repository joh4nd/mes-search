
import logging
import pandas as pd
from es_client import Search

logging.basicConfig(level=logging.INFO)

isis = pd.read_csv('../../data/tweets.csv', usecols=['username','tweets','time'])

isis_docs = isis.to_dict(orient='records')

es = Search()

es.add_documents(json_docs=isis_docs)

