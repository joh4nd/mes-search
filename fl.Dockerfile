
FROM python:3.12.2-slim-bookworm

WORKDIR /app/src/gui-search

ENV PYTHONPATH "${PYTHONPATH}:.."

# install cpu version of torch to not require gpu version by sentence-transformers: https://stackoverflow.com/questions/77205123/how-do-i-slim-down-sberts-sentencer-transformer-library
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
COPY src/gui-search/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ENTRYPOINT flask run
