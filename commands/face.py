#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: face.py                            #
# Logic for face command                   #
# ======================================== #

import urllib
import json

class CmdFace:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        tweet = self.twitter.get_tweet(tweet_id)

        reply = ""

        # If the user has included a photo, we go in!
        if len(tweet['entities']['media']) == 1:
            imgUrl = tweet['entities']['media'][0]['media_url']
            apiUrl = "http://api.skybiometry.com/fc/faces/detect.json?api_key=651f3779e5204a2bb22991d92f355a70&api_secret=5ffefb03a623403c9d106e7759354c43&urls=" + imgUrl + "&attributes=all"
            
            try:
                response = urllib.urlopen(apiUrl)
                data = json.load(response)

                if data['status'] == "success":
                    if len(data['photos'][0]['tags']) == 1:
                        tag_data = data['photos'][0]['tags'][0]

                        gender = tag_data['attributes']['gender']
                        mood = tag_data['attributes']['mood']
                        smiling = tag_data['attributes']['smiling']

                        reply = "@" + user + ": Based on the picture you sent..." + "\n"
                        reply = reply + "Gender: " + gender['value'] + " (" + str(gender['confidence']) + "%)\n"
                        reply = reply + "Mood: " + mood['value'] + " (" + str(mood['confidence']) + "%)\n"
                        reply = reply + "Smiling: " + smiling['value'] + " (" + str(smiling['confidence']) + "%)"
                    else:
                        reply = "@" + user + ": Only one person should be in your photo! Please try again!"
                else:
                    reply = "@" + user + ": Your picture couldn't be analyzed. Either because I'm worn out or cause there is no face in your pic"
            except:
               reply = "@" + user + ": Something went wrong trying to analyze your picture. Try again later."
        else:
            reply = "@" + user + ": Please include ONE photo of yourself"

        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave face stats to " + user
        )