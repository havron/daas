from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, time

time.sleep(60)
print("loop")
consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
es = Elasticsearch(['es'])
for message in consumer:
  m = json.loads((message.value).decode('utf-8'))
  print(m)
  some_new_listing = {'owner': m['owner'], 'drone': m['drone'], 'listing_id':m['listing_id'], 'price_per_day':m['price_per_day'],'time_posted':m['time_posted'], 'description':m['description']}
  es.index(index='listing_index', doc_type='listing', id=some_new_listing['listing_id'], body=some_new_listing)
  es.indices.refresh(index="listing_index")
  print("let's search")
  print(es.search(index='listing_index', body={'query': {'query_string': {'query': 'air'}}, 'size': 10}))
  print("search done")

# while(True):
# print("loop")
#   try:
#     consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
#     es = Elasticsearch(['es'])
#     for message in consumer:
#       m = json.loads((message.value).decode('utf-8'))
#       print(m)
#       some_new_listing = {'owner': m['owner'], 'drone': m['drone'], 'listing_id':m['listing_id'], 'price_per_day':m['price_per_day'],'time_posted':m['time_posted'], 'description':m['description']}
#       es.index(index='listing_index', doc_type='listing', id=some_new_listing['listing_id'], body=some_new_listing)
#       es.indices.refresh(index="listing_index")
#       print("let's search")
#       print(es.search(index='listing_index', body={'query': {'query_string': {'query': 'air'}}, 'size': 10}))
#       print("search done")
#   except:
#     print("no kafka queue index found")
#     time.sleep(30)
