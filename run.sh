#!/bin/bash

# set -x

my_command="docker compose up -d"

if [[ "$1" == "--build" ]]; then
    my_command="docker compose up -d --build"
    $my_command || exit 1
elif [[ "$1" == "down" ]]; then
    my_command="docker compose down"
    $my_command
    exit 0
else
    $my_command || exit 1
fi

# given a container running jupyter find the notebook URL
if docker container ls | awk '{print $5}' | grep -q jupyter; then
    dock_jcontainer="$(docker container ls | awk '{if(NR>1) print $NF}' | grep py)"

    until $(docker logs $dock_jcontainer 2>&1 | grep -q "To access the server"); do
        echo waiting for Jupyter...
        sleep 5         
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

my_open_services http://127.0.0.1:5000/ search-GUI

if [ -z $dock_URLjn ]; then
    exit 0
else
    my_open_services $dock_URLjn "Jupyter Notebook"
fi


if docker container ls | awk '{print $5}' | grep -q python3; then
    dock_jcontainer="$(docker container ls | awk '{if(NR>1) print $NF}' | grep py)"

    echo data is being piped and processed to ES... This may take 10 minutes.
    my_counter=0

    until $(docker logs $dock_jcontainer 2>&1 | grep -q "Inserted number of messages:"); do

        ((my_counter++))

        echo data is being prepared for MES-SEARCH... Waiting 20 seconds. Round $my_counter
        sleep 20

    done

    echo MES-SEARCH can now be used!
else
    echo The data pipeline is not running as it should...
fi


exit 0

# $ docker build --no-cache --progress=plain --rm -t py-peline:1.0.0 -f py.Dockerfile .
# $ docker run --rm -d -p 8888:8888 --mount type=bind,src=$(pwd)/src/pipeline,dst=/app/src/pipeline --name mes-search-py-peline py-peline:1.0.0

# $ docker build --rm -t es-client:1.0.0 -f es.Dockerfile .
# $ docker run -d -p 9200:9200 --name mes-search-es-client-1 es-client:1.0.0

# $ docker build --no-cache --progress=plain --rm -t flask:1.0.0 -f fl.Dockerfile .
# $ docker run --rm -it -p 5001:5001 --mount type=bind,src=$(pwd)/src,dst=/app/src --name mes-search-gui-search-1 flask:1.0.0
