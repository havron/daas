# compact access to post request for updating APIs!
import requests
import datetime
from django.utils import timezone

from django.forms import ModelForm
from django.forms import Form

import json, datetime, os
from django import db
from django.forms.models import model_to_dict
from django.contrib.auth import hashers
from django.http import JsonResponse
from daasapp import models
from daasapp import views

################ RESPONSE HELPER FUNCTIONS #############

# _ denotes a helper function
def _success_response(request, resp=None):
  if resp:
    return JsonResponse({'ok': True, 'resp': resp})
  else:
   return JsonResponse({'ok': True})

# _ denotes a helper function
def _error_response(request, error_msg):
    return JsonResponse({'ok': False, 'error': error_msg})


url = "http://localhost:8000/"

def _makeNewUser(username, password, email_address, date_joined, is_active, f_name, l_name):
  payload = {'username': username, 'password' : password, 'email_address' : email_address, 
  'date_joined': date_joined, 'is_active': is_active, 'f_name': f_name, 'l_name': l_name}
  
  r = requests.post(url+"api/v1/user/create", data=payload)

def _updateUser(user_id, password, email_address, is_active, f_name, l_name):
  payload = {'password' : password, 'email_address' : email_address, 
  'is_active': is_active, 'f_name': f_name, 'l_name': l_name}
  
  r = requests.post(url+"api/v1/user/"+user_id+"/update", data=payload)


def _makeNewDrone(model_name, drone_desc, demo_link, permissions, owner_email, battery_level, 
   maintenance_status, available_for_hire, owner, last_checked_out, _owner_key):

    payload = {'model_name':model_name, 'drone_desc':drone_desc, 'demo_link':demo_link,
    'permissions':permissions, 'owner_email':owner_email, 
     'battery_level':battery_level, 
    'maintenance_status':maintenance_status, 'available_for_hire':available_for_hire, 'owner': owner, 
    'last_checked_out':last_checked_out,'_owner_key':_owner_key}
    
    r = requests.post(url+"api/v1/drone/create", data=payload)


def _updateDrone(drone_id, drone_desc, demo_link, permissions, battery_level, 
   maintenance_status, available_for_hire, last_checked_out):

    payload = {'drone_desc':drone_desc, 'demo_link':demo_link,
    'permissions':permissions, 
     'battery_level':battery_level, 
    'maintenance_status':maintenance_status, 'available_for_hire':available_for_hire, 
    'last_checked_out':last_checked_out}
    
    r = requests.post(url+"api/v1/drone/"+drone_id+"/update", data=payload)


###### MAKE POST REQUEST CALLS HERE ######################



# do not run unless you have flushed the database
def populate(request):
  try:
    for i in range(0,100):
      _makeNewUser("user"+str(i),"password"+str(i),"email"+str(i)+"@email.com", datetime.datetime.now(), True, "firstname"+str(i), "lastname"+str(i))

    for i in range(0,100):
      try:
        owner = models.User.objects.get(pk=i+1)
      except models.User.DoesNotExist:
        return _error_response(request, "error finding user"+str(i))

      _makeNewDrone("model"+str(i),"description"+str(i),"http://demolink"+str(i)+".com","permissions"+str(i),"owneremail"+str(i)+"@email.com",
      i,"maintenancestatus"+str(i),True, owner, timezone.now(), str(i+1) )

  except db.Error:
    return _error_response(request, "db error")

  return _success_response(request, "populated the database")

def updateUser(request, user_id): # updates a user
  u_id = int(user_id)
  u_id -= 1
  u_id = str(u_id)
  try:
    u = models.User.objects.get(pk=user_id)
  except models.User.DoesNotExist:
    return _error_response(request, "user not found")
 
  try:
    _updateUser(user_id, "Updatedpassword"+u_id, "Updatedemail"+u_id+"@email.com", True, "Upfirstname"+u_id, u.l_name)
  except db.Error:
    return _error_response(request, "db error")
  return _success_response(request, "user successfully updated")


def updateDrone(request, drone_id): # updates a drone
  d_id = int(drone_id)
  d_id -= 1
  d_id = str(d_id)
  try:
    d = models.Drone.objects.get(pk=drone_id)
  except models.Drone.DoesNotExist:
    return _error_response(request, "drone not found")
 
  try:
    _updateDrone(drone_id, "newdescription"+d_id, "http://newdemo"+d_id+".com", "newperms"+d_id, str(int(d_id)+5),"newmaintenancesta"+d_id,True,datetime.datetime.now())
  except db.Error:
    return _error_response(request, "db error")
  return _success_response(request, "drone successfully updated")


### make calls to the other methods for simple POST request management : the fields are 
# all strings at the moment, so you can fill them with dummy values.
