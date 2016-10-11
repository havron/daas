from django.shortcuts import render
import urllib.request
import urllib.parse
import json
from django.http import JsonResponse

################ RESPONSE HELPER FUNCTIONS #############

# _ denotes a helper function
def _success_response(request, resp=None):
  if resp:
    return JsonResponse({'ok': True, 'resp': resp})
  else:
   return JsonResponse({'ok': True})

# _ denotes a helper function
# EXP ERROR CODES DOCUMENTED IN 'error_codes_exp.txt'
def _error_response(request, error_msg, error_code=None):
   if error_code:
     return JsonResponse({'ok': False, 'error': error_msg, 'error_code': error_code})
   else:
     return JsonResponse({'ok': False, 'error': error_msg})


def hi(request):
  context = {} # can send dictionary values (results of api calls) to the template
  print ("About to do the GET...")
  req = urllib.request.Request('http://models-api:8000/api/v1/user/all')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  print(resp)
  return _success_response(request, resp)

def productdetails(request, drone_id):
  req = urllib.request.Request('http://models-api:8000/api/v1/drone/'+drone_id)
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  return _success_response(request, resp)

def userprofile(request, user_id):
  req = urllib.request.Request('http://models-api:8000/api/v1/user/'+user_id)
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  return _success_response(request, resp)
