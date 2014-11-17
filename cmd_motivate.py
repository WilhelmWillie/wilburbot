#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_motivate.py                    #
# Logic for motivate me command            #
# ======================================== #

import random

class Motivate:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        messages = [
                "Every accomplishment starts with the decision to try",
                "Stop wishing. Start doing.",
                "You have to fight through the bad days in order to earn the best days.",
                "If you don't have what you want, work harder!",
                "A year from now, you will wish you had started today",
                "Dreams don't work unless you do",
                "The struggle you're in today is developing the strength you need for tomorrow",
                "Do something today that your future self will thank you for",
                "What's stopping you?",
                "Work until your idols become your rivals",
                "Believe you can and you are halfway there",
                "If opportunity doesn't knock, build a door.",
                "Push yourself because no one else is going to do it for you",
                "Success isn't given. It's earned",
                "If you're going through hell.. keep going",
                "Opportunities don't happen, you create them",
                "The distance between insanity and genius is measured only by success",
                "No masterpiece was ever created by a lazy artist",
                "Success is the sum of small efforts, repeated day-in and day-out.",
                "Failure is the condiment that gives success its flavor.",
                "The only place where success comes before work is in the dictionary",
                "There is no substitute for hard work",
                "Do it now. Sometimes 'later' becomes 'never'",
                "Excellence is not a skill. It is an attitude",
                "'Regardless of the scoreboard, you're going to be succesful' - Apollos Hester",
                "'It took an attitude. That's all it takes. That's all it takes to be succesful' - Apollos Hester"
                "'You can do anything you put your mind to' - Apollos Hester",
                "'ANYTHING IS POSSIBLEEE' - Kevin Garnett",
                "The expert in anything was once a beginner"
        ]
        
        index = random.randint(0, len(messages)-1)
        reply = "@" + user + ": " + messages[index]
        
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave motivation to " + user
        else:
            print "[ERROR] Something went wrong giving motivation to " + user