# Imports
from apscheduler.schedulers.background import BackgroundScheduler
from brain import Brain
from listener import TweetListener
from pymongo import MongoClient
import Queue
import tweepy
import util
import traceback
import logging

class Wilbur(object):
    def __init__(self, settings, debug, announce):
        self.settings = settings
        self.twitter_keys = settings.twitter
        self.debug = debug
        self.announce = announce

        # Set up the twitter API
        self.auth = tweepy.OAuthHandler(
            self.twitter_keys['consumer_key'],
            self.twitter_keys['consumer_secret'])
        self.auth.set_access_token(
            self.twitter_keys['access_key'],
            self.twitter_keys['access_secret'])
        self.twitter_api = tweepy.API(self.auth)

        # Set up MongoDB connection
        self.client = MongoClient()
        self.db = self.client.wilbur 
        self.reports = self.db.reports
        self.tweets = self.db.tweets

        self.tweet_queue = Queue.Queue()
        logging.basicConfig()
        self.scheduler = BackgroundScheduler()
        self.brain = Brain(self)


    # Mutator method used by other modules to add to the tweet queue
    def add_to_queue(self, response):
        print "Added to Queue:", response
        self.tweet_queue.put(response)

    # Grab the oldest tweet from queue and post/print it
    def post_from_queue(self):
        if self.tweet_queue.empty():
            return

        res = self.tweet_queue.get()

        # We get the oldest tweet and truncate it to make sure it doesn't go over 140 characters
        tweet = util.truncate_tweet(res.to_string())

        # In debug mode, we print the tweet to console. Otherwise, we pass it to twitter's API
        if self.debug: 
            pass
        else:
            try:
                self.twitter_api.update_status(status=tweet, in_reply_to_status_id=res.id)
            except Exception as e:
                print e
                traceback.print_exc()

        print "Attempted to tweet:", tweet

    '''
    Main loop for Wilbur. Uses an inner loop that waits for twitter replies/CLI input
    Asynchronously, a scheduled interval job runs every 40 seconds that posts the oldest tweet in queue
    '''
    def run(self):
        # If the script is run with the announce argument, we post an announcement tweet
        if self.announce:
            self.twitter_api.update_status(status=self.settings.parse_message(self.settings.get_announce()))
 
        # Start interval for tweeting from queue
        self.scheduler.add_job(self.post_from_queue, 'interval', seconds=40) # 90 tweets per hour to prevent Wilbur from burning out
        self.scheduler.start()

        '''
        If we're in debug mode:
            We run a while loop that gathers input from the CLI rather than from the twitter API
        else 
            We start a twiter user stream that waits for replies to the bot account.

        When inputs are received, they are sent to Wilbur's brain where they are processed
        After being processed, they are sent back to Wilbur's queue and will wait to be posted

        A try-except clause is used to make sure we handle any errors gracefully
        '''
        try:
            if self.debug:
                author = raw_input("Who's profile are you tweeting from? ")
                author = self.twitter_api.get_user(author)

                while True:
                    text = raw_input("Tweet: ")
                    print "Added to queue: " + self.brain.process_tweet(text=text, author=author)
            else:
                listener = TweetListener(self.twitter_api, self)
                stream = tweepy.Stream(self.auth, listener)
                stream.userstream(replies='all') 
        except Exception as e:
            print e
            traceback.print_exc()

            if not self.debug:
                # Make emergency post if error occurs
                self.twitter_api.update_status(status="An error occured while running.. @" + self.settings.owner + " fix it!")
        else:
            if not self.debug:
                # Tweet shutdown post. Error didn't occur, stream might have timed out or something like that
                self.twitter_api.update_status(status=self.settings.get_shutdown())