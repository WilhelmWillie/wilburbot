#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: terminate.py                       #
# Logic for terminate command              #
# ======================================== #

import sys

class CmdTerminate:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        if user == "Willieminati":
            self.twitter.post("Terminating main process. (As told by @Willieminati)", "Forced to terminate by Willieminati")
            sys.exit()