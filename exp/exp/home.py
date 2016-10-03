from django.http import HttpResponse
def index(request):
  return HttpResponse('<p><b>Experience API Homepage</b></p>')
