# run ES in Docker
# https://www.elastic.co/search-labs/tutorials/install-elasticsearch/docker
# modified, see docker-compose

# docker.elastic.co/elasticsearch/elasticsearch:8.11.0
FROM elasticsearch:8.11.0

ENV discovery.type=single-node
ENV xpack.security.enabled=false
ENV xpack.security.http.ssl.enabled=false
ENV xpack.license.self_generated.type=basic

CMD ["elasticsearch"]
