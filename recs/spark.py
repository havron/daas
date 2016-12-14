from pyspark import SparkContext
import itertools

sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: tuple(line.split("\t")))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[1], 1))      # re-layout the data to ignore the user id
count = pages.reduceByKey(lambda x,y: x+y)        # shuffle the data so that each key is only on one worker
												  # and then reduce all the values by adding them together

print(pairs.collect())
print(pages.collect())


output = count.collect()                          # bring the data back to the master node so we can print it out
for page_id, count in output:
    print ("page_id %s count %d" % (page_id, count))
print ("Popular items done")

# Group data into [(user_id, [items clicked on])]
clicks = pairs.groupByKey()
clickpairs = clicks.map(lambda click: (click[0],itertools.combinations(click[1],2)))

for click in clicks.collect():
    print(click[0]+" clicked on the following items: "+str(list(click[1])))
    print(str(list(itertools.combinations(click[1], 2))))




clicks = pairs.distinct().groupByKey()
clickpairs = clicks.map(lambda click: (click[0], list(itertools.combinations(click[1],2))))

print("Click pairs: "+ str(clickpairs.collect()))


cl = clickpairs.collect()

for c in cl:
  print("mapping is "+str((c[0], c[1])))
  print("NEW mapping is "+str(list((ca, c[0]) for ca in c[1])))


# coclicks = clickpairs.map(lambda pair: list((pa, pair[0]) for pa in pairs[1]))
coclicks = clickpairs.flatMap(lambda pair: list((pair[0], pair[1])))

p = coclicks.map(lambda pair: (pair[1],1))
p2 = p.reduceByKey(lambda x, y: x + y)

p3 = p2.filter(lambda pair: pair[1] >= 3)

print("CO-CLICKS: "+str(coclicks.collect()))
print("p1: "+str(p.collect()))
print("p2: "+str(p2.collect()))
print("p3: "+str(p3.collect()))



# Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on

# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)

# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)


# Filter out any results where less than 3 users co-clicked the same pair of items

sc.stop()
