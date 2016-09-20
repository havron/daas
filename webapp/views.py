from django.shortcuts import render
from django.http import HttpResponse
from models import User
import json

def create_user(request):
    dictionary = {}
    if request.method == 'POST':
        u = models.User.(username=request.POST['username'],
                         password=request.POST['password'],
                         email_address=request.POST['email_address'])
        u.save()
    #return render(request, 'index.html', dictionary)