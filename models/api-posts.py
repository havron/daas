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
  

def makeNewDrone(model_name, drone_desc, demo_link, permissions, owner_email, last_checked_out, battery_level, maintenance_status, available_for_hire):

    payload = {'model_name':model_name, 'drone_desc':drone_desc, 'demo_link':demo_link,
    'permissions':permissions, 'owner_email':owner_email, 
    'last_checked_out':last_checked_out, 'battery_level':battery_level, 
    'maintenance_status':maintenance_status, 'available_for_hire':available_for_hire}
    r = requests.post("http://localhost:8000/api/v1/drone/create", data=payload)

def updateDrone(model_name, drone_desc, demo_link, permissions, owner_email, 
    last_checked_out, battery_level, maintenance_status, available_for_hire, drone_id):
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

###### MAKE POST REQUEST CALLS HERE ######################

# do not run unless you have flushed the database.
for i in range(0,100):
  makeNewUser("user"+str(i),"password"+str(i),"email"+str(i)+"@email.com")

for i in range(0,100):
  makeNewDrone("model"+str(i),"description"+str(i),"http://demolink"+str(i)+".com","permissions"+str(i),"owneremail"+str(i)+"@email.com",
  "lastcheckedout"+str(i), i,"maintenancestatus"+str(i),True)


### make calls to the other methods for simple POST request management : the fields are 
# all strings at the moment, so you can fill them with dummy values.
