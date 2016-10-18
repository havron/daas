from django.test import TestCase, Client
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from .. import models
from .. import views
import json
import datetime
import random
import arrow

class ListingFormTests(TestCase):
  fixtures = ['db']  # load from DB

  def setUp(self):
    self.client = Client()

    form_data = {'_owner_key': 50, 
    			'_drone_key': 50,
    			'price_per_day': 10.50,
    			'time_posted': datetime.datetime.now(),
    			'description': "lsjlerjl",
    			'listing_status': 'available'
    }

    response = self.client.post(reverse('create_listing'), form_data)
    print("test_create_listing POST " + str(response))

    resp = json.loads(response.content.decode('utf8'))
    self.assertEquals(response.status_code, 200)
    print("listing_atts" + str(resp))

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