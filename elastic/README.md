# Elasticsearch

Structure of Elasticsearch index (along with property mappings) is defined in `documents-index.json` file. 

## Creating index

Replace `${ELASTICSEARCH_URL}` with a proper URI to the Elasticsearch HTTP layer. Additional options of curl might be required (e.g. when Elasticsearch is proxied).

```bash
$ curl -XPUT ${ELASTICSEARCH_URL}/documents -H 'Content-Type: application/json' -d @documents-index.json
```

## Settings

According to your means and needs, you can alter `number_of_shards` and `number_of_replicas`. 
Current setup should result in a _"green"_ health check for a single-node Elasticsearch cluster.

## Operating with indices

Check [Elasticsearch docs](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html) for details of how to add, retrieve or manipulate with Elasticsearch data. 

## Running Elasticsearch and Kibana

Setup Elasticsearch and Kibana using [Elastic stack guide](https://www.elastic.co/guide/en/elastic-stack-get-started/7.7/get-started-elastic-stack.html) from their official site. Alternatively, you can use nshou's [Docker image](https://hub.docker.com/r/nshou/elasticsearch-kibana/).
