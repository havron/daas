from django import forms
from django.forms import ModelForm
import json, datetime
from django import db
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
from django.http import JsonResponse
from daasapp import models
from daasapp import err_models
from django.conf import settings # for getting HMAC key from project settings
import hmac, os # for generating auth token
from random import randrange 

############### FORMS ###############
class UserForm(ModelForm): 
    class Meta:
        model = models.User
#        widgets = {
#          'password': forms.PasswordInput(),
#        }

        fields = ['username', 'password', 'email_address','date_joined','is_active','f_name','l_name', 'bio']

    def save(self, commit=True):
            user = super(UserForm, self).save(commit=False)

            if not hashers.is_password_usable(self.cleaned_data['password']):
              user.set_password(self.cleaned_data['password']) # implemented in models

            if commit:
                user.save()

            return user

class LoginForm(forms.Form): 
  username = forms.CharField()
  password = forms.CharField()
    # this form is never saved, only used to properly get username and pw fields

class UpdateUserForm(ModelForm): 
    class Meta:
        model = models.User
        fields = ['password', 'email_address','is_active','f_name','l_name', 'bio']

class AuthForm(ModelForm): 
  class Meta:
    model = models.Authenticator
    fields = ['user_id', 'authenticator', 'date_created']

class CheckAuthForm(forms.Form): 
  authenticator = forms.CharField()

class DroneForm(ModelForm): # currently not using this form ... see create_drone()
    owner = forms.ModelChoiceField(queryset=models.User.objects.all())
    class Meta:
        model = models.Drone
    #    fields = ['model_name', 'drone_desc', 'demo_link', 'permissions', 'owner_email', 
    #    'battery_level', 'maintenance_status', 'available_for_hire', 'owner','last_checked_out']
        exclude = ['owner','_owner_key']

class UpdateDroneForm(ModelForm):
    class Meta:
        model = models.Drone
        fields = ['drone_desc', 'demo_link', 'permissions', 'battery_level', 
        'maintenance_status', 'available_for_hire', 'last_checked_out']

# note: multiple form classes (with different names) for a model can be made, 
# with different subsets of fields accepted or excluded

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
    return JsonResponse({'ok': True, 'resp': resp,'model_machine':os.environ['DB_NAME'][1:-3]})
  else:
   return JsonResponse({'ok': True,'model_machine':os.environ['DB_NAME'][1:-3]})

# _ denotes a helper function
# MODEL ERROR CODES DOCUMENTED IN 'err_models.py'
def _error_response(request, error_msg, error_specific=None):
   if error_specific:
     return JsonResponse({'ok': False, 'error': error_msg, 'error_info': error_specific,'model_machine':os.environ['DB_NAME'][1:-3]})
   else:
     return JsonResponse({'ok': False, 'error': error_msg, 'model_machine':os.environ['DB_NAME'][1:-3]})


############# USER APIs ###################
def machine(request):
  return JsonResponse({'model_machine':os.environ['DB_NAME'][1:-3]})


def create_user(request): # /api/v1/user/create
    if request.method != 'POST':
      return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")
    
    form = UserForm(request.POST)
    if not form.is_valid():
      return _error_response(request, err_models.E_FORM_INVALID, "missing required fields")  

    if not hashers.is_password_usable(form.cleaned_data['password']):
      return _error_response(request, err_models.E_FORM_INVALID, "password is not hashed")

    new_user = form.save(commit='false')

    try:
      new_user.save()
    except db.Error:
      return _error_response(request, err_models.E_DATABASE, 'could not save user data')

    return _success_response(request, {'user_id': new_user.pk})


def login_user(request): # /api/v1/user/login
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")

  form = LoginForm(request.POST)
  if not form.is_valid():
    #return _error_response(request, err_models.E_FORM_INVALID, "exp service did not supply valid login credentials")
    return _error_response(request, form.errors, "exp service did not supply valid login credentials")

  try:
    u = models.User.objects.get(username=form.cleaned_data['username'])
  except models.User.DoesNotExist:
    return _error_response(request, err_models.E_LOGIN_FAILED, "could not find user with supplied username...")

  if not hashers.check_password(form.cleaned_data['password'], u.password):
    return _error_response(request, err_models.E_LOGIN_FAILED, "password not correct")

  token = hmac.new(\
    key = settings.SECRET_KEY.encode('utf-8'), \
    msg = os.urandom(32), \
    digestmod='sha256').hexdigest()

  auth_payload = dict(user_id=u.pk, authenticator=token, date_created=datetime.datetime.now())
  auth_form = AuthForm(auth_payload)

  if not auth_form.is_valid():
    return _error_response(request, err_models.E_FORM_INVALID, "authenticator failed to form")

  new_auth = auth_form.save(commit=False)

  try:
    new_auth.save()
  except db.Error:
    return _error_response(request, err_models.E_DATABASE, "could not save new authenticator")

  return _success_response(request, new_auth.to_json())


def logout_user(request): # /api/v1/user/logout
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")

  form = CheckAuthForm(request.POST)
  if not form.is_valid():
    return _error_response(request, form.errors, "auth token form not filled out correctly")
    #return _error_response(request, err_models.E_FORM_INVALID, "auth token form not filled out correctly")

  data = form.cleaned_data
  try:
    auth = models.Authenticator.objects.get(pk=data['authenticator'])
  except models.Authenticator.DoesNotExist:
    return _error_response(request, err_models.E_UNKNOWN_AUTH, "authenticator not found")

  # currently not being checked due to cookies never remembering username...
  #if data['user_id'] != auth.user_id: # prevent a user from logging out another user
  #  return _error_response(request, err_models.E_UNKNOWN_AUTH, "invalid user")

  try:
    auth.delete()
  except db.Error:
    return _error_response(request, err_models.E_DATABASE, "could not delete auth token")

  return _success_response(request, "logged out successfully")


def check_auth_user(request): # /api/v1/user/auth
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")

  form = CheckAuthForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_models.E_FORM_INVALID, "auth token form not filled out correctly")

  data = form.cleaned_data
  try:
    auth = models.Authenticator.objects.get(pk=data['authenticator'])
  except models.Authenticator.DoesNotExist:
    return _error_response(request, err_models.E_UNKNOWN_AUTH, "authenticator not found")

# causes error...cookie deletion not synchronized?
#   if datetime.datetime.now() - auth.date_created > datetime.timedelta(days=1):
#     try:
#       auth.delete()
#     except db.Error:
#       return _error_response(request, err_models.E_DATABASE, "could not delete expired authenticator")
#     return _error_response(request, err_models.E_UNKNOWN_AUTH, "authenticator expired")

  # currently not being checked due to cookies never remembering username...
  #if data['user_id'] != auth.user_id:
  #  return _error_response(request, err_models.E_UNKNOWN_AUTH, "invalid user")

  # date expiration check in experience layer
  return _success_response(request, auth.to_json()) # gives exp layer the date_created



def inspect_user(request, user_id): # /api/v1/user/<user_id>
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")

  try:
    u = models.User.objects.get(pk=user_id)
  except models.User.DoesNotExist:
    return _error_response(request, err_models.E_DATABASE, "user not found")

  return _success_response(request, u.to_json()) 
 

def update_user(request, user_id): # /api/v1/user/<user_id>/update
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")

  try:
    u = models.User.objects.get(pk=user_id)
  except models.User.DoesNotExist:
    return _error_response(request, err_models.E_DATABASE, "user not found")

  form = UpdateUserForm(request.POST, instance=u) # magically updates the fields!
  if not form.is_valid():
    return _error_response(request, err_models.E_FORM_INVALID, "user fields not updated, form error")

  form.save()
  
  return _success_response(request,u.to_json())


def all_users(request): # /api/v1/user/all
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")

  users = {}
  for u in models.User.objects.all():
    users.update({u.id : u.to_json()})
  return _success_response(request, users)


def recent_givers(request): # /api/v1/user/recent_givers
  if request.method != 'GET': 
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")

  givers = []
  try:
    ts = _recent_drones()
    for t in ts:
      u = models.User.objects.get(pk=t['owner'])
      givers.append(model_to_dict(u))
  except db.Error:
    return _error_response(request, err_models.E_DATBASE, "db error while retrieving users")

  return _success_response(request, {'recent_givers': givers})


########## DRONE APIs ##############
def create_drone(request): # /api/v1/drone/create
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")
  
  if( not request.POST.get('auth')):
    try:
      owner = models.User.objects.get(pk=request.POST['_owner_key']) # not efficient, assumes pk is passed in
    except models.User.DoesNotExist:
      return _error_response(request, err_models.E_DATABASE, "owner not found")
  else:
    form = CheckAuthForm(dict(authenticator=request.POST['auth']))
    if not form.is_valid():
      return _error_response(request, err_models.E_FORM_INVALID, "auth token form not filled out correctly")

    data = form.cleaned_data
    try:
      auth = models.Authenticator.objects.get(pk=data['authenticator'])
    except models.Authenticator.DoesNotExist:
      return _error_response(request, err_models.E_UNKNOWN_AUTH, "authenticator not found")

    try:
      owner = models.User.objects.get(pk=auth.user_id) # not efficient, assumes pk is passed in
    except models.User.DoesNotExist:
      return _error_response(request, err_models.E_DATABASE, "owner not found")


  ######### attempt at using a form to populate. Foreignkey is tough to deal with.
  #  form = DroneForm(initial={'owner':owner.pk})
  #
  #  if form.is_valid():
  #    new_drone = form.save(commit=False)
  #    if not new_drone.owner:
  #      new_drone.owner = owner
  #  else:
  #    return _error_response(request, "missing required fields")  
  #
  #  try:
  #    new_drone.save()
  #  except db.Error:
  #      return _error_response(request, "db error")

  d = models.Drone(model_name=request.POST['model_name'], \
                   drone_desc=request.POST['drone_desc'], \
                   demo_link=request.POST['demo_link'], \
                   permissions=request.POST['permissions'], \
                   owner_email=owner.email_address, \
                   battery_level=request.POST['battery_level'], \
                   maintenance_status=request.POST['maintenance_status'], \
                   available_for_hire=request.POST['available_for_hire'], \
                   owner=owner, \
                   last_checked_out=request.POST['last_checked_out'], \
                  )
  try:
    d.save()
  except db.Error:
    return _error_response(request, err_models.E_DATABASE, "db error occurred while saving drone data")

  return _success_response(request, {'drone_id': d.pk})


def inspect_drone(request, drone_id): # /api/v1/drone/<drone_id>
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")

  try:
    d = models.Drone.objects.get(pk=drone_id)
  except models.Drone.DoesNotExist:
    return _error_response(request, err_models.E_DATABASE, "drone not found")

  return _success_response(request, d.to_json()) 


def update_drone(request, drone_id): # /api/v1/drone/<drone_id>/update
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")

  try:
    d = models.Drone.objects.get(pk=drone_id)
  except models.Drone.DoesNotExist:
    return _error_response(request, err_models.E_DATABASE, "drone not found")

  form = UpdateDroneForm(request.POST, instance=d) # magically updates the fields!
  if not form.is_valid():
    return _error_response(request, err_models.E_FORM_INVALID, "drone fields not updated, form error")
  form.save()
  
  return _success_response(request,d.to_json())


def all_drones(request): # /api/v1/drone/all
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")

  drones = {}
  for d in models.Drone.objects.all():
    print(d)
    drones.update({d.id : d.to_json()})
  return _success_response(request, drones)


# _ denotes a helper function
def _recent_drones():
  ts = models.Drone.objects.order_by('last_checked_out')[:3]
  ts = list(map(model_to_dict, ts))
  return ts

def recent_drones(request): # /api/v1/drone/recent
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")

  try:
    ts = _recent_drones()
  except db.Error:
    return _error_response(request, err_models.E_DATABASE, "recent drones not found")

  return _success_response(request, {'recent_things': ts})



#############listings api ####################

def create_listing(request): # /api/v1/listing/create
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")
  
  if( not request.POST.get('auth')):
    try:
      owner = models.User.objects.get(pk=request.POST['_owner_key']) # not efficient, assumes pk is passed in
    except models.User.DoesNotExist:
      return _error_response(request, err_models.E_DATABASE, "owner not found")
  else:
    form = CheckAuthForm(dict(authenticator=request.POST['auth']))
    if not form.is_valid():
      return _error_response(request, err_models.E_FORM_INVALID, "auth token form not filled out correctly")

    data = form.cleaned_data
    try:
      auth = models.Authenticator.objects.get(pk=data['authenticator'])
    except models.Authenticator.DoesNotExist:
      return _error_response(request, err_models.E_UNKNOWN_AUTH, "authenticator not found")

    try:
      owner = models.User.objects.get(pk=auth.user_id) # not efficient, assumes pk is passed in
    except models.User.DoesNotExist:
      return _error_response(request, err_models.E_DATABASE, "owner not found")



  try:
    drone = models.Drone.objects.get(pk=request.POST['_drone_key']) # not efficient, assumes pk is passed in
  except models.Drone.DoesNotExist:
    return _error_response(request, err_models.E_DATABASE, "drone not found")

  l = models.Listing(owner=owner, \
                      drone = drone, \
                      price_per_day=request.POST['price_per_day'], \
                      time_posted=request.POST['time_posted'], \
                      description=request.POST['description'], \
                      #listing_status=request.POST['listing_status'], \ # need to implement
                  )
  try:
    l.save()
  except db.Error:
    return _error_response(request, err_models.E_DATABASE, "db error occurred while saving listing data")

  return _success_response(request, {'listing_id': l.pk, 'listing': l.to_json()})




def inspect_listing(request, listing_id): # /api/v1/listing/<listing_id>
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")
 
  try:
    d = models.Listing.objects.get(pk=listing_id)
  except models.Listing.DoesNotExist:
    return _error_response(request, err_models.E_DATABASE, "listing not found")

  return _success_response(request, d.to_json()) 



def my_drones(request): # /api/v1/my_drones
  if request.method != 'POST':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make POST request")

  form = CheckAuthForm(request.POST)
  if not form.is_valid():
    return _error_response(request, err_models.E_FORM_INVALID, "auth token form not filled out correctly")

  data = form.cleaned_data
  try:
    auth = models.Authenticator.objects.get(pk=data['authenticator'])
  except models.Authenticator.DoesNotExist:
    return _error_response(request, err_models.E_UNKNOWN_AUTH, "authenticator not found")

  try:
    owner = models.User.objects.get(pk=auth.user_id)  
  except models.User.DoesNotExist:
    return _error_response(request, err_models.E_UNKNOWN_AUTH, "User not found")

  try:
    my_drones = models.Drone.objects.filter(owner=owner)
  except models.Drone.DoesNotExist:
    return _error_response(request, err_models.E_UNKNOWN_AUTH, "drones not found")

  # currently not being checked due to cookies never remembering username...
  #if data['user_id'] != auth.user_id:
  #  return _error_response(request, err_models.E_UNKNOWN_AUTH, "invalid user")

  # date expiration check in experience layer
  drone_dict = [ drone.to_json() for drone in my_drones ]
  return _success_response(request, {'resp': { 'my_drones': drone_dict }}) # gives exp layer the date_created


#doesn't work
def all_listing(request): # /api/v1/listing/all
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")
  return _success_response(request, {'resp': 'good'})



def featured_items(request): # /api/v1/shop/
  if request.method != 'GET':
    return _error_response(request, err_models.E_BAD_REQUEST, "must make GET request")

  listing1 = random.randrange(1, 201)
  try:
    l1 = models.Listing.objects.get(pk=listing1)
  except models.Listing.DoesNotExist:
    return _error_response(request, err_models.E_DATABASE, "listing not found")
  # dict(l1=l1.to_json(), L2=
  return _success_response(request, l1.to_json()) 
