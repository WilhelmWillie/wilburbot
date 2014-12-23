#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: main.py                            #
# Starts up Wilbur Bot                     #
# ======================================== #

from auth import *
from twitter_bot import *

from commands import *

import sys
import traceback # Used for debug purposes
import time

# Variables to be used throughout the Wilbur Bot program
twitter = None # Object used to make calls to twitter API
stream = None # Used for streaming

# Command List
commands = None

# Becomes True when @Willieminati commands Wilbur to terminate
terminated = False

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
            twitter.post(
                message = "I'm back up and running! Mention me in your tweets and I'll process your request! (" + time.strftime("%H:%M:%S") + ")",
                success_log = "[***] ANNOUNCING: Tweet will be posted to @WilburBot to alert followers"
            )
        elif sys.argv[1] == "debug":
            twitter.post(
                message = "I'm back up and running in debug mode! This means features are being tested and/or added. As a result, I might break down at times!",
                success_log = "[***] DEBUG ANNOUNCE: Tweet will be posted to @WilburBot letting users know you're testing out new features"
            )

# Main: Where most of the Wilbur Bot logic occurs
def main():
    # Loops through tweets in stream
    for tweet in stream:
        if "retweeted_status" not in tweet: # It was brought to my attention that retweeted tweets can pop up in the stream.. this is to make sure we don't process such tweets
            try:
                process_tweet(tweet)
            except SystemExit:
                terminated = True
                break
            except Exception as e:
                print traceback.format_exc()
                pass # If something goes bad trying to process tweet, we ignore it to prevent Wilbur from crashing

# Setup Commands: Instantiates command objects and store them in commands dictionary
def setup_commands():
    global commands
    # KEY = String of possible commands.. Aliases are split using the '|' delimiter
    # VALUE = Class used to deal with command
    commands = {
        "basic stats": CmdBasicStats(twitter),
        "emoji stats": CmdEmojiStats(twitter),
        "favorite stats|favorites stats": CmdFavoriteStats(twitter),
        "mention stats|mentions stats": CmdMentionStats(twitter),
        "word stats|words stats": CmdWordStats(twitter),
        "time stats": CmdTimeStats(twitter),
        "weather in": CmdWeather(twitter),
        "movie info for": CmdMovie(twitter),
        "drake lyrics": CmdDrake(twitter),
        "motivate|motivation": CmdMotivate(twitter),
        "thanks|thank|thx": CmdThanks(twitter),
        "wish birthday to|wish happy birthday to": CmdBirthday(twitter),
        "pickup|pickup line": CmdPickup(twitter),
        "terminate": CmdTerminate(twitter),
        "forecast for": CmdForecast(twitter),
        "face|analyze face|analyze my pic|analyze my picture|analyze this picture": CmdFace(twitter),
        "derive|derivative": CmdDerive(twitter)
    }

# Process Tweet: When we find a tweet, process it and fire up any commands if needed
def process_tweet(tweet):
    if 'text' in tweet and 'id_str' in tweet:   # Every now and then, the stream might receive a non-tweet so this should check for an actual tweet
        text = tweet['text']
        tweet_id = tweet['id_str']

        # Make sure tweet was a mention of @WilburBot and not a mention of the string 'WilburBot'
        if '@wilburbot' in text.lower():    # We lower() the string text to catch all possible possibilities (e.g WILbURbot, wilburBOT, WILburBOT)
            user = tweet['user']['screen_name']

            # Loop through all possible commands in commands dictionary
            # Then we split the possible commands to check for possible aliases
            for command in commands:
                command_labels = command.split("|")

                command_executed = False

                for label in command_labels:
                    if label in text.lower():
                        commands[command].execute(user=user,tweet_id=tweet_id,text=text)
                        command_executed = True
                        break # Terminate from loop early in case the same command alias occurs twice in the text

                if command_executed == True:
                    break # Only process one command at a time to prevent command overload (Trying to reply back w/ more than 1 command)

init()
main()

if terminated == False:
    # Called when main stream closes.. NOTE: Killing Wilbur through Control+C will not run this
    twitter.post("Terminating main process. Either I've fallen asleep or was turned off manually", "Posted termination tweet")