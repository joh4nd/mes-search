# https://www.elastic.co/search-labs/tutorials/install-elasticsearch/docker
# https://github.com/elastic/elasticsearch/issues/102416
# https://www.elastic.co/guide/en/elasticsearch/reference/8.12/dense-vector.html#index-vectors-knn-search
FROM elasticsearch:8.12.0

ENV discovery.type=single-node
ENV xpack.security.enabled=false
ENV xpack.security.http.ssl.enabled=false
ENV xpack.license.self_generated.type=basic

ENTRYPOINT ["elasticsearch"]
