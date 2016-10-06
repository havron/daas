from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from . import models
from . import views

class GetDroneDetailsTestCase(TestCase):
	def test_setUp(self):
		pass
	def test_success_response(self):
		response = self.client.get(reverse('inspect_user', kwargs={'user_id':1}))
		self.assertContains(response, 'ok')
	def test_fails_invalid(self):
		response = self.client.get(reverse('inspect_user', kwargs=None))
		self.assertEquals(response.status_code, 404)
		#self.assertEquals(response.context['resp']['ok'], False)    #user_id not given in url, so error
	def test_tearDown(self): 
		pass              
