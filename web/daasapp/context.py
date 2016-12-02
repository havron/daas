import os
import urllib.request
import urllib.parse
import json


# ASSUMES LEGACY DOCKER-COMPOSE 1 IS BEING USED TO LOAD ENV LINK VARIABLES
def web_machine(request):
  return {'web_machine': os.environ['EXPBAL_NAME'][1:-7]} # find the container HAProxy picked!

def api_machines(request): 
  # the actual exp/model machine at a given time is based on 
  # individual service requests, so this context request
  # might not really be the machines that were used...
  # json for any service request returns machine used, so 
  # that could be fully integrated across views.py!
  # also, this is super inefficient and makes a request to exp/models on every page load :(
  req = urllib.request.Request('http://exp-api:8000/machine/')
  resp_json = urllib.request.urlopen(req).read().decode('utf-8')
  resp = json.loads(resp_json)
  if not resp:
    return {'exp_machine': 'exp machine not found','model_machine': 'model machine not found'}

  return {'exp_machine': resp['exp_machine'], 'model_machine':resp['model_machine']} # find the containers HAProxy picked!
