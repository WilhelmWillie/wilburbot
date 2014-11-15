#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_drake.py                       #
# Logic for drake lyrics command           #
# ======================================== #

import random

class Drake:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        messages = [
                "I know they say the first love is the sweetest, but that first cut is the deepest.",
                "I live for the nights that I can't remember with the people that I won't forget.",
                "Better late than never but never late is better",
                "Lately I've been drinking like there's a message in a bottle",
                "Lights get low and that's when I have my brightest ideas",
                "You know its real when your latest nights are your greatest nights",
                "Tables turn, bridges burn, you live and learn.",
                "Last name Ever, first name Greatest, Like a sprained ankle, boy I ain't nothing to play with",
                "Everybody dies, but not everybody lives",
                "Somewhere between I want it and I got it",
                "Started from the bottom now we're here",
                "Swanging, eyes closed just swanging",
                "Cause you're a good girl and you know it. You act so different around me",
                "Just hold on, we're going home..",
                "Done saying, I'm done playing. Last time was on the outro",
                "I think I'm scared of what the future holds",
                "And no, I'm not saying I'm the nicest, I just live life like it",
                "Cry if you need to, but I can't stay to watch you, that's the wrong thing to do",
                "I realized I waited too long, but please don't move on",
                "I never had you, although I would be glad to",
                "I'm willing to work it out however long it takes you",
                "I better find your heart, I bet if I give all my love, then nothing's going to tear us apart",
                "I'm scared that every girl I care for will find a better man and end up happier in the long run",
                "I pop bottles because I bottle my emotions",
                "When the party's over, just don't forget me",
                "I tried to keep us together, you were busy keeping secrets",
                "I just hate sleeping alone",
                "I need you to rescue me from my destiny, I'm trying to live right and give you whatever's left of me",
                "You could have my heart or we could share it like the last slice.",
                "Baby you're my everything, you're all I ever wanted",
                "We could do it real big, bigger than you ever done it"
        ]
        
        reply = "@" + user + ": \"" + random.choice(messages) + "\" - Drake"
        
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave Drake lyrics to " + user
        else:
            print "[ERROR] Something went wrong giving Drake lyrics to " + user