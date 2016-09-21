from django.shortcuts import render
from django.http import HttpResponse
from webapp.models import User
from webapp.models import Drone
from django.forms import ModelForm
from django.http import JsonResponse
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import json
import os

class UserForm(ModelForm): # means to get user form data from keys
    class Meta:
        model = User
        fields = ['username', 'password', 'email_address']

class DroneForm(ModelForm): # drone form data from keys
    class Meta:
        model = Drone
        fields = ['model_name', 'drone_desc', 'demo_link', 'permissions', 'owner_email', 
    'last_checked_out', 'battery_level', 'maintenance_status', 'available_for_hire']

### USER VIEWS ###################
def all_user(request): # /api/v1/user/all
  if request.method == 'GET':
    for u in User.objects.all():
      print(u)
    return HttpResponse("Look at the log!")
  else:
        return HttpResponse("%s is not a valid request method. Use a GET request instead!" % request.method)

def inspect_user(request): # user id URL /api/v1/user/<id>
  user_id = os.path.basename(os.path.normpath(request.path))
  try:  # try to find the user specified at the URL and quit if they do not exist in the db
    user = User.objects.get(pk=user_id)
  except ObjectDoesNotExist as e:
    return HttpResponse('%s does not exist' % user_id)

  if request.method == 'GET':
    return HttpResponse(json.dumps(user.to_json()), content_type="application/json")
  else: # POST request
    form = UserForm(request.POST, instance=user) # magically updates the fields!
    if form.is_valid():
      user.save()
    else: 
      return HttpResponse(form.errors)
    return HttpResponse(json.dumps(user.to_json()), content_type="application/json")

def create_user(request): # /api/v1/user/create
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
          try:
            new_user = form.save(commit='false')
            new_user.save()
            return HttpResponse(json.dumps(new_user.to_json()), content_type="application/json")
          except IntegrityError as e:
              return HttpResponse("problem saving data")
        else:
            return HttpResponse(form.errors)
    else:
        return HttpResponse("%s is not a valid request method. Use a POST request instead!" % request.method)

#### DRONE VIEWS ##############
def all_drone(request): # /api/v1/drone/all
  if request.method == 'GET':
    for u in Drone.objects.all():
      print(u)
    return HttpResponse("Look at the server log!")
  else:
        return HttpResponse("%s is not a valid request method. Use a GET request instead!" % request.method)

def inspect_drone(request): # /api/v1/done/<id>
  drone_id = os.path.basename(os.path.normpath(request.path))
  try: # try to find the drone specified at the URL and quit if they do not exist in the db
    drone = Drone.objects.get(pk=drone_id)
  except ObjectDoesNotExist as e:
    return HttpResponse('%s does not exist' % drone_id)

  if request.method == 'GET':
    return HttpResponse(json.dumps(drone.to_json()), content_type="application/json")
  else: # POST request
    form = DroneForm(request.POST, instance=drone) # magically updates the fields!
    if form.is_valid():
      drone.save()
    else:
      return HttpResponse(form.errors)
    return HttpResponse(json.dumps(drone.to_json()), content_type="application/json")

def create_drone(request): # /api/v1/drone/create
    if request.method == 'POST':
        form = DroneForm(request.POST)
        if form.is_valid():
          try:
            new_drone = form.save(commit='false')
            new_drone.save()
            return HttpResponse(json.dumps(new_drone.to_json()), content_type="application/json")
          except IntegrityError as e:
              return HttpResponse("problem saving data")
        else:
            return HttpResponse(form.errors)
    else:
        return HttpResponse("%s is not a valid request method. Use a POST request instead!" % request.method)
