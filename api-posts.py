# compact access to post request for updating APIs!
import json
import requests
import datetime


def makeNewUser(username, password, email_address):
  payload = {'username': username, 'password' : password, 'email_address' : email_address}
  r = requests.post("http://localhost:8000/api/v1/user/create", data=payload)

def updateUser(username, password, email_address, user_id): # should lookup id for instance pk
  payload = {'username': username, 'password' : password, 'email_address' : email_address}
  r = requests.post("http://localhost:8000/api/v1/user/" + user_id, data=payload)
  

def makeNewDrone(model_name, drone_desc, demo_link, permissions, owner_email, 
    last_checked_out, battery_level, maintenance_status, available_for_hire)

    payload = {'model_name':model_name, 'drone_desc':drone_desc, 'demo_link':demo_link,
    'permissions':permissions, 'owner_email':owner_email, 
    'last_checked_out':last_checked_out, 'battery_level':battery_level, 
    'maintenance_status':maintenance_status, 'available_for_hire':available_for_hire}
    r = requests.post("http://localhost:8000/api/v1/drone/create", data=payload)

def updateDrone(model_name, drone_desc, demo_link, permissions, owner_email, 
    last_checked_out, battery_level, maintenance_status, available_for_hire, drone_id)
    # should lookup id for instance pk

    payload = {'model_name':model_name, 'drone_desc':drone_desc, 'demo_link':demo_link,
    'permissions':permissions, 'owner_email':owner_email, 
    'last_checked_out':last_checked_out, 'battery_level':battery_level, 
    'maintenance_status':maintenance_status, 'available_for_hire':available_for_hire}
    r = requests.post("http://localhost:8000/api/v1/drone/" + drone_id, data=payload)

    #model_name = models.CharField(max_length=50)
    #drone_desc = models.TextField()
    #demo_link = models.URLField() # (link to photo gallery or videos)
    #permissions = models.CharField(max_length=50)
    #owner_email = models.EmailField()
    #last_checked_out = models.DateTimeField()
    #battery_level = models.FloatField()
    #maintenance_status = models.TextField()
    #available_for_hire = models.BooleanField()

makeNewDrone("oreo", "black and white, best drone ever", "http://www.2sly4u.com", "can do everything",
 "cooldude@awesome.net", date.today(), 56.6, "ready to roll", True)
