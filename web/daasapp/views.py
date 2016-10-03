from django.shortcuts import render

def index(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/index.html', context)
def login(request):
  context = {} # can send dictionary values (results of api calls) to the template
  return render(request, 'web/login.html', context)
