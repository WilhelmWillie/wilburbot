#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: twitter_bot.py                     #
# Handles twitter API calls in a simpler   #
# fashion.                                 #
# ======================================== #

from twitter import *

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

    def get_favorites(self,name):
        return self.twitter.favorites.list(screen_name=name, count=200)
        
    def reply(self,reply,reply_to):
        try:
            self.twitter.statuses.update(status=reply,in_reply_to_status_id=reply_to)
        except TwitterHTTPError as e:
            print e
            
            if "Status is a duplicate" in e:
                reply("Try again, something went wrong trying to reply to you", reply_to)
            return False
        else:
            return True
    
    def post(self,message):
        try:
            self.twitter.statuses.update(status=message)
        except TwitterHTTPError as e:
            print e
            return False
        else:
            return True