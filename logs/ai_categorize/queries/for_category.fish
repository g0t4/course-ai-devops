#!/usr/bin/env fish

set category $argv[1]

curl -X GET "http://localhost:9200/nginx-access/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
        "match": {
            "category": "'$category'"
        }
  },
  "size": 10
}' | jq
