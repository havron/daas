from django.shortcuts import render
from django.http import HttpResponse
from webapp.models import User
from django.forms import ModelForm
from webapp.models import User
from django.http import JsonResponse
from django.db import IntegrityError
import json

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email_address']

def create_user(request):
    dictionary = {}
    if request.method == 'POST':
        #create a form to add an article
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                #new_user = form.save()
                print(form)
                dictionary = form
                '''
                u = models.User.(username=request.POST['username'],
                         password=request.POST['password'],
                         email_address=request.POST['email_address'])
                u.save()
                '''
            except IntegrityError as e:
                return HttpResponse("problem saving data")
        else:
            print(form.errors)


        return JsonResponse(dictionary)
    else:
        return HttpResponse("not working")
