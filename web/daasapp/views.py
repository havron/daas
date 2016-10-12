from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import datetime
import time
from datetime import datetime
import arrow
from . import err_exp, err_web
from django import forms
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

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

# fields = ['username', 'password', 'email_address','date_joined','is_active','f_name','l_name', 'bio']

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

########################################################


def index(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/index.html', context)


# Look into https://github.com/kencochrane/django-defender for blocking brute force login requests
def login(request): # /login
  if request.method == 'GET':
    login_form = LoginForm()
    register_form = RegisterForm()
    next = request.GET.get('next') or reverse('index')
    return render(request, 'web/login.html', {'login_form':login_form, 'register_form': register_form })

  if request.method != 'POST': # user did not make GET or POST request (unlikely).
    resp = err_web.E_BAD_REQUEST
    return render(request, 'web/t404.html', resp)
  
  form = LoginForm(request.POST)
  if not form.is_valid():
    invalid_form = err_web.E_FORM_INVALID
    return render(request, 'web/login.html', invalid_form)
  
  next = form.cleaned_data.get('next') or reverse('index')

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/login', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = err_web.E_TECH_DIFFICULTIES
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    resp = err_web.E_LOGIN_FAILED
    return render(request, 'web/login.html', resp)


  authenticator = resp['resp']['authenticator']
  response = HttpResponseRedirect(next)
  response.set_cookie("auth", authenticator)
  return response



def logout(request): # /logout
  auth = request.COOKIES.get('auth')
  if not auth:
    # handle user not logged in while trying to create a listing
    return HttpResponseRedirect(reverse("login"))

  if request.method != 'GET':
    resp = err_web.E_BAD_REQUEST
    return render(request, 'web/t404.html', resp)
  
  form = AuthForm(dict(auth))
  if not form.is_valid():
    resp = err_web.E_TECH_DIFFICULTIES
    return render(request, 'web/login.html', resp)
  
  next = form.cleaned_data.get('next') or reverse('index')

  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/logout', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = err_web.E_TECH_DIFFICULTIES
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    resp = err_web.E_LOGOUT_FAILED
    return render(request, 'web/login.html', resp)

  response = HttpResponseRedirect(next)
  response.set_cookie("auth", '') # deletes from client cookies. already deleted in db.
  return response



def register(request): # /login
  if request.method == 'GET':
    login_form = LoginForm()
    register_form = RegisterForm()
    return render(request, 'web/login.html', {'login_form':login_form, 'register_form': register_form })

  if request.method != 'POST': # user did not make GET or POST request (unlikely).
    resp = err_web.E_BAD_REQUEST
    return render(request, 'web/t404.html', resp)
  
  form = RegisterForm(request.POST)
  if not form.is_valid():
    invalid_form = {'invalid_form': err_web.E_FORM_INVALID} #TODO for rest
    return render(request, 'web/login.html', invalid_form)
  
  post_data = form.cleaned_data
  post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
  req = urllib.request.Request('http://exp-api:8000/register', data=post_encoded, method='POST')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)

  if not resp:
    resp = err_web.E_TECH_DIFFICULTIES
    return render(request, 'web/t404.html', resp)

  if resp['ok'] == False: # could be much more nuanced. 
    resp = err_web.E_REGISTER_FAILED
    return render(request, 'web/login.html', resp)


  registration_success = "congrats, you've registered an account successfully! login to get started :)"
  return render(request, 'web/login.html', registration_success)



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
  req = urllib.request.Request('http://exp-api:8000/hi')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  if not resp:
    resp = err_web.E_TECH_DIFFICULTIES
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
      resp = err_web.E_TECH_DIFFICULTIES
      return render(request, 'web/t404.html', resp)

    if resp['resp']['ok'] == False:
      resp = err_web.E_DRONE_NOT_FOUND
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
      resp = err_web.E_TECH_DIFFICULTIES
      return render(request, 'web/t404.html', resp)

    if resp['resp']['ok'] == False:
      resp = err_web.E_USER_NOT_FOUND
      return render(request, 'web/t404.html', resp)
    
    resp2 = resp['resp']
    t = arrow.get(resp2['resp']['date_joined'])
    resp2['resp']['date_joined'] = str(t.format('D MMMM, YYYY') + " at " + t.format('h:mma'))

  return render(request, 'web/userprofile.html', resp2)
