
FROM python:3.12.2-slim-bookworm

WORKDIR /app/src/gui-search

COPY src/gui-search/requirements.txt .

ENV PYTHONPATH "${PYTHONPATH}:.."

RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

ENTRYPOINT flask run
