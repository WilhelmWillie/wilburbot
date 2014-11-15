#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_thanks.py                      #
# Logic for thank you command              #
# ======================================== #

import random

class Thanks:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        messages = [
                "You're welcome!",
                "No problem!",
                "It was my pleasure!",
                "Any time!",
                "Don't mention it!",
                "It was nothing!",
                "No worries!",
                "You're welcome! #ballislife"
        ]
        
        reply = "@" + user + ": " + random.choice(messages)
        
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave thanks to " + user
        else:
            print "[ERROR] Something went wrong giving thanks to " + user