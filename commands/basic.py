import stats
import util

PRIORITY = 1

'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "basic stat" in tweet or "calculate my averages" in tweet or "calculate averages" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    statuses = author.timeline(count=200, include_rts=False)
    fav_per_tweet, rt_per_tweet = stats.get_averages(statuses)

    response = "Based on your last 200 tweets, you average %0.3f favorites and %0.3f retweets per tweet" % (fav_per_tweet, rt_per_tweet,)
    
    # Store data in tweets collection
    util.add_tweets(statuses, wilbur)

    return response