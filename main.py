#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: main.py                            #
# Starts up Wilbur Bot                     #
# ======================================== #

from auth import *
from twitter_bot import *

# Command imports
from cmd_basic import Basic
from cmd_emoji import Emoji
from cmd_time import TimeStats
from cmd_mention import Mention
from cmd_weather import Weather
from cmd_drake import Drake
from cmd_motivate import Motivate
from cmd_thanks import Thanks

import sys
import time

# Variables to be used throughout the Wilbur Bot program
twitter = None # Object used to make calls to twitter API
stream = None # Used for streaming

# Command List
commands = None

# Init: Sets up Wilbur Bot
def init():
    global twitter
    global stream
    
    oauth = get_oauth()
    twitter = TwitterBot(oauth=oauth)
    stream = twitter.stream
    
    setup_commands()
    
    print "[START] WilburBot is up and running!"
    # If we started Wilbur Bot with the argument 'announce', we push a tweet announcing start up
    if len(sys.argv) == 2:
        if sys.argv[1] == "announce":
            print "[***] ANNOUNCING: Tweet will be posted to @WilburBot to alert followers"
            twitter.post("I'm back up and running! Mention me in your tweets and I'll process your request! (" + time.strftime("%c") + ")")
        elif sys.argv[1] == "debug":
            print "[***] DEBUG ANNOUNCE: Tweet will be posted to @WilburBot letting users know you're testing out new features"
            twitter.post("I'm back up and running in debug mode! This means features are being tested and/or added. As a result, I might break down at times!")
    
# Main: Where most of the Wilbur Bot logic occurs
def main():
    # Loops through tweets in stream
    for tweet in stream:
        process_tweet(tweet)
        
# Setup Commands: Instantiates command objects and store them in commands dictionary
def setup_commands():
    global commands
    # KEY = String of possible commands.. Multiple commands are split using the '|' delimiter
    # VALUE = Class used to deal with command
    # NOTE: Commands are in order of priority (Top = HIGHEST)
    commands = {
        "basic stats": Basic(twitter),
        "emoji stats": Emoji(twitter),
        "time stats": TimeStats(twitter),
        "mention stats|mentions stats": Mention(twitter),
        "weather in": Weather(twitter),
        "drake lyrics": Drake(twitter),
        "motivate me|give motivation": Motivate(twitter),
        "thanks|thank you|thx": Thanks(twitter)
    }
    
# Process Tweet: When we find a tweet, process it and fire up any commands if needed
def process_tweet(tweet):
    if 'text' in tweet and 'id_str' in tweet:   # Every now and then, the stream might receive a non-tweet so this should check for an actual tweet
        text = tweet['text'].lower()    # Force the string to go to lowercase to avoid case sensitive mishaps
        tweet_id = tweet['id_str']
        
        # Make sure tweet was a mention of @WilburBot and not a mention of the string 'WilburBot'
        if '@wilburbot' in text:
            user = tweet['user']['screen_name']
            
            # Loop through all possible commands in commands dictionary
            # Then we split the possible commands to check for possible aliases
            for command in commands:
                command_labels = command.split("|")
                
                command_executed = False
                
                for label in command_labels:
                    if label in text:
                        commands[command].execute(user=user,tweet_id=tweet_id,text=text)
                        command_executed = True
                        break # Terminate from loop early in case the same command alias occurs twice in the text
                        
                if command_executed == True:
                    break # Only process one command at a time to prevent command overload (Trying to reply back w/ more than 1 command)
    
init()
main()

# Called when main stream closes
twitter.post("Terminating main process. Either I've fallen asleep or was turned off manually")