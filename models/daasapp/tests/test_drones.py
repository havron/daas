from django.test import TestCase, Client
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from .. import models
from .. import views
import json
import datetime
import random

class DroneFormTests(TestCase):
  fixtures = ['db']  # load from DB

  def setUp(self):
    self.client = Client()

    form_data = {'_owner_key': 50, 'drone_desc': 'velutinous peg-top Mesopotamia rakees lecherously and 100.', 
    #'drone_id': 100, 
    'demo_link': 'http://demo_pacific100.com', 
    'last_checked_out': datetime.datetime.now(), 
    #owner': {'user_id': 300, 'f_name': 'Mark', 'date_joined': datetime.datetime.now(), 'email_address': 'conjugally_Guadalcanal100@equatorially.com', 'username': 'abolishputamen100', 'bio': "a little about me: I'm pitter-patter, limiting, zoonal, ", 'l_name': 'White', 'is_active': True, 'password': 'Lettish_fundamentalism100'},
    'permissions': 'you can this and wintery with my drone, but NOT pygmoid, or 100.', 
    'maintenance_status': "my drone is in great condition! 100.", 
    'available_for_hire': True, 
    'owner_email': 'tactic100@nautically.com', 
    'battery_level': 100.0, 
    'model_name': 'prehistorians_inexpugnably100' }

    response = self.client.post(reverse('create_drone'), form_data)
    print("test_create_drone POST " + str(response))

    resp = json.loads(response.content.decode('utf8'))
    self.assertEquals(response.status_code, 200)
    print("drone_atts" + str(resp))

  # append number to test to get python to run defs in correct order
  def test1_DroneForm(self):

    response = self.client.get(reverse('inspect_drone', kwargs={'drone_id':201}))
    resp = json.loads(response.content.decode('utf8'))

    print("test_drone_attributes GET " + str(resp))
    self.assertEquals(resp["ok"],True)
    self.assertEquals(resp['resp']['model_name'], 'prehistorians_inexpugnably100')

  def test2_Drone_Invalid_id(self):
    response = self.client.get(reverse('inspect_drone', kwargs={'drone_id':300}))
    resp = json.loads(response.content.decode('utf8'))
    self.assertEquals(resp["ok"], False)

  # Unit Test for User Story 6
  def test3_Most_Recent_Drones(self):
    response = self.client.get(reverse('recent_drones'))
    resp = json.loads(response.content.decode('utf8'))
    print(str(resp) + "----------------------------")
    self.assertEquals(len(list(resp['resp']['recent_things'])), 3)

  def tearDown(self): 
    del self.client