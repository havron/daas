from django.shortcuts import render

def index(request):
  context = {} # can send dictionary values (results of API calls) to the template
  return render(request, 'web/index.html', context)
