from django.shortcuts import render
from django.template.loader import get_template

def index(request):
  context = {} # can send dictionary values (results of API calls) to the template
  return render('index.html', context)
