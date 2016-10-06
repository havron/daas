from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from . import models
from . import views
import json

#create new class
#fields = ['username', 'password', 'email_address','date_joined','is_active','f_name','l_name', 'bio']

class InspectUserTestCase(TestCase):

  def setUp(self):
    c = Client()
    response = c.post(reverse('create_user'), 
      {'f_name': 'Mark', 'date_joined': '2000-08-31T08:23:47.652Z', 'email_address': 'conjugally_Guadalcanal100@equatorially.com', 'username': 'abolishputamen100', 'bio': "a zoonal", 'l_name': 'White', 'is_active': True, 'password': 'Lettish_fundamentalism100'
      })
    resp = json.loads(response.content.decode('utf8'))
    print("setUp " + str(resp))
      
  def test_user_attributes(self):
    #add users
    c = Client()
    #response = c.post(reverse('create_user'), 
    #  {'user_id': 1, 'f_name': 'Mark', 'date_joined': '2000-08-31T08:23:47.652Z', 'email_address': 'conjugally_Guadalcanal100@equatorially.com', 'username': 'abolishputamen201', 'bio': "a little about me: I'm pitter-patter, limiting, zoonal, ", 'l_name': 'White', 'is_active': True, 'password': 'Lettish_fundamentalism100',
    #  })
    
    #self.assertEquals(response.status_code, 200)
    response = c.get(reverse('inspect_user', kwargs={'user_id':100}))
    resp = json.loads(response.content.decode('utf8'))
    print("test_user_attributes " + resp)
    #print('monica')
    self.assertEquals(resp["ok"],True)
    self.assertEquals(resp['resp']['f_name'], 'Mark')
    

  def test_success_response(self):
    response = self.client.get(reverse('inspect_user', kwargs={'user_id':100}))
    resp = json.loads(response.content.decode('utf8'))
    print("test_success_response " + resp)
    self.assertEquals(resp["ok"],True)

  def test_fails_invalid(self):
    response = self.client.get(reverse('inspect_user', kwargs=None))
    self.assertEquals(response.status_code, 200)
    #self.assertJSONEqual(
      #json.loads(str(dict({"ok": json.loads(str(response.content, encoding='utf8'))["ok"]}))),
    #resp = json.loads(str(response.content, encoding='utf8'))
    resp = json.loads(response.content.decode('utf8'))
    print("test_fails_invalid " + resp)
    self.assertEquals(resp["ok"],False)

  def tearDown(self): 
    pass   


  #experience tests bonus
  #this project is read ony?
  #test reading users
  #given user with index 1, verify name of user at index 1 is correct
  #given 10 users, make reading 11th gives correct error    
'''
  def test_user_attributes(self):
    response = self.client.get(reverse('inspect_user', kwargs={'user_id':100}))
    resp = json.loads(response.content.decode('utf8'))
    print(resp)
    print('monica')
    self.assertEquals(resp['payload']['f_name'], 'Mark')
    '''



'''
{'drone_desc': 'velutinous peg-top Mesopotamia rakees lecherously and 100.', 
      'drone_id': 100, 
      'demo_link': 'http://demo_pacific100.com', 
      'last_checked_out': '5 October, 2016 at 8:24am', 
      'owner': {'user_id': 100, 'f_name': 'Mark', 'date_joined': '2000-08-31T08:23:47.652Z', 'email_address': 'conjugally_Guadalcanal100@equatorially.com', 'username': 'abolishputamen100', 'bio': "a little about me: I'm pitter-patter, limiting, zoonal, ", 'l_name': 'White', 'is_active': True, 'password': 'Lettish_fundamentalism100'},
      'permissions': 'you can this and wintery with my drone, but NOT pygmoid, or 100.', 
      'maintenance_status': "my drone is in great condition! 100.", 
      'available_for_hire': True, 
      'owner_email': 'tactic100@nautically.com', 
      'battery_level': 100.0, 
      'model_name': 'prehistorians_inexpugnably100'
      })
      '''
