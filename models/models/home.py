from django.http import HttpResponse
def index(request):
  return HttpResponse('<p><b>Models Homepage</b></p>')
