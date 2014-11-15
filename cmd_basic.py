#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_basic.py                       #
# Logic for basic stats command            #
# ======================================== #

class Basic:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        fav_count = 0
        rt_count = 0
        tweet_count = len(user_statuses)
        
        for tweet in user_statuses:
            fav_count += tweet['favorite_count']
            rt_count += tweet['retweet_count']
            
        fav_per_tweet = round((fav_count / float(tweet_count)), 3)
        rt_per_tweet = round((rt_count / float(tweet_count)), 3)
        reply = "@" + user + ": Based on your last 200 tweets, you average " + str(fav_per_tweet) + " favorites and " + str(rt_per_tweet) + " retweets per tweet! #WilburBot"
        
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave basic stats to " + user
        else:
            print "[ERROR] Something went wrong giving basic stats to " + user