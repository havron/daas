from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
for message in consumer:
  print(json.loads((message.value).decode('utf-8')))







from elasticsearch import Elasticsearch
es = Elasticsearch(['es'])
some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id':42}
es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
es.indices.refresh(index="listing_index")
es.search(index='listing_index', body={'query': {'query_string': {'query': 'macbook air'}}, 'size': 10})


