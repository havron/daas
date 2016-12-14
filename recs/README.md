# Recommendation System for daas, using mass co-views
See `logGen.py` for `access.log`'s creation details. You're welcome to change
the parameters in the generator and create an access log and running `python logGen.py`! 
Currently, the generator makes each user click on exclusively even or odd item IDs, 
which make it simple to verify the spark job is producing correct output (odd
items and even items are co-clicked).

Given `access.log` as input, `spark.py` produces standard output with the
results of the spark job.

High level pseudocode for our map-reduce style algorithm for computing
co-views is as follows:

1. Read data in as pairs of (user_id, item_id clicked on by the user)
2. Group data into (user_id, list of item ids they clicked on)
3. Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on
4. Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2)
5. Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2)
6. Filter out any results where less than 3 users co-clicked the same pair of items

# How to run the spark job
To use the spark job, simply run `make spark` in the base directory of this
repository! Standard output will show the job as it is running. 
You're welcome to adjust the settings of spark; currently, one master and one worker node are used.

# Sample Results
See `spark.out`, produced by running `make sparklog` in the base directory of
the repository. The final (filtered) result is the last line of output.
