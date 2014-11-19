#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_birthday.py                    #
# Logic for birthday command               #
# ======================================== #

import re

class Birthday:
    twitter = None

    def __init__(self, twitter):
        self.twitter = twitter

    def execute(self, user, tweet_id, text):
        # RegEx pattern, used to fetch an at name
        pattern = re.search('birthday to @([A-Za-z0-9_]+)', text)

        reply = ""

        # If the pattern fails to find something, then the user didn't do something right
        if pattern:
            # Target location is captured in group(2) of the pattern
            target = pattern.group(1)

            reply = "@" + target + ": HAPPY BIRTHDAY! Hope your day is as splendid as you are!"
        else:
            reply = "@" + user + ": Make sure you're actually mentioning a user"

        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave birthday wish for " + user
        else:
            print "[ERROR] Something went wrong giving birthday for " + user