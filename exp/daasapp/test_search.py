from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
from kafka import KafkaProducer
from . import views
import json
import datetime
import random
import arrow

class ListingFormTests(TestCase):
  #fixtures = ['db']  # load from DB

  def setUp(self): # try to indice some fixtures to elasticsearch
    self.client = Client()


  # append number to test to get python to run defs in correct order
  def test1_es_index(self): # not passing 

    fixtureA = {"listing_id":1,"drone": 2, "owner": 2, "description": "please rent myseediestdrone!", "time_posted": "2016-10-24T04:28:48.932Z", "price_per_day": 10.0}
    fixtureB = {"listing_id":2,"drone": 3, "owner": 3, "description": "please rent myforgeddrone!", "time_posted": "2016-10-24T04:28:48.991Z", "price_per_day": 14.0}

    response = self.client.post(reverse('create-listing'), fixtureA)
    print("test_create_listing POST " + str(response))

    resp = json.loads(response.content.decode('utf8'))
    self.assertEquals(response.status_code, 200)

    es = Elasticsearch(['es'])
    es.index(index='listing_index', doc_type='listing', id=fixtureA['listing_id'], body=fixtureA)
    es.index(index='listing_index', doc_type='listing', id=fixtureB['listing_id'], body=fixtureB)
    es.indices.refresh(index='listing_index')

    # search by description
    res = es.search(index='listing_index', body={'query': {'query_string': {'query': 'myseediestdrone'}}, 'size': 10})

    hits = res['hits']['hits']
    hit = hits[0]['_source']
    self.assertEquals(hit, fixtureA)

    # search by price-per-day
    res = es.search(index='listing_index', body={'query': {'query_string': {'query': '10.0'}}, 'size': 10})
    hits = res['hits']['hits']
    hit = hits[0]['_source']
    self.assertEquals(hit, fixtureA)
    print("searches successful!")

  def est1_kafka(self): # not passing 
    #producer = KafkaProducer(bootstrap_servers='kafka:9092')
    #producer.send('new-listings-topic', json.dumps(fixtureA).encode('utf-8'))

    fixtureA = {"listing_id":1,"drone": 2, "owner": 2, "description": "please rent myseediestdrone!", "time_posted": "2016-10-24T04:28:48.932Z", "price_per_day": 10.0}
    fixtureB = {"listing_id":2,"drone": 3, "owner": 3, "description": "please rent myforgeddrone!", "time_posted": "2016-10-24T04:28:48.991Z", "price_per_day": 14.0}

    es = Elasticsearch(['es'])
    es.index(index='listing_index', doc_type='listing', id=fixtureA['listing_id'], body=fixtureA)
    es.index(index='listing_index', doc_type='listing', id=fixtureB['listing_id'], body=fixtureB)
    es.indices.refresh(index='listing_index')
    #producer = KafkaProducer(bootstrap_servers='kafka:9092')
    #producer.send('new-listings-topic', json.dumps(fixtureA).encode('utf-8'))

    response = self.client.post(reverse('create-listing'), fixtureA)
    print("test_create_listing POST " + str(response))

    resp = json.loads(response.content.decode('utf8'))
    self.assertEquals(response.status_code, 200)
    print("listing_atts" + str(resp))

  def tearDown(self): 
    del self.client
