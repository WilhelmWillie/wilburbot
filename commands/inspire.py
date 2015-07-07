import util
import random

PRIORITY = 1

# Data loaded in on initial load so we don't load strings on every request
data = util.load_strings_from_file('inspire')
    
'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "inspire" in tweet or "inspiration" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    return random.choice(data)