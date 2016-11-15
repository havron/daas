from django.shortcuts import render
from django import forms
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse
from daasapp import err_models, err_exp
from django.contrib.auth import hashers
import datetime
from kafka import KafkaProducer
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import time

# GLOBAL
es = Elasticsearch(['es']) 

class LoginForm(forms.Form):
  username = forms.CharField()
  password = forms.CharField()

class AuthForm(forms.Form):
  authenticator = forms.CharField()
  #user_id = forms.IntegerField() # not implemented at the moment (not stored in cookies)

class RegisterForm(forms.Form):
  f_name = forms.CharField(label="Your first name")
  l_name = forms.CharField(label="Your last name")
  username = forms.CharField(label="Your daas! username")
  email1 = forms.EmailField(label="Your daas! email address")
  email2 = forms.EmailField(label="Your daas! email address (again)")
  bio = forms.CharField(label="A short description of yourself!", widget=forms.Textarea)
  password1 = forms.CharField(label="Your daas! password", widget=forms.PasswordInput)
  password2 = forms.CharField(label="Your daas! password (again)", widget=forms.PasswordInput)

class ListingForm(forms.Form):
  # my_drones = forms.ChoiceField(label="Choose your drone", choices = "no drones")
  price_per_day = forms.FloatField( label = "Price of Drone per day")
  description = forms.CharField(label = "Write something about your lease.", widget=forms.Textarea )    
  model_name = forms.CharField(label = "model name of your drone")
  drone_desc = forms.CharField(label = "Write something about this particular drone", widget = forms.Textarea)
  demo_link = forms.URLField(label = "link to demo", required=False) # (link to photo gallery or videos)
  permissions = forms.CharField(label = "legals", widget = forms.Textarea)
  battery_level = forms.FloatField(label = "battery level")
  maintenance_status = forms.CharField(label = "maintenance status", widget = forms.Textarea)
  available_for_hire = forms.BooleanField(label = "ready for hire?")

################ RESPONSE HELPER FUNCTIONS #############

# _ denotes a helper function
def _success_response(request, resp=None):
  if resp:
    return JsonResponse({'ok': True, 'resp': resp})
  else:
   return JsonResponse({'ok': True})

# _ denotes a helper function
# EXP ERROR CODES DOCUMENTED IN 'err_exp.py'
def _error_response(request, error_msg, error_specific=None):
   if error_specific:
     return JsonResponse({'ok': False, 'error': error_msg, 'error_info': error_specific})
   else:
     return JsonResponse({'ok': False, 'error': error_msg})


def check_auth(request): # /auth
  if request.method != 'POST':  
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make POST request")

  form = AuthForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_exp.E_FORM_INVALID, "user logout form not correctly filled out")

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://models-api:8000/api/v1/user/auth/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    return _error_response(request, err_exp.E_LOGIN_FAILED, "no response from models API")
  if resp['ok'] == False: # could be much more nuanced. makes web view handle errors
    return _error_response(request, err_exp.E_LOGIN_FAILED, resp)

  # if datetime.datetime.now() - resp['resp']['date_created'] > : ... expiration of auth token not implemented.
  return _success_response(request, resp['resp'])



# Look into https://github.com/kencochrane/django-defender for blocking brute force login requests
def login(request): # /login
  if request.method != 'POST':  
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make POST request")

  form = LoginForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_exp.E_FORM_INVALID, "user login form not correctly filled out")

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://models-api:8000/api/v1/user/login/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    return _error_response(request, err_exp.E_LOGIN_FAILED, "no response from models API")
  if resp['ok'] == False: # could be much more nuanced. makes web view handle errors
    return _error_response(request, err_exp.E_LOGIN_FAILED, resp)

  return _success_response(request, resp['resp'])


def logout(request): # /logout
  if request.method != 'POST':  
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make POST request")

  form = AuthForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_exp.E_FORM_INVALID, "user logout form not correctly filled out")

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://models-api:8000/api/v1/user/logout/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    return _error_response(request, err_exp.E_LOGIN_FAILED, "no response from models API")
  if resp['ok'] == False: # could be much more nuanced. makes web view handle errors
    return _error_response(request, err_exp.E_LOGIN_FAILED, resp)

  #return _success_response(request, resp['resp'])
  return _success_response(request, "logged out successfully")


def register(request): # /register
  if request.method != 'POST':  
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make POST request")

  form = RegisterForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_exp.E_FORM_INVALID, "user registration form not correctly filled out")

  post_data = form.cleaned_data
  post_data['password'] = hashers.make_password(post_data['password1']) # get first validated password and hash it
  post_data['date_joined'] = datetime.datetime.now()
  post_data['is_active'] = True
  post_data['email_address'] = post_data['email1'] 

  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://models-api:8000/api/v1/user/create/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    return _error_response(request, err_exp.E_REGISTER_FAILED, "no response from models API")
  if resp['ok'] == False: # could be much more nuanced. makes web view handle errors
    return _error_response(request, err_exp.E_REGISTER_FAILED, resp)

  return _success_response(request, resp['resp'])


# fields = ['username', 'password', 'email_address','date_joined','is_active','f_name','l_name', 'bio']


def hi(request): # /hi
  context = {} # can send dictionary values (results of api calls) to the template
  req = urllib.request.Request('http://models-api:8000/api/v1/user/all/')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  return _success_response(request, resp)



def productdetails(request, drone_id): # /product-details/(?P<drone_id>\d+)
  if request.method != 'GET':
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make GET request with drone_id")

  req = urllib.request.Request('http://models-api:8000/api/v1/drone/'+drone_id)
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  return _success_response(request, resp)



def userprofile(request, user_id): # /userprofile/(?P<user_id>\d+)
  if request.method != 'GET':
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make GET request with user_id")

  req = urllib.request.Request('http://models-api:8000/api/v1/user/'+user_id)
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  return _success_response(request, resp)



def listing(request, listing_id):
  if request.method != 'GET':
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make a GET request with listing_id")
  req = urllib.request.Request('http://models-api:8000/api/v1/listing/'+listing_id)
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  return _success_response(request, resp) 


def create_listing(request): # /create-listing
  if request.method != 'POST':  
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make POST request")

  form = ListingForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_exp.E_FORM_INVALID, "listing form not correctly filled out")

  post_data = form.cleaned_data
  post_data['auth'] = request.POST['auth']
  post_data['last_checked_out'] = datetime.datetime.now()

  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://models-api:8000/api/v1/drone/create/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    return _error_response(request, err_exp.E_REGISTER_FAILED, "no response from models API")
  if resp['ok'] == False: # could be much more nuanced. makes web view handle errors
    return _error_response(request, err_exp.E_REGISTER_FAILED, resp)

  post_data['_drone_key'] = resp['resp']['drone_id']
  post_data['time_posted'] = datetime.datetime.now()

  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://models-api:8000/api/v1/listing/create/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    return _error_response(request, err_exp.E_REGISTER_FAILED, "no response from models API")
  if resp['ok'] == False: # could be much more nuanced. makes web view handle errors
    return _error_response(request, err_exp.E_REGISTER_FAILED, {'resp':resp})
  
  '''
  # add newly created listing to Kafka 
  # get listing 
  req = urllib.request.Request('http://models-api:8000/api/v1/listing/'+resp['listing_id'])
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp1 = json.loads(resp_json)
  resp1['listing_id'] = resp1['id']
  '''
  # add to kafka
  producer = KafkaProducer(bootstrap_servers='kafka:9092')

  # need to pass dictionary object
  new_listing = resp['resp']
  producer.send('new-listings-topic', json.dumps(new_listing).encode('utf-8'))
  print(new_listing)
  
  return _success_response(request, resp['resp'])


def my_drones(request): # /my-drones
  if request.method != 'POST':  
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make POST request")

  form = AuthForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_exp.E_FORM_INVALID, "user logout form not correctly filled out")

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://models-TODO:8000/api/v1/my-drones/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    return _error_response(request, err_exp.E_LOGIN_FAILED, "no response from models API")
  if resp['ok'] == False: # could be much more nuanced. makes web view handle errors
    return _error_response(request, err_exp.E_LOGIN_FAILED, resp)

  # if datetime.datetime.now() - resp['resp']['date_created'] > : ... expiration of auth token not implemented.
  return _success_response(request, resp['resp'])


def featured_items(request): # /shop/
  if request.method != 'GET':
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make GET request")
  req  = urllib.request.Request('http://models-api:8000/api/v1/shop/')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  return _success_response(request, resp)


def search(request): # /search
  if request.method != 'POST':  
    return _error_response(request, err_exp.E_BAD_REQUEST, "must make POST request")
  
  if not es.indices.exists(index='listing_index'):
    return _error_response(request, 'listings not found')

  resp = []
  res = es.search(index='listing_index', body={'query': {'query_string': {'query': request.POST['query']}}, 'size': 10})
  hits = res['hits']['hits']
  if not hits:
    return _error_response(request, res)
  for hit in hits:
    resp.append(hit['_source']) # parse es source

  return _success_response(request, resp)
