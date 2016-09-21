# compact access to post request for updating APIs!
import json
import requests


username = 'new'
password = 'rlol'
email_address = 'm@m.me'
url = '/api/v1/user/19'


payload = {'username': username, 'password' : password, 'email_address' : email_address}
r = requests.post("http://localhost:8000" + url, data=payload)
#print(r.text)
