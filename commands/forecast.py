#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: forecast.py                        #
# Logic for forecast command               #
# ======================================== #

import re
import urllib
import json
import datetime

class CmdForecast:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        # RegEx pattern, used to fetch the location wrapped in quotation marks
        pattern = re.search('forecast for ([\"\'](.*?)[\"\'])', text.lower())
        
        reply = ""
        
        # If the pattern fails to find something, then the user didn't do something right
        if pattern:
            # Target location is captured in group(2) of the pattern
            # We add this to a URL and attempt to read JSON data from OpenWeatherMap
            location = pattern.group(2)
            
            url = "http://api.openweathermap.org/data/2.5/forecast/daily?mode=json&units=imperial&cnt=4&q=" + location
            data = {}

            try:
                response = urllib.urlopen(url)
                data = json.loads(response.read())
            except:
                pass    # If an error occurs when trying to read data, we ignore it (because it'll kill Wilbur)
                        # Then we set our reply to an error message
                reply = "@" + user + ": Error with pulling up weather data. Please try again later."
            else:
                if data['cod'] == "200":
                    # Store the next 4 days into a forecast array.. Note that the first index is today's weather data
                    forecast_data = data['list']
                    name = data['city']['name']

                    if name == "":
                        name = location
                    
                    reply = "@" + user + ": 3 day forecast for " + name + "\n"

                    for i in range(1,len(forecast_data)):
                        dt = datetime.datetime.fromtimestamp(int(forecast_data[i]['dt'])).strftime('%m/%d')
                        temp = forecast_data[i]['temp']['max']
                        reply = reply + dt + " - " + str(temp) + "F" + "\n"
                else:
                    reply = "@" + user + ": The location you entered is not a valid location"
        else:
            reply = "@" + user + ": Please put quotation marks around your target location"
             
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave forecast info to " + user
        )