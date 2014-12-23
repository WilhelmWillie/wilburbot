#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: naughty_or_nice.py                 #
# Logic for naughty or nice command        #
# ======================================== #

class CmdNaughtyOrNice:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        # Tweets containing any of the following naughty words will increase the naughty count by 1
        naughty_count = 0
        naughty_words = ['shit','fuck','damn','bitch','crap','piss','dick','cock','pussy','asshole','fag','bstard','slut','douche', 'ass']

        for tweet in user_statuses:
            for naughty_word in naughty_words:
                if naughty_word in tweet['text']:
                    naughty_count = naughty_count + 1
                    break
                    
        reply = ""
        
        naughty_percent = float(naughty_count) / len(user_statuses)

        if naughty_percent > 0.15:
            reply = "@" + user + ": You're very naughty! " + str(round(naughty_percent * 100, 3)) + " percent of your tweets contain naughty words"
        else:
            reply = "@" + user + ": You're very nice! Only " + str(round(naughty_percent * 100, 3)) + " percent of your tweets contain naughty words"

        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Told " + user + " whether or not he/she is naughty/nice"
        )