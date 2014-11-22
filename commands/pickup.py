#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: pickup.py                          #
# Logic for pickup command                 #
# ======================================== #

import random

class CmdPickup:
    twitter = None

    def __init__(self, twitter):
        self.twitter = twitter

    def execute(self, user, tweet_id, text):
        messages = [
                "What's your sine? Must be pi/2 because you are the 1",
                "Your body is 65% water and I'm thirsty",
                "Can I follow you home? Cause my parents always told me to follow my dreams.",
                "If you were a vegetable you'd be a cute-cumber",
                "If you were a booger I'd pick you first. ;-)",
                "Are you lost? Because heaven is a long way from here",
                "Are you a campfire? Cause you are hot and I want s'more",
                "My love for you is like diarrhea, I just can't hold it in",
                "Baby I might not be Sriracha sauce but I sure will spice your life up",
                "Grab my arm so I can tell my friends I've been touched by an angel",
                "Of all the beautiful curves on your body, your smile is my favorite",
                "Did you have lucky charms for breakfast? Because you look magically delicious ;-)",
                "I'm no organ donor but I'd be happy to give you my heart"
        ]

        index = random.randint(0, len(messages)-1)
        reply = "@" + user + ": " + messages[index]

        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave pickup line to " + user
        )