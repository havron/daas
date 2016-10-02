from django.http import HttpResponse
from django.shortcuts import render
import time

def index(request):
  localtime = time.asctime( time.localtime(time.time()) )
  context = {'the_time':localtime}
  return HttpResponse('<p>"Web: Our lives begin to end the day we become silent about things that matter." - Martin Luther King Jr.</p>')
