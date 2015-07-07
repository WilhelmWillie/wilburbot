# -*- coding: utf-8 -*-
# Imports
import pkgutil
import paths
import traceback
import random

class Brain(object):
    def __init__(self, wilbur):
        self.wilbur = wilbur
        self.commands = self.load_commands()

        # Used for generating text from user tweets
        self.tweet_collection = {} # Key: Tweet ID, Value: Tweet
        self.corpus = {} # Stores markov chains
        self.load_tweets() # Load tweets from MongoDB collection into tweet_collection
        self.init_corpus() # Takes tweets from tweet_collection and creates the markov chains for corpus

    # Walks through modules in the commands folder and stores them in a list
    def load_commands(self):
        commands = []

        locations = [paths.CMD_PATH]
        for finder, name, pkg in pkgutil.walk_packages(locations):
            # We try loading the module in.. If it draws an error, we ignore it and move on. Otherwise we add it to the commands list
            try:
                loader = finder.find_module(name)
                cmd = loader.load_module(name)
            except Exception as e:
                print e
                print "Error occured while trying to find module.. Moving on.."
            else:
                commands.append(cmd)

        # Finally, we sort it out based on the priority value stored in the command module. Higher numbers = higher priority
        commands.sort(key=lambda mod: mod.PRIORITY if hasattr(mod, 'PRIORITY') else 0, reverse=True)

        command_names = ""
        for command in commands:
            command_names = command_names + command.__name__ + " "
        print "Commands loaded in:", command_names

        return commands

    # Called when tweet is detected, finds a matching command to a request and returns a response
    def process_tweet(self, text, author, id=0):
        for command in self.commands:
            if command.is_valid(text.lower()):
                try:
                    response_text = command.process(id, text, author, self.wilbur)
                    response = Response(author.screen_name, response_text, id)
                except Exception as e:
                    print e
                    traceback.print_exc()
                    print "Error occured while trying to process tweet.. Moving on.."
                else:
                    self.wilbur.add_to_queue(response)
                    return response.to_string()

        response = Response(author.screen_name, self.generate_convo_text(), id)
        self.wilbur.add_to_queue(response)
        return response.to_string() 

    # Used for generating pseudo-text whenever a request doesn't match a command (Conversation)
    def generate_convo_text(self):
        new_text = ""

        count = 0
        max_iter = random.choice(range(10, 20))

        key = random.choice(self.corpus.keys())

        new_text = new_text + key[0] + " " + key[1] + " "

        while (key in self.corpus) and (count < max_iter):
            next_word = random.choice(self.corpus[key])
            new_text = new_text + next_word + " "

            key = (key[1], next_word)
            count = count + 1

        return new_text

    # Loads tweets from MongoDB collection
    def load_tweets(self):
        for tweet in self.wilbur.tweets.find():
            self.tweet_collection[tweet['id']] = tweet['text']

    # Initializes corpus
    def init_corpus(self):
        for id in self.tweet_collection:
            text = self.tweet_collection[id]
            words = text.split()

            if len(words) > 3:
                for i in range(len(words) - 2):
                    key = (words[i], words[i+1])
                    value = words[i+2]

                    if key in self.corpus:
                        self.corpus[key].append(value)
                    else:
                        self.corpus[key] = [value]
                
    # Add to corpus
    def add_to_corpus(self, text):
        words = text.split()

        if len(words) > 3:
            for i in range(len(words) - 2):
                key = (words[i], words[i+1])
                value = words[i+2]

                if key in self.corpus:
                    self.corpus[key].append(value)
                else:
                    self.corpus[key] = [value]

# Response class that holds a potential tweet's text and reply ID
class Response(object):
    def __init__(self, at, text, id):
        self.at = at
        self.text = text
        self.id = id

    def to_string(self):
        return "@" + self.at + " " + self.text
