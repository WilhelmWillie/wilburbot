#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_weather.py                     #
# Logic for weather command                  #
# ======================================== #

import re
import urllib
import json

class Weather:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        # RegEx pattern, used to fetch the location wrapped in quotation marks
        pattern = re.search('weather in ([\"\'](.*?)[\"\'])', text)
        
        reply = ""
        
        # If the pattern fails to find something, then the user didn't do something right
        if pattern:
            # Target location is captured in group(2) of the pattern
            # We add this to a URL and attempt to read JSON data from OpenWeatherMap
            location = pattern.group(2)
            
            url = "http://api.openweathermap.org/data/2.5/find?units=imperial&q=" + location
            
            try:
                response = urllib.urlopen(url)
                data = json.loads(response.read())
            except:
                pass    # If an error occurs when trying to read data, we ignore it (because it'll kill Wilbur)
                        # Then we set our reply to an error message
                reply = "@" + user + ": Error with pulling up weather data. Please try again later."
            else:
                if data['count'] == 0:
                    # If the count is 0, that means we did not find a city that matches the location the user wanted
                    reply = "@" + user + ": The location you entered is not a valid location"
                else:
                    # Otherwise, we get the first matched location (OpenWeatherMap might retrieve multiple cities.. It's up to user to be more specific)
                    # and return temperature data
                    name = data['list'][0]['name']
                    
                    if name == "":
                        name = location
                    
                    temperature = data['list'][0]['main']['temp']
                    high = data['list'][0]['main']['temp_max']
                    low = data['list'][0]['main']['temp_min']
                    reply = "@" + user + ": In " + name + ", it is currently " + str(temperature) + " degrees Fahrenheit with a high of " + str(high) + " and a low of " + str(low)
        else:
            reply = "@" + user + ": Your search query is invalid. Make sure you put quotation marks around your target location"
             
        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave weather to " + user
        else:
            print "[ERROR] Something went wrong giving weather to " + user