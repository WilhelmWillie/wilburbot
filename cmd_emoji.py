#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_emoji.py                       #
# Logic for emoji command                  #
# ======================================== #

import re
import operator

class Emoji:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        emoji_count = {}
        total = 0   # Used for calculating percentage at the end
        
        # Found online, RegEx pattern for finding emojis
        try:
            emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            emoji_pattern = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
            
        # Loop through tweets and use RegEx to find emojis. Loop through all found emojis and add to emoji_count
        for tweet in user_statuses:
            emojis_in_tweet = emoji_pattern.findall(tweet['text'])
            
            for e in emojis_in_tweet:
                total = total + 1
                
                if e in emoji_count:
                    emoji_count[e] = emoji_count[e] + 1
                else:
                    emoji_count[e] = 1
                    
        reply = ""
        
        # There's a chance a user won't have any emojis, if this is the case prepare a fallback reply
        if len(emoji_count) == 0:
            reply = "@" + user + ": Based on your last 200 tweets, you don't seem to use emojis at all #TeamAndroid ?"
        else:
            most_used_emoji = max(emoji_count.iteritems(), key=operator.itemgetter(1))[0]
            percentage = round(float(emoji_count[most_used_emoji]) / total, 5) * 100
            reply = "@" + user + ": Based on your last 200 tweets, your most used emoji is " + most_used_emoji + " (" + str(percentage) + "%) #WilburBot"
            
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave emoji stats to " + user
        else:
            print "[ERROR] Something went wrong giving emoji stats to " + user