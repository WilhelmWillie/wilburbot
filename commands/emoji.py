# -*- coding: utf-8 -*-
import re
import operator
import stats
import util

PRIORITY = 1

'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "emoji stat" in tweet or "most used emoji" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    statuses = author.timeline(count=200, include_rts=False)

    emoji = stats.get_emoji(statuses)

    if emoji == "N/A":
        response = "Based on your last 200 tweets, you don't seem to use emojis at all"
    else:
        response = "Based on your last 200 tweets, your most used emoji is " + emoji

    # Store data in tweets collection
    util.add_tweets(statuses, wilbur)

    return response