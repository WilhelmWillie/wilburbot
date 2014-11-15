#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_time.py                        #
# Logic for time command                   #
# ======================================== #

import time
import operator

class TimeStats:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        hour_count = {}
            
        for tweet in user_statuses:
            hour = time.strftime('%H', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            
            hour = int(hour) - 5 # Time they give us is in UTC. We subtract 5 hours to convert it to EST

            if hour < 0:
                hour = 24 + hour
            if hour > 24:
                hour = hour - 24
            
            if hour in hour_count:
                hour_count[hour] = hour_count[hour] + 1
            else:
                hour_count[hour] = 1
                    
        reply = ""
        
        if len(hour_count) == 0:
            reply = "@" + user + ": Based on your last 200 tweets, you don't tweet... at all.. ???"
        else:
            common_hour = max(hour_count.iteritems(), key=operator.itemgetter(1))[0] 
            pm_or_am = "PM"
            
            percentage = round(float(hour_count[common_hour]) / len(user_statuses), 4) * 100
            
            if common_hour > 12:
                common_hour = common_hour - 12
            elif common_hour < 12:
                pm_or_am = "AM"
                
            reply = "@" + user + ": Based on your last 200 tweets, you tweet the most during the hour of " + str(common_hour) + " " + pm_or_am + " EST (" + str(percentage) + "%) #WilburBot"

        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave time stats to " + user
        else:
            print "[ERROR] Something went wrong giving time stats to " + user