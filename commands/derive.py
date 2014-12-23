#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: derive.py                          #
# Logic for derive command                 #
# ======================================== #

from sympy import *
import re

class CmdDerive:
    twitter = None

    def __init__(self, twitter):
        self.twitter = twitter

    def execute(self, user, tweet_id, text):
        text = text.replace("^", "**")

        # RegEx pattern, used to fetch function to derive
        pattern = re.search('[\'"](.*?)[\'"]+', text)

        reply = ""
        
        if pattern:
            equation = pattern.group(1)
            
            derivative = ""
            x = "x"
            try:
                derivative = diff(equation, x)
            except:
                reply = "@" + user + ": Error trying to calculate derivative! Your equation is formatted strangely"
            else:
                reply = "@" + user + ": f'(x) = " + str(derivative)
        else:
            reply = "@" + user + ": Couldn't find equation to derive"

        reply = reply.replace("**","^")
        reply = reply.replace("*","")
        
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave birthday msg as requested by " + user
        )