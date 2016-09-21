# compact access to post request for updating APIs!
import json
import requests


username = 'acjhad'
password = 'lol'
email_address = 'm@m.me'

payload = {'username': username, 'password' : password, 'email_address' : email_address}
r = requests.post("http://localhost:8000/api/v1/user/create", data=payload)
print(r.text)
