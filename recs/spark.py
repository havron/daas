from pyspark import SparkContext
import itertools

sc = SparkContext("spark://spark-master:7077", "PopularItems")
sc.setLogLevel("ERROR")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: tuple(line.split("\t")))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
count = pages.reduceByKey(lambda x,y: x+y)        # shuffle the data so that each key is only on one worker
												  # and then reduce all the values by adding them together
output = count.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular items done\n")

# Group data into [(user_id, [items clicked on])]
clicks = pairs.groupByKey()
for click in clicks.collect():
    print(click[0]+" clicked on the following items: "+str(list(click[1])))
print("\n")
# distinct clicks mapped in pairs
clicks = pairs.distinct().groupByKey()
clickpairs = clicks.map(lambda click: (list(itertools.combinations(click[1],2)), click[0]))


def iterpairs(click):
  combs = itertools.combinations(click[1],2)
  res = []
  for comb in combs:
    res.append((comb,click[0])) # map all pair combos to each user
  return res

# Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
clickpairs = clicks.map(iterpairs)
#print("Click pairs: "+ str(clickpairs.collect()))

coclicks = clickpairs.flatMap(lambda line: line)
#print("Co-clicks: "+str(coclicks.collect()))

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
coclickers = coclicks.groupByKey()
for clickers in coclickers.collect():
  print("Items "+str(clickers[0])+" were clicked on by "+str(list(clickers[1])))
print("\n")

# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
distinct = coclicks.map(lambda pair: (pair[0],1))
print("all distinct clicks: "+str(distinct.collect())+"\n")

distinct = distinct.reduceByKey(lambda x, y: x + y)
print("reduced distinct clicks: "+str(distinct.collect())+"\n")

# Filter out any results where less than 3 users co-clicked the same pair of items
massclicks = distinct.filter(lambda pair: pair[1] >= 3)

print("filtered mass clicks (THE RESULT OF OUR SPARK JOB): "+str(massclicks.collect()))
sc.stop()
