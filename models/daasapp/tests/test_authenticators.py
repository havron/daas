from django.test import TestCase, Client
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from .. import models
from .. import views
import json
import datetime
import random
import arrow
from django.contrib.auth import hashers
import hmac, os
from django.conf import settings  
#create new class
#fields = ['username', 'password', 'email_address','date_joined','is_active','f_name','l_name', 'bio']
class AuthForm(ModelForm): 
  class Meta:
    model = models.Authenticator
    fields = ['user_id', 'authenticator', 'date_created']

class AutheticatorFormTests(TestCase):

  fixtures = ['db']

  def setUp(self):
    pass


  def test_UserCreationLoginAuthenticationLogout(self):
    #creation
    form_data = {'username': 'abolish100','password': 'Lettish_fundamentalism100', 'email_address': 'conjugally_Guadalcanal100@equatorially.com','date_joined': datetime.datetime.now(),  'is_active': True, 'f_name': 'Mark', 'l_name': 'White','bio': "a zoonal" }
    form = views.UserForm(data=form_data)
    new_user = form.save(commit='false')
    new_user.save()
    print(new_user)
    print(models.User.objects.get(pk = 201))
    self.assertEquals(models.User.objects.get(pk = 201).username, 'abolish100')

    #password hash
    self.assertEquals(hashers.check_password('Lettish_fundamentalism100', models.User.objects.get(pk = 201).password), True)

    #login & authentication
    token = hmac.new(\
    key = settings.SECRET_KEY.encode('utf-8'), \
    msg = os.urandom(32), \
    digestmod='sha256').hexdigest()

    auth_payload = dict(user_id=new_user.pk, authenticator=token, date_created=datetime.datetime.now())
    auth_form = AuthForm(auth_payload)
    new_auth = auth_form.save(commit=False)
    new_auth.save()

    self.assertEquals(models.Authenticator.objects.get(pk = token).user_id, new_user.pk)

    #logout
    models.Authenticator.objects.get(pk = token).delete()
    self.assertEquals(models.Authenticator.objects.filter(pk = token).count(), 0)


  def tearDown(self): 
    pass   


