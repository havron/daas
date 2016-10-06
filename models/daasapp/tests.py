from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from . import models
from . import views
import json

class InspectUserTestCase(TestCase):
  def test_setUp(self):
    pass

  def test_success_response(self):
    response = self.client.get(reverse('inspect_user', kwargs={'user_id':1}))
    self.assertContains(response, 'ok')

  def test_fails_invalid(self):
    response = self.client.get(reverse('inspect_user', kwargs=None))
    self.assertEquals(response.status_code, 200)
    #self.assertJSONEqual(
      #json.loads(str(dict({"ok": json.loads(str(response.content, encoding='utf8'))["ok"]}))),
    #resp = json.loads(str(response.content, encoding='utf8'))
    resp = json.loads(response.content.decode('utf8'))
    self.assertEqual(resp["ok"],False)

  def test_tearDown(self): 
    pass              
