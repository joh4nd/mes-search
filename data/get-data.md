# get data

__Kaggle isis-twitter-data__

Download the data from Kaggle https://www.kaggle.com/datasets/fifthtribe/how-isis-uses-twitter or with an API key https://www.kaggle.com/docs/api


```python
# Set Kaggle API credentials
os.environ['KAGGLE_USERNAME'] = 'your_kaggle_username'
os.environ['KAGGLE_KEY'] = 'your_kaggle_api_key'

# Download data from Kaggle
!kaggle datasets download -d dataset_name # requires kaggle cli
!unzip dataset_name.zip -d data
```
