#!/bin/bash

docker compose up -d

# $ docker build -t test -f py.Dockerfile .

# $ docker run -d -p 8888:8888 --name testcontainer test

dock_jcontainer="$(docker container ls | awk '{if(NR>1) print $NF}' | grep py)"

while true; do
    if docker logs $dock_jcontainer 2>&1 | grep -q "To access the server"; then
        dock_jlogs="$(docker logs $dock_jcontainer 2>&1)"
        break
    fi
done

dock_URL="$(grep -P 'http:\/\/127.0.0.1:8888\/tree\?token=[^\s]+$' <<< $dock_jlogs | awk 'NR==2 {print $1}')"

dock_URLjn="$(echo $dock_URL | sed 's/\/tree/\/notebooks\/search-index.ipynb/')"

my_message() {
    echo "$1 is about to open in the browser. Attempt number $2"
}

my_counter=0

while true; do
    curl -s $dock_URLjn >/dev/null
    if [ $? -eq 0 ]; then
        xdg-open $dock_URLjn
        break
    else
        ((my_counter++))
        my_message "Jupyter Notebook" $my_counter
        sleep 5
    fi
done

my_counter=0

while true; do
    curl -s http://127.0.0.1:9200/ >/dev/null
    if [ $? -eq 0 ]; then
        xdg-open http://127.0.0.1:9200/
        break
    else
        ((my_counter++))
        my_message "Elasticsearch" $my_counter
        sleep 5
    fi
done
