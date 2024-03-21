# https://www.elastic.co/search-labs/tutorials/install-elasticsearch/docker
FROM elasticsearch:8.11.0

ENV discovery.type=single-node
ENV xpack.security.enabled=false
ENV xpack.security.http.ssl.enabled=false
ENV xpack.license.self_generated.type=basic

CMD ["elasticsearch"]
