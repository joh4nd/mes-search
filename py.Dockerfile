
FROM python:3.12.2

WORKDIR /app

COPY src/es_client.py src/es_client.py
COPY search-index.ipynb search-index.ipynb
COPY data data/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

CMD jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser