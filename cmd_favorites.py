#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_favorites.py                   #
# Logic for favorites command              #
# ======================================== #

import operator

class Favorites:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        favorites = self.twitter.get_favorites(name=user)
        
        favorites_count = {}
    
        # Loop through all favorites and add to favorites_count
        for tweet in favorites:
            author = tweet['user']['screen_name']

            if author in favorites_count:
                favorites_count[author] = favorites_count[author] + 1
            else:
                favorites_count[author] = 1
                    
        reply = ""
        
        # There's a chance a user won't favorite anyone, if this is the case prepare a fallback reply
        if len(favorites_count) == 0:
            reply = "@" + user + ": Based on your last 200 favorites, you don't favorite anyone!?"
        else:
            most_favorited = max(favorites_count.iteritems(), key=operator.itemgetter(1))[0]
            reply = "@" + user + ": Based on your last 200 favorites, you favorite @" + most_favorited + " (" + str(favorites_count[most_favorited]) + ") the most #WilburBot"
            
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave favorite stats to " + user
        else:
            print "[ERROR] Something went wrong giving favorite stats to " + user