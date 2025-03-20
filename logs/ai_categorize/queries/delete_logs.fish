#!/usr/bin/env fish

curl -XPOST 'http://localhost:9200/nginx-access/_delete_by_query' \
    -H 'Content-Type: application/json' \
    -d '{"query": {"match_all": {}}}'
