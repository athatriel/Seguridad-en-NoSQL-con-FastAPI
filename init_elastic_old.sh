#!/bin/sh

curl -X PUT http://localhost:9200/articulos \
-H "Content-Type: application/json" \
-d '{
  "mappings": {
    "properties": {
      "titulo": {"type": "text"},
      "precio": {"type": "integer"}
    }
  }
}'

curl -X POST http://localhost:9200/articulos/_doc \
-H "Content-Type: application/json" \
-d '{
  "titulo":"Portatil Lenovo",
  "precio":700
}'

curl -X POST http://localhost:9200/articulos/_doc \
-H "Content-Type: application/json" \
-d '{
  "titulo":"Monitor Dell",
  "precio":250
}'
