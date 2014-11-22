#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: movie.py                           #
# Logic for movie command                  #
# ======================================== #

import re
import urllib
import json

class CmdMovie:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        # RegEx pattern, used to fetch the movie title wrapped in quotation marks
        pattern = re.search('movie info for ([\"\'](.*?)[\"\'])', text.lower())
        
        reply = ""
        
        # If the pattern fails to find something, then the user didn't do something right
        if pattern:
            # Target movie is captured in group(2) of the pattern
            # We add this to a URL and attempt to read JSON data from OpenMovieDatabase
            location = pattern.group(2)
            
            url = "http://www.omdbapi.com/?t=" + location
            
            try:
                response = urllib.urlopen(url)
                data = json.loads(response.read())
            except:
                pass    # If an error occurs when trying to read data, we ignore it (because it'll kill Wilbur)
                        # Then we set our reply to an error message
                reply = "@" + user + ": Error with pulling up movie data. Please try again later."
            else:
                if data['Response'] == "False":
                    # If the response is false, that means we did not find a movie that matches the title the user wanted
                    reply = "@" + user + ": The movie title you entered is not a valid movie"
                else:
                    title = data['Title']
                    year = data['Year']
                    awards = data['Awards']
                    imdb_rating = data['imdbRating']

                    reply = "@" + user + ": " + title + " (" + year + ") // Awards: " + awards + " // IMDB Rating: " + imdb_rating
        else:
            reply = "@" + user + ": Please put quotation marks around your movie title"
             
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave movie info to " + user
        )