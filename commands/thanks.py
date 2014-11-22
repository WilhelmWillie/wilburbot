#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: thanks.py                          #
# Logic for thank you command              #
# ======================================== #

import random

class CmdThanks:
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
                "You're welcome! #ballislife",
                "Not a problem!"
        ]
        
        index = random.randint(0, len(messages)-1)
        reply = "@" + user + ": " + messages[index]
        
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave 'your welcome' to " + user
        )