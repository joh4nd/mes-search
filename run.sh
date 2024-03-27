#!/bin/bash

# run containers
$ docker compose up -d

# $ docker build -t test -f py.Dockerfile .
# $ docker run -d -p 8888:8888 --name testcontainer test

# run notebook in host browser
$ xdg-open $(docker logs testcontainer 2>&1 | grep -P 'http:\/\/127.0.0.1:8888\/tree\?token=[^\s]+$') | awk 'NR==2 {print $1}')
