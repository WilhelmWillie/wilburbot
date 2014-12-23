#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: holidays.py                        #
# Logic for holidays command               #
# ======================================== #

class CmdHolidays:
    twitter = None

    def __init__(self, twitter):
        self.twitter = twitter

    def execute(self, user, tweet_id, text):
        messages [
            "Thanks! You too!",
            "Aw shucks! Hope you have a great one too!",
            "Thanks! You as well!",
            "I love winter!",
            "Hope you have a great one!",
            "Hope you enjoy yours!",
            "Thanks, hope you enjoy yours!",
            ":-D"
        ]

        index = random.randint(0, len(messages)-1)
        reply = "@" + user + ": " + messages[index]
        
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave holiday message to " + user
        )