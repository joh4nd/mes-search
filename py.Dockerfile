
FROM python:3.12-slim-bookworm

WORKDIR /app

COPY data data/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ENTRYPOINT jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser
