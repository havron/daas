from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import datetime
import time
from datetime import datetime
import arrow
from daasapp import err_exp, err_web
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import messages

class LoginForm(forms.Form):
  username = forms.CharField(label="Your daas! username")
  password = forms.CharField(label="Your daas! password", widget=forms.PasswordInput)

class AuthForm(forms.Form): # not used by a user, so no need to be user-friendly.
  authenticator = forms.CharField()
  # user_id = forms.IntegerField() # currently not implemented. cookies not storing this...

class RegisterForm(forms.Form):
  f_name = forms.CharField(label="Your first name")
  l_name = forms.CharField(label="Your last name")
  username = forms.CharField(label="Your daas! username")
  email1 = forms.EmailField(label="Your daas! email address")
  email2 = forms.EmailField(label="Your daas! email address (again)")
  bio = forms.CharField(label="A short description of yourself!", widget=forms.Textarea)
  password1 = forms.CharField(label="Your daas! password", widget=forms.PasswordInput)
  password2 = forms.CharField(label="Your daas! password (again)", widget=forms.PasswordInput)
  def clean_email2(self):
      email1 = self.cleaned_data.get('email1')
      email2 = self.cleaned_data.get('email2')

      if not email2:
          raise forms.ValidationError("You must confirm your email")
      if email1 != email2:
          raise forms.ValidationError("Your emails do not match")
      return email2

  def clean_password2(self):
      password1 = self.cleaned_data.get('password1')
      password2 = self.cleaned_data.get('password2')

      if not password2:
          raise forms.ValidationError("You must confirm your password")
      if password1 != password2:
          raise forms.ValidationError("Your passwords do not match")
      return password2


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



########################################################

# use the decorator @login_required in other views that need it! :-)
def login_required(f):
  def wrap(request, *args, **kwargs):
    response = HttpResponseRedirect(reverse("login")+"?next="+request.path)
    auth = request.COOKIES.get('auth')
    if not auth:
      messages.success(request, 'You are not logged in.')
      return response

    form = AuthForm(dict(authenticator=auth))
    if not form.is_valid():
      messages.success(request, 'You are not logged in.')
      response.delete_cookie('auth') # deletes from client cookies. already deleted in db.
      return response

    post_data = form.cleaned_data
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/auth/', data=post_encoded, method='POST')
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)

    if not resp:
      resp = {'resp':err_web.E_TECH_DIFFICULTIES}
      return render(request, 'web/t404.html', resp)

    if resp['ok'] == False:
      messages.success(request, 'You are not logged in.')
      response.delete_cookie('auth') # deletes from client cookies. already deleted in db.
      return response

    return f(request, *args, **kwargs)
  return wrap


def index(request): # home page! 
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/index.html', context)


# Look into https://github.com/kencochrane/django-defender for blocking brute force login requests
def login(request): # /login
  login_form = LoginForm()
  register_form = RegisterForm()
  if request.method == 'GET':
    next = request.GET.get('next') or reverse('index')
    return render(request, 'web/login.html', {'login_form':login_form, 'register_form': register_form , 'next':next})

  if request.method != 'POST': # user did not make GET or POST request (unlikely).
    resp = err_web.E_BAD_REQUEST
    return render(request, 'web/t404.html', resp)
  
  form = LoginForm(request.POST)
  if not form.is_valid():
    invalid_form = err_web.E_FORM_INVALID
    return render(request, 'web/login.html', invalid_form)

  next = request.GET.get('next') or reverse('index')

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/login/', data=post_encoded, method='POST')

  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = {'resp':err_web.E_TECH_DIFFICULTIES}
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    resp = err_web.E_LOGIN_FAILED
    return render(request, 'web/login.html', {'login_form':login_form, 'register_form': register_form, 'resp': resp, 'next':next})


  authenticator = resp['resp']['authenticator']
  response = HttpResponseRedirect(next)
  messages.success(request, 'Successfully logged in!')
  response.set_cookie("auth", authenticator)
  response.set_cookie("user", form.cleaned_data['username'])
  response.set_cookie("pk", resp['resp']['user_id'])
  return response



@login_required
def logout(request): # /logout
  auth = request.COOKIES.get('auth')
  if not auth: # should never happen with our decorator, but just in case.
    messages.success(request, 'You are not logged in.')
    return HttpResponseRedirect(reverse("login"))

  if request.method != 'GET':
    resp = err_web.E_BAD_REQUEST
    return render(request, 'web/t404.html', resp)
  
  form = AuthForm(dict(authenticator=auth))
  if not form.is_valid():
    resp = err_web.E_TECH_DIFFICULTIES
    return render(request, 'web/login.html', {'resp':resp})
  
  next = request.GET.get('next') or reverse('index')

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/logout/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = {'resp':err_web.E_TECH_DIFFICULTIES}
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    #resp = {'resp':err_web.E_LOGOUT_FAILED}
    return render(request, 'web/login.html', {'resp':resp})

  response = HttpResponseRedirect(next)
  response.delete_cookie('auth') # deletes from client cookies. already deleted in db.
  response.delete_cookie('pk') # deletes from client cookies. already deleted in db.
  response.delete_cookie('user') # deletes from client cookies. already deleted in db.
  messages.success(request, 'Successfully logged out!')
  return response



def register(request): # /login
  login_form = LoginForm()
  register_form = RegisterForm()
  if request.method == 'GET':
    return render(request, 'web/login.html', {'login_form':login_form, 'register_form': register_form })

  if request.method != 'POST': # user did not make GET or POST request (unlikely).
    resp = err_web.E_BAD_REQUEST
    return render(request, 'web/t404.html', resp)
  
  form = RegisterForm(request.POST)
  if not form.is_valid():
    #resp = {'resp': err_web.E_FORM_INVALID} #TODO for rest
    resp = {'resp': form.errors} #TODO for rest
    return render(request, 'web/login.html', resp)
  
  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/register/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = {'resp':err_web.E_TECH_DIFFICULTIES}
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    resp = {'resp':err_web.E_REGISTER_FAILED}
    return render(request, 'web/login.html', {'login_form':login_form, 'register_form': register_form, 'resp':resp })


  resp = '<span style="font-size:30px; color=orange">congrats, you registered an account successfully! login to get started :)</span>'
  return render(request, 'web/login.html', {'resp':resp})



@login_required
def checkout(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/checkout.html', context)

@login_required
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
  req = urllib.request.Request('http://exp-api:8000/hi/')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  if not resp:
    resp = {'resp':err_web.E_TECH_DIFFICULTIES}
    return render(request, 'web/t404.html', resp)

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

    if not resp:
      resp = {'resp':err_web.E_TECH_DIFFICULTIES}
      return render(request, 'web/t404.html', resp)

    if resp['resp']['ok'] == False:
      resp = {'resp':err_web.E_DRONE_NOT_FOUND}
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

    if not resp:
      resp = {'resp':err_web.E_TECH_DIFFICULTIES}
      return render(request, 'web/t404.html', resp)

    if resp['resp']['ok'] == False:
      resp = {'resp':err_web.E_USER_NOT_FOUND}
      return render(request, 'web/t404.html', resp)
    
    resp2 = resp['resp']
    t = arrow.get(resp2['resp']['date_joined'])
    resp2['resp']['date_joined'] = str(t.format('D MMMM, YYYY') + " at " + t.format('h:mma'))

  return render(request, 'web/userprofile.html', resp2)

def listing(request, listing_id=None):
  resp = {}
  resp2 = {}
  if listing_id:
    req = urllib.request.Request('http://exp-api:8000/listing/'+listing_id)
    resp_json = urllib.request.urlopen(req).read().decode('utf-8')
    resp = json.loads(resp_json)
    
    if not resp:
      resp = {'resp':err_web.E_TECH_DIFFICULTIES}
      return render(request, 'web/t404.html', resp)

    if resp['resp']['ok'] == False:
      resp = {'resp':err_web.E_LISTING_NOT_FOUND}
      return render(request, 'web/t404.html', resp)

    resp2 = resp['resp']
    t = arrow.get(resp2['resp']['time_posted'])
    resp['resp']['resp']['time_posted'] = str(t.format('D MMMM, YYYY') + " at " + t.format('h:mma'))

    resp2 = resp['resp']
    t = arrow.get(resp2['resp']['drone']['last_checked_out'])
    resp['resp']['resp']['drone']['last_checked_out'] = str(t.format('D MMMM, YYYY') + " at " + t.format('h:mma'))

  return render(request, 'web/listing.html', resp.get("resp"))      


@login_required
def create_listing(request):

  if request.method == 'GET':   
    listing_form = ListingForm()

    next = request.GET.get('next') or reverse('index')
    return render(request, 'web/create-listing.html', {'listing_form': listing_form, 'next':next})
    
    '''
    # inspect all drones that owner ownes
    drones_json = urllib.request.urlopen(req).read().decode('utf-8')
    drones = json.loads(drones_json)

    if not drones:
      resp = {'resp':err_web.E_TECH_DIFFICULTIES}
      return render(request, 'web/t404.html', resp)

    if drones['ok'] == False:
      resp = {'resp':err_web.E_DRONE_NOT_FOUND}
      return render(request, 'web/t404.html', resp)
    
    listing_form = ListingForm( initial = { 'my_drones': drones.get("my_drones") })
    '''

  if request.method != 'POST': # user did not make GET or POST request (unlikely).
    resp = err_web.E_BAD_REQUEST
    return render(request, 'web/t404.html', resp)

  form = ListingForm(request.POST)
  if not form.is_valid():
    #resp = {'resp': err_web.E_FORM_INVALID} #TODO for rest
    resp = {'resp': form.errors} #TODO for rest
    return render(request, 'web/create-listing.html', resp)
  
  post_data = form.cleaned_data
  post_data['auth'] = request.COOKIES.get("auth")
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/listing/create/', data=post_encoded, method='POST')

  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = {'resp':err_web.E_TECH_DIFFICULTIES}
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    listing_form = ListingForm()
    return render(request, 'web/create-listing.html', {'listing_form': listing_form, 'resp':resp })


  next = '/listing/' + str(resp['resp']['listing_id'])
  response = HttpResponseRedirect(next)
  #messages.success(request, 'Successfully created Listing!')
  messages.success(request, resp['resp'])
  return response
    
  '''
        auth = request.COOKIES.get('auth')
    form = AuthForm(dict(authenticator=auth))
    if not form.is_valid():
      resp = {'resp':err_web.E_TECH_DIFFICULTIES}
      return render(request, 'web/t404.html', resp)

    post_data = form.cleaned_data
    post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
    req = urllib.request.Request('http://exp-api:8000/create-listing/', data=post_encoded, method='POST')
    '''

  '''
  form = LoginForm(request.POST)
  if not form.is_valid():
    invalid_form = err_web.E_FORM_INVALID
    return render(request, 'web/login.html', invalid_form)
  
  next = request.GET.get('next') or reverse('index')

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/login/', data=post_encoded, method='POST')

  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = {'resp':err_web.E_TECH_DIFFICULTIES}
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    resp = err_web.E_LOGIN_FAILED
    return render(request, 'web/login.html', {'login_form':login_form, 'register_form': register_form, 'resp': resp, 'next':next})


  authenticator = resp['resp']['authenticator']
  response = HttpResponseRedirect(next)
  messages.success(request, 'Successfully logged in!')
  response.set_cookie("auth", authenticator)
  response.set_cookie("user", form.cleaned_data['username'])
  response.set_cookie("pk", resp['resp']['user_id'])
  return response
  '''


# featured items in shop.html
def featured_items(request):
  resp = {}
  resp2 = {}
  req = urllib.request.Request('http://exp-api:8000/shop/')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
    
  if not resp:
    resp = {'resp':err_web.E_TECH_DIFFICULTIES}
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False:
    resp = {'resp':err_web.E_LISTING_NOT_FOUND}
    return render(request, 'web/t404.html', resp)

  return render(request, 'web/shop.html', resp.get("resp"))      


# search results
def search_results(request):
  print("nil")

#def search(request, q): # doesn't work for some reason?
def search(request):
  if request.method != 'POST': 
    resp = {'resp':'bad request'}
    return render(request, 'web/t404.html', resp)
  
  query = request.POST['q']

  post_data = {'query':request.POST['q']}
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/search/', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  
  if not resp:
    resp = {'resp':resp}
    resp['resp']['query'] = query
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False:
    #resp = {'resp':resp}
    #resp['resp']['query'] = query
    #return render(request, 'web/t404.html', resp)
    resp['query'] = query
    return render(request, 'web/search-result.html', resp)      

  
  resp['resp'].append(query)
  resp['query'] = query
  return render(request, 'web/search-result.html', resp)      
