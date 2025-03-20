#!/usr/bin/env fish


curl -X GET "http://localhost:9200/nginx-access/_search" -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "distinct_categories": {
      "terms": {
        "field": "category.keyword",
        "size": 1000
      }
    }
  }
}' | jq
