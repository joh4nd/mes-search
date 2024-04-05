
FROM python:3.12-slim-bookworm

WORKDIR /app/src/pipeline

COPY data ../../data/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ENTRYPOINT python3 -m data-to-index

# ENTRYPOINT jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser
