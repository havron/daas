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
        #print(request.POST)
        #create a form to add an article
        form = UserForm(request.POST)
        
        
        print(request.POST)
        for key in request.POST:

          #print(key)
          #print (1)
          v = request.POST[key]
          #print(v)
        if form.is_valid():
            print ("VALID!")
            try:
                new_user = form.save()
                print(form)
                dictionary = form

                #u = models.User(username=request.POST['username'],
                #         password=request.POST['password'],
                #         email_address=request.POST['email_address'])
                #u.save()
                return JsonResponse(dictionary)

            except IntegrityError as e:
                return HttpResponse("problem saving data")
        else:
            print ("NOOOOOOOOOOOOOOOOOOO VALID!")
            #print (form)
            # print (form.errors)
            return HttpResponse(form.errors)
    else:
        return HttpResponse("not working")
