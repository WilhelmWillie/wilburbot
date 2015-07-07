import operator
import stats
import util

PRIORITY = 1

'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "mention stat" in tweet or "mentions stat" in tweet or "most mentioned" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    statuses = author.timeline(count=200, include_rts=False)

    mention_count = stats.get_mention_count(statuses)

    if len(mention_count) == 0:
        response = "Based on your last 200 tweets, you don't talk to anyone on twitter"
    else:
        most_mentioned = max(mention_count.iteritems(), key=operator.itemgetter(1))[0]
        response = "Based on your last 200 tweets, you mention @%s the most (%i)" % (most_mentioned,mention_count[most_mentioned],)
    
    # Store data in tweets collection
    util.add_tweets(statuses, wilbur)

    return response