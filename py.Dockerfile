
FROM python:3.12.2

WORKDIR /app

COPY search.py app/src/search.py
COPY data app/data/

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# CMD python search.py
CMD ["bash", "-c", "echo hello && exec bash"]