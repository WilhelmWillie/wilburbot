#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_derive.py                      #
# Logic for derive command                 #
# ======================================== #

from sympy import *
import re

class Derive:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        text = text.replace("^","**")
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
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave derivative to " + user
        else:
            print "[ERROR] Something went wrong giving derivative to " + user