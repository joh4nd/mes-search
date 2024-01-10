# mes-search: message search

A project enabling vector search of isis messages

## Kaggle isis-twitter-data

The data are downloaded from Kaggle: https://www.kaggle.com/datasets/fifthtribe/how-isis-uses-twitter

The data can also be downloaded with an API key: https://www.kaggle.com/docs/api

```python
# Set Kaggle API credentials
os.environ['KAGGLE_USERNAME'] = 'your_kaggle_username'
os.environ['KAGGLE_KEY'] = 'your_kaggle_api_key'

# Download data from Kaggle
!kaggle datasets download -d dataset_name
!unzip dataset_name.zip -d data
```
