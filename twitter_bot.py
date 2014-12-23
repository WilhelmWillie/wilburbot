#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: twitter_bot.py                     #
# Handles twitter API calls in a simpler   #
# fashion.                                 #
# ======================================== #

from twitter import *
import time

class TwitterBot:
    # Holds primary twitter object.. 
    twitter = None
    stream = None
    
    def __init__(self,oauth):
        self.twitter = Twitter(auth=oauth)
        twitter_stream = TwitterStream(auth=oauth)
        self.stream = twitter_stream.statuses.filter(track="WilburBot")
    
    def get_user_timeline(self,name):
        return self.twitter.statuses.user_timeline(screen_name=name,count=200,include_rts=False)

    def get_tweet(self,tweet_id):
        return self.twitter.statuses.show(id=tweet_id)

    def get_favorites(self,name):
        return self.twitter.favorites.list(screen_name=name, count=200)
        
    def reply(self, reply, reply_to, success_log):
        try:
            self.twitter.statuses.update(status=reply,in_reply_to_status_id=reply_to)
        except TwitterHTTPError as e:
            print "[" + time.strftime("%H:%M:%S") + "] Twitter HTTP Error"
            print e
        else:
            print "[" + time.strftime("%H:%M:%S") + "] " + success_log
    
    def post(self, message, success_log):
        try:
            self.twitter.statuses.update(status=message)
        except TwitterHTTPError as e:
            print "[" + time.strftime("%H:%M:%S") + "] Twitter HTTP Error"
            print e
        else:
            print "[" + time.strftime("%H:%M:%S") + "] " + success_log