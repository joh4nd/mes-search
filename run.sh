#!/bin/bash

# $ docker build -t py-peline:0.1.1 -f py.Dockerfile .
# $ docker run -d -p 8888:8888 --name mes-search-py-peline py-peline:0.1.1

# $ docker build -t es-client:0.1.1 -f es.Dockerfile .
# $ docker run -d -p 8888:8888 --name mes-search-es-client-1 es-client:0.1.1

# $ docker build -t flask:0.1.1 -f fl.Dockerfile .
# $ docker run -it -p 5001:5001 --name mes-search-gui-search-1 flask:0.1.1

# set -x

my_command="docker compose up -d"

if [[ "$1" == "--build" ]]; then
    my_command="docker compose up -d --build"
    $my_command
elif [[ "$1" == "down" ]]; then
    my_command="docker compose down"
    $my_command
    exit 0
else
    $my_command
fi

# given a python container name find the jupyter notebook URL
if docker container ls | awk '{if(NR>1) print $NF}' | grep py; then
    dock_jcontainer="$(docker container ls | awk '{if(NR>1) print $NF}' | grep py)"

    until [ $(docker logs $dock_jcontainer 2>&1 | grep "To access the server") ]; do
        echo waiting for Jupyter...
        sleep 2            
    done

    dock_jlogs="$(docker logs $dock_jcontainer 2>&1)"

    dock_URL="$(grep -P 'http:\/\/127.0.0.1:8888\/tree\?token=[^\s]+$' <<< $dock_jlogs | awk 'NR==2 {print $1}')"

    dock_URLjn="$(echo $dock_URL | sed 's/\/tree/\/notebooks\/search-index.ipynb/')"
else
    echo No Jupyter container...
fi

my_open_services() {

    url=$1
    name=$2
    my_counter=0

    until curl -s $url >/dev/null; do
        ((my_counter++))
        echo $name is about to open in the browser. Attempt number $my_counter $2
        sleep 5
    done

    echo $name will open in the browser!
    xdg-open $url
}

my_open_services http://127.0.0.1:9200/ Elasticsearch

my_open_services http://127.0.0.1:5001/ search-GUI

if [ -z $dock_URLjn ]; then
    exit 0
else
    my_open_services $dock_URLjn "Jupyter Notebook"
fi

exit 0