#!/usr/bin/env fish

curl -X GET "http://localhost:9200/nginx-access/_search" -H 'Content-Type: application/json' -d'
{
  "query": {
        "bool": {
            "must_not": [
                {"exists": {"field": "category"}}
            ]
        }
  },
  "size": 2
}' | jq

