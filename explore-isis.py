
import pandas as pd

isis = pd.read_csv('./isis-kaggle/tweets.csv', usecols=['username','tweets','time']) 

# consider regex rm escape characters e.g. \n
