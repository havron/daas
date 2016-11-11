from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])
for message in consumer:
  m = json.loads((message.value).decode('utf-8')))
  print(m)
  some_new_listing = {'title': m['title'], 'description': m['description'], 'id':m['id']}
  es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
  es.indices.refresh(index="listing_index")
  print("let's search")
  es.search(index='listing_index', body={'query': {'query_string': {'query': 'macbook air'}}, 'size': 10})
  print("search done")
