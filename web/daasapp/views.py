from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import datetime
import time
from datetime import datetime
import arrow

def index(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/index.html', context)
def login(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/login.html', context)

def checkout(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/checkout.html', context)

def cart(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/cart.html', context)

def shop(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/shop.html', context)


def blog(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/blog.html', context)

def blogsingle(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/blog-single.html', context)

def t404(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/t404.html', context)

def contactus(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/contact-us.html', context)

def hi(request):
  context = {} # can send dictionary values (results of api calls) to the template
  print ("About to do the GET...")
  req = urllib.request.Request('http://exp-api:8000/hi')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  print(resp)
  return render(request, 'web/hi.html', resp)


def letsgrade(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/lets-grade.html', context)




def productdetails(request, drone_id=None): # allow conditional params

  resp = {}
  resp2 = {}
  if drone_id:
    req = urllib.request.Request('http://exp-api:8000/product-details/'+drone_id)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['resp']['ok'] == False:
      return render(request, 'web/t404.html', resp)
    
    resp2 = resp['resp']
    t = arrow.get(resp2['resp']['last_checked_out'])
    resp2['resp']['last_checked_out'] = str(t.format('D MMMM, YYYY') + " at " + t.format('h:mma'))


  return render(request, 'web/product-details.html', resp2)

def userprofile(request, user_id=None): # allow conditional params

  resp = {}
  resp2 = {}
  if user_id:
    req = urllib.request.Request('http://exp-api:8000/userprofile/'+user_id)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if resp['resp']['ok'] == False:
      return render(request, 'web/t404.html', resp)
    
    resp2 = resp['resp']
    t = arrow.get(resp2['resp']['date_joined'])
    resp2['resp']['date_joined'] = str(t.format('D MMMM, YYYY') + " at " + t.format('h:mma'))

  return render(request, 'web/userprofile.html', resp2)
