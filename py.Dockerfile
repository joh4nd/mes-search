
FROM python:3.12-slim-bookworm

WORKDIR /app/src/pipeline

COPY data ../../data/

# install cpu version of torch to not require gpu version by sentence-transformers: https://stackoverflow.com/questions/77205123/how-do-i-slim-down-sberts-sentencer-transformer-library
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# prod
ENTRYPOINT python3 -m data-to-index

# dev
# ENTRYPOINT jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --no-browser
