
# https://www.elastic.co/search-labs/tutorials/search-tutorial/full-text-search/connect-python

import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)

# class communication(object):

isis = pd.read_csv('./isis-kaggle/tweets.csv', usecols=['username','tweets','time'])

