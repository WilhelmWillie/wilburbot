'''
Util module stores helper methods that can be used by all Wilbur modules.
Helper methods can do things like truncate tweets, make HTTP requests, etc.
'''
import re

# Makes sure tweets don't exceed 140 characters
def truncate_tweet(tweet):
    if len(tweet) > 140:
        return tweet[:137] + "..."
    else:
        return tweet

# Reads a txt file from the static folder and converts it into a list of strings
def load_strings_from_file(file):
    with open("static/" + file + ".txt", "r") as f:
        lines = f.read().decode('utf-8').splitlines()

    return lines

# Adds tweets to Wilbur's tweet_collection so they can be used in the markov text generator
def add_tweets(statuses, wilbur):
    many = []
    for status in statuses:
        # We do not store tweets that: contain hashtags, mentions, or links
        can_store = True

        # Hashtags
        if len(status.entities['hashtags']) != 0:
            can_store = False

        # User Mentions
        if len(status.entities['user_mentions']) != 0:
            can_store = False

        # Links
        if  len(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', status.text)) > 0:
            can_store = False
            
        if can_store:
            if status.id_str not in wilbur.brain.tweet_collection:
                data = {'id': status.id_str, 'text': status.text}
                many.append(data)

                wilbur.brain.tweet_collection[data['id']] = data['text']
                wilbur.brain.add_to_corpus(data['text'])

    if len(many) != 0:
        wilbur.tweets.insert_many(many)
