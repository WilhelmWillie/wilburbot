# Imports
import tweepy

class TweetListener(tweepy.StreamListener):
    def __init__(self, api, wilbur):
        self.api = api
        self.wilbur = wilbur

    def on_status(self, tweet):
        # When we detect a tweet, we make sure it mentions @WilburBot and isn't a retweet
        if "@" + self.wilbur.settings.screen_name.lower() in tweet.text.lower() and hasattr(tweet, 'retweeted_status') is False:
            print "Tweet Received:", tweet.text 
            self.wilbur.brain.process_tweet(tweet.text, tweet.author, tweet.id)
        
    def on_error(self, status):
        print status