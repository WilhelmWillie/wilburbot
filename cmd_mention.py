#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_mention.py                     #
# Logic for mentions command               #
# ======================================== #

import re
import operator

class Mention:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        mention_count = {}
            
        # Loop through tweets and find mentions. Loop through all found mentions and add to mention_count
        for tweet in user_statuses:
            user_mentions = tweet['entities']['user_mentions']
            
            for mention in user_mentions:
                user_mentioned = mention['screen_name']
                
                if user_mentioned in mention_count:
                    mention_count[user_mentioned] = mention_count[user_mentioned] + 1
                else:
                    mention_count[user_mentioned] = 1
                    
        reply = ""
        
        # There's a chance a user won't mention anyone, if this is the case prepare a fallback reply
        if len(mention_count) == 0:
            reply = "@" + user + ": Based on your last 200 tweets, you don't talk to anyone on twitter"
        else:
            most_mentioned = max(mention_count.iteritems(), key=operator.itemgetter(1))[0]
            reply = "@" + user + ": Based on your last 200 tweets, you mention @" + most_mentioned + " the most #WilburBot"
            
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave mentions stats to " + user
        else:
            print "[ERROR] Something went wrong giving mentions stats to " + user