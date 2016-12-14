# automatically creates access log entries, verified for correctness 
# as only odd and even item IDs get coclicked!
from faker import Factory
from random import randrange, getrandbits

##### parameters, adjust as desired
USERS = 10
MAX_CLICKS_PER_USER = 50
URL_ID_MIN = 1
URL_ID_MAX = 20

fake = Factory.create()
out = []
for i in range(0,USERS):
  uname = fake.first_name()
  isOdd = bool(getrandbits(1))

  for j in range(0,randrange(1,MAX_CLICKS_PER_USER)): 
   click = randrange(URL_ID_MIN, URL_ID_MAX, 2)
   if (isOdd):
     click += 1
   out.append("{}\t{}".format(uname, click))

with open('access.log', 'w') as handle:
  for o in out:
    print(o)
    print >> handle, o
