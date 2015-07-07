import stats
import util

PRIORITY = 1

'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "time stat" in tweet or "most active hour" in tweet or "hour stat" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    statuses = author.timeline(count=200, include_rts=False)

    common_hour, pm_or_am = stats.get_hour(statuses)

    response = "Based on your last 200 tweets, you are most active on twitter on the hour of " + str(common_hour) + " " + pm_or_am + " EST"
    
    # Store data in tweets collection
    util.add_tweets(statuses, wilbur)
    
    return response