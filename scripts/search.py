#search
from kafka import KafkaProducer
import json
producer = KafkaProducer(bootstrap_servers='kafka:9092')
some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id':42}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
