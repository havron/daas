#search
from kafka import KafkaProducer
import json, time
print("sleeping")
time.sleep(1)
print("slept")

producer = KafkaProducer(bootstrap_servers='kafka:9092')

some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': 42}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
print(some_new_listing)

counter = 1;
time.sleep(5)

'''
print("pls  work")
some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': counter}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
print(some_new_listing)
counter = counter + 1

print("pls  work")
some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': counter}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
print(some_new_listing)
counter = counter + 1

print("pls  work")
some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': counter}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
print(some_new_listing)
counter = counter + 1

print("pls  work")
some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': counter}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
print(some_new_listing)
counter = counter + 1

print("pls  work")
some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': counter}
producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
print(some_new_listing)
counter = counter + 1
'''



for i in range(100):  
  print("pls work")
  some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': i}
  producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
  print(some_new_listing)
  time.sleep(5)

  

'''
                 
for i in range(43,143):
	print("trying")
	some_new_listing = {'title': 'Used MacbookAir 13"', 'description': 'This is a used Macbook Air in great condition', 'id': i}
	producer.send('new-listings-topic', json.dumps(some_new_listing).encode('utf-8'))
	print(some_new_listing)
	time.sleep(5)
'''
