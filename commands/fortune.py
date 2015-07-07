import util
import random

PRIORITY = 1

# Data loaded in on initial load so we don't load strings on every request
data = util.load_strings_from_file('fortune')
    
'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "open fortune cookie" in tweet or "fortune cookie" in tweet or "fortune" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    return random.choice(data)