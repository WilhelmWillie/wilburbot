#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: weather.py                         #
# Logic for weather command                #
# ======================================== #

import re
import urllib
import json

class CmdWeather:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        # RegEx pattern, used to fetch the location wrapped in quotation marks
        pattern = re.search('weather in ([\"\'](.*?)[\"\'])', text.lower())
        
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
                if data['message'] == "accurate":
                    if data['count'] == 0:
                        # If the count is 0, that means we did not find a city that matches the location the user wanted
                        reply = "@" + user + ": We couldn't find weather data for your specified location"
                    elif data['count'] == 1:
                        # Otherwise, we get the first matched location (OpenWeatherMap might retrieve multiple cities.. It's up to user to be more specific)
                        # and return temperature data
                        name = data['list'][0]['name']
                        
                        if name == "":
                            name = location
                        
                        temperature = data['list'][0]['main']['temp']
                        condition_array = data['list'][0]['weather']
                        reply = "@" + user + ": In " + name + ", it is currently " + str(temperature) + " degrees Fahrenheit. Conditions: "

                        for i in range(0,len(condition_array)):
                            if i == len(condition_array) - 1:
                                reply = reply + condition_array[i]['description']
                            else:
                                reply = reply + condition_array[i]['description'] + ", "

                    else:
                        # There's a possibility that the user's location will have more than 1 result ("Paris" returns 2 results, "Paris, France" returns one)
                        reply ="@" + user + ": Your location returned more than 1 result. Please be more specific (if possible)"
                else:
                    reply = "@" + user + ": The location you entered is not a valid location"
        else:
            reply = "@" + user + ": Please put quotation marks around your target location"
             
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave weather info to " + user
        )