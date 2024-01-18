
FROM python:latest

COPY search.py search.py/
COPY data data/

# executed at build-time
RUN pip install elasticsearch

# https://docs.docker.com/engine/reference/builder/#run
# shell form
RUN echo "hello from build-time py.dockerfile"
# exec form
RUN ["echo", "hello from build-time py.dockerfile"]

# executed at run-time
CMD echo "hello from run-time py.dockerfile"
# CMD python search.py
