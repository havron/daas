# compact access to post request for updating APIs!
import json
import requests


username = 'joe'
password = 'rofl'

email_address = 'jo@b.in'

#maybe user_id isn't the best name?
user_id = 2
url = "http://localhost:8000/api/v1/user/" + str(user_id) + '/'

r = requests.get(url)
r.status_code
print(r.text)




