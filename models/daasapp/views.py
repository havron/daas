from django import forms
from django.forms import ModelForm
import json, datetime
from django import db
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
from django.http import JsonResponse
from . import models

############### FORMS ###############
class UserForm(ModelForm): 
    class Meta:
#        password = forms.CharField(widget=forms.PasswordInput)
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

class UpdateUserForm(ModelForm): 
    class Meta:
        model = models.User
        fields = ['password', 'email_address','is_active','f_name','l_name', 'bio']


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


################ RESPONSE HELPER FUNCTIONS #############

# _ denotes a helper function
def _success_response(request, resp=None):
  if resp:
    return JsonResponse({'ok': True, 'resp': resp})
  else:
   return JsonResponse({'ok': True})

# _ denotes a helper function
# MODEL ERROR CODES DOCUMENTED IN 'error_codes_models.txt'
def _error_response(request, error_msg, error_code=None):
   if error_code:
     return JsonResponse({'ok': False, 'error': error_msg, 'error_code': error_code})
   else:
     return JsonResponse({'ok': False, 'error': error_msg})


############# USER APIs ###################
def create_user(request): # /api/v1/user/create
    if request.method != 'POST':
      return _error_response(request, "must make POST request", 1)
    
    form = UserForm(request.POST)
    if not form.is_valid():
      return _error_response(request, "missing required fields", 2)  

    if not hashers.is_password_usable(form.cleaned_data['password']):
      return _error_response(request, str("password "+form.cleaned_data['password']+" is not hashed"),4)

    new_user = form.save(commit='false')

    try:
      new_user.save()
    except db.Error:
      return _error_response(request, "db error occurred while saving user's data", 3)

    return _success_response(request, {'user_id': new_user.pk})


def inspect_user(request, user_id): # /api/v1/user/<user_id>
  if request.method != 'GET':
    return _error_response(request, "must make GET request", 1)

  try:
    u = models.User.objects.get(pk=user_id)
  except models.User.DoesNotExist:
    return _error_response(request, "user not found", 3)

  return _success_response(request, u.to_json()) 
 

def update_user(request, user_id): # /api/v1/user/<user_id>/update
  if request.method != 'POST':
    return _error_response(request, "must make POST request", 1)

  try:
    u = models.User.objects.get(pk=user_id)
  except models.User.DoesNotExist:
    return _error_response(request, "user not found", 3)

  form = UpdateUserForm(request.POST, instance=u) # magically updates the fields!
  if not form.is_valid():
    return _error_response(request, "user fields not updated, form error", 2)

  form.save()
  
  return _success_response(request,u.to_json())


def all_users(request): # /api/v1/user/all
  if request.method != 'GET':
    return _error_response(request, "must make GET request", 1)

  users = {}
  for u in models.User.objects.all():
    users.update({u.id : u.to_json()})
  return _success_response(request, users)


def recent_givers(request): # /api/v1/user/recent_givers
  if request.method != 'GET': 
    return _error_response(request, "must make GET request", 1)

  givers = []
  try:
    ts = _recent_drones()
    for t in ts:
      u = models.User.objects.get(pk=t['owner'])
      givers.append(model_to_dict(u))
  except db.Error:
    return _error_response(request, "db error while retrieving users", 3)

  return _success_response(request, {'recent_givers': givers})


########## DRONE APIs ##############
def create_drone(request): # /api/v1/drone/create
  if request.method != 'POST':
    return _error_response(request, "must make POST request", 1)
  
  try:
    owner = models.User.objects.get(pk=request.POST['_owner_key']) # not efficient, assumes pk is passed in
  except models.User.DoesNotExist:
    return _error_response(request, "owner not found", 3)
 

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
                   owner_email=request.POST['owner_email'], \
                   battery_level=request.POST['battery_level'], \
                   maintenance_status=request.POST['maintenance_status'], \
                   available_for_hire=request.POST['available_for_hire'], \
                   owner=owner, \
                   last_checked_out=request.POST['last_checked_out'], \
                  )
  try:
    d.save()
  except db.Error:
    return _error_response(request, "db error occurred while saving drone data", 3)

  return _success_response(request, {'drone_id': d.pk})


def inspect_drone(request, drone_id): # /api/v1/drone/<drone_id>
  if request.method != 'GET':
    return _error_response(request, "must make GET request", 1)

  try:
    d = models.Drone.objects.get(pk=drone_id)
  except models.Drone.DoesNotExist:
    return _error_response(request, "drone not found", 3)

  return _success_response(request, d.to_json()) 


def update_drone(request, drone_id): # /api/v1/drone/<drone_id>/update
  if request.method != 'POST':
    return _error_response(request, "must make POST request", 1)

  try:
    d = models.Drone.objects.get(pk=drone_id)
  except models.Drone.DoesNotExist:
    return _error_response(request, "drone not found", 3)

  print(request.POST)
  form = UpdateDroneForm(request.POST, instance=d) # magically updates the fields!
  if not form.is_valid():
    print(form.errors)
    return _error_response(request, "drone fields not updated, form error", 2)
  form.save()
  
  return _success_response(request,d.to_json())


def all_drones(request): # /api/v1/drone/all
  if request.method != 'GET':
    return _error_response(request, "must make GET request", 1)

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
    return _error_response(request, "must make GET request", 1)

  try:
    ts = _recent_drones()
  except db.Error:
    return _error_response(request, "db error", 3)

  return _success_response(request, {'recent_things': ts})
