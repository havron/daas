from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json, time

# time.sleep(60)
# print("loop")
# consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
# es = Elasticsearch(['es'])
# for message in consumer:
#   m = json.loads((message.value).decode('utf-8'))
#   print(m)
#   some_new_listing = {'owner': m['owner'], 'drone': m['drone'], 'listing_id':m['listing_id'], 'price_per_day':m['price_per_day'],'time_posted':m['time_posted'], 'description':m['description']}
#   es.index(index='listing_index', doc_type='listing', id=some_new_listing['listing_id'], body=some_new_listing)
#   es.indices.refresh(index="listing_index")
#   print("let's search")
#   print(es.search(index='listing_index', body={'query': {'query_string': {'query': 'air'}}, 'size': 10}))
#   print("search done")

while(True):
  time.sleep(30)
  print("loop")
  
  fixtureA = {"listing_id":1,"drone": 2, "owner": 2, "description": "please rent myseediestdrone!", "time_posted": "2016-10-24T04:28:48.932Z", "price_per_day": 10.0}

  fixtureB = {"listing_id":2,"drone": 3, "owner": 3, "description": "please rent myforgeddrone!", "time_posted": "2016-10-24T04:28:48.991Z", "price_per_day": 14.0}

  es = Elasticsearch(['es'])
  es.index(index='listing_index', doc_type='listing', id=fixtureA['listing_id'], body=fixtureA)
  es.index(index='listing_index', doc_type='listing', id=fixtureB['listing_id'], body=fixtureB)
  es.indices.refresh(index='listing_index')

  try:
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

  except:
    print("no kafka queue index found")
    time.sleep(30)
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

  for message in consumer:
    m = json.loads((message.value).decode('utf-8'))
    print(m)
    some_new_listing = {'owner': m['owner'], 'drone': m['drone'], 'listing_id':m['listing_id'], 'price_per_day':m['price_per_day'],'time_posted':m['time_posted'], 'description':m['description']}
    some_new_listing = m
    es.index(index='listing_index', doc_type='listing', id=some_new_listing['listing_id'], body=some_new_listing)
    es.indices.refresh(index="listing_index")
    print("let's search")
    print(es.search(index='listing_index', body={'query': {'query_string': {'query': 'myseediestdrone'}}, 'size': 10}))
    print("search done")
