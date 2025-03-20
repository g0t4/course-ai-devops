#!/usr/bin/env fish

curl -X GET "http://localhost:9200/nginx-access/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
        "bool": {
            "must": [
                {"exists": {"field": "category"}}
            ]
        }
  },
  "size": 10
}' | jq

