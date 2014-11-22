#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_stats.py                       #
# Contains classes for all "stat" variants #
# Basic, emoji, favorites, mention, words, #
# time.. what's next? :)                   #
# ======================================== #

import re
import operator
import time

################################################################################

class CmdBasicStats:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        fav_count, rt_count = 0, 0
        tweet_count = len(user_statuses)
        
        for tweet in user_statuses:
            fav_count += tweet['favorite_count']
            rt_count += tweet['retweet_count']
            
        fav_per_tweet = round((fav_count / float(tweet_count)), 3)
        rt_per_tweet = round((rt_count / float(tweet_count)), 3)
        reply = "@" + user + ": Based on your last 200 tweets, you average " + str(fav_per_tweet) + " favorites and " + str(rt_per_tweet) + " retweets per tweet! #WilburBot"
        
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave basic stats to " + user
        )

################################################################################

class CmdEmojiStats:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        emoji_count = {}
        total = 0   # Used for calculating percentage at the end
        
        # Found online, RegEx pattern for finding emojis
        try:
            emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            emoji_pattern = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
            
        # Loop through tweets and use RegEx to find emojis. Loop through all found emojis and add to emoji_count
        for tweet in user_statuses:
            emojis_in_tweet = emoji_pattern.findall(tweet['text'])
            
            for e in emojis_in_tweet:
                total = total + 1
                
                if e in emoji_count:
                    emoji_count[e] = emoji_count[e] + 1
                else:
                    emoji_count[e] = 1
                    
        reply = ""
        
        # There's a chance a user won't have any emojis, if this is the case prepare a fallback reply
        if len(emoji_count) == 0:
            reply = "@" + user + ": Based on your last 200 tweets, you don't seem to use emojis at all #TeamAndroid ?"
        else:
            most_used_emoji = max(emoji_count.iteritems(), key=operator.itemgetter(1))[0]
            percentage = round(float(emoji_count[most_used_emoji]) / total, 5) * 100
            reply = "@" + user + ": Based on your last 200 tweets, your most used emoji is " + most_used_emoji + " (" + str(percentage) + "%) #WilburBot"

        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave emoji stats to " + user
        )

################################################################################

class CmdFavoriteStats:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        favorites = self.twitter.get_favorites(name=user)
        
        favorites_count = {}
    
        # Loop through all favorites and add to favorites_count
        for tweet in favorites:
            author = tweet['user']['screen_name']

            if author in favorites_count:
                favorites_count[author] = favorites_count[author] + 1
            else:
                favorites_count[author] = 1
                    
        reply = ""
        
        # There's a chance a user won't favorite anyone, if this is the case prepare a fallback reply
        if len(favorites_count) == 0:
            reply = "@" + user + ": Based on your last 200 favorites, you don't favorite anyone?"
        else:
            most_favorited = max(favorites_count.iteritems(), key=operator.itemgetter(1))[0]
            reply = "@" + user + ": Based on your last 200 favorites, you favorite @" + most_favorited + " (" + str(favorites_count[most_favorited]) + ") the most #WilburBot"
            
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave favorite stats to " + user
        )

################################################################################

class CmdMentionStats:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        mention_count = {}
            
        # Loop through tweets and find mentions. Loop through all found mentions and add to mention_count
        for tweet in user_statuses:
            user_mentions = tweet['entities']['user_mentions']
            
            for mention in user_mentions:
                user_mentioned = mention['screen_name']
                
                if user_mentioned in mention_count:
                    mention_count[user_mentioned] = mention_count[user_mentioned] + 1
                else:
                    mention_count[user_mentioned] = 1
                    
        reply = ""
        
        # There's a chance a user won't mention anyone, if this is the case prepare a fallback reply
        if len(mention_count) == 0:
            reply = "@" + user + ": Based on your last 200 tweets, you don't talk to anyone on twitter"
        else:
            most_mentioned = max(mention_count.iteritems(), key=operator.itemgetter(1))[0]
            reply = "@" + user + ": Based on your last 200 tweets, you mention @" + most_mentioned + " the most #WilburBot"
            
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave mention stats to " + user
        )

################################################################################

class CmdWordStats:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        word_count = {}
        
        # Words in common_words will not be included in word count
        common_words = ['ur','was','am','we','did','had','like','always','away','u','is','me','so', 'if', 'who','are','than','just','can','your','you','what','when','where','how','stats','time', 'person', 'year', 'way', 'day', 'thing', 'man', 'world', 'life', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point', 'government', 'company', 'number', 'group', 'problem', 'fact', 'be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see', 'come', 'think', 'look', 'want', 'give', 'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try', 'leave', 'call', 'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own', 'other', 'old', 'right', 'big', 'high', 'different', 'small', 'large', 'next', 'early', 'young', 'important', 'few', 'public', 'bad', 'same', 'able', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'beneath', 'under', 'above', 'the', 'and', 'a', 'that', 'i', 'it', 'im', 'u', 'ur', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'EXIT', '', 'break;', 'time', 'person', 'year', 'way', 'day', 'thing', 'man', 'world', 'life', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point', 'government', 'company', 'number', 'group', 'problem', 'fact', 'be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see', 'come', 'think', 'look', 'want', 'give', 'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try', 'leave', 'call', 'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own', 'other', 'old', 'right', 'big', 'high', 'different', 'small', 'large', 'next', 'early', 'young', 'important', 'few', 'public', 'bad', 'same', 'able', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'beneath', 'under', 'above', 'the', 'and', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their']
            
        for tweet in user_statuses:
            words = tweet['text'].lower().split()
            
            for word in words:
                if word not in common_words and word.isalpha():
                    if word in word_count:
                       word_count[word] = word_count[word] + 1
                    else:
                        word_count[word] = 1
                    
        reply = ""
        
        most_used_words = sorted(word_count.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
        reply = "@" + user +": Based on your last 200 tweets, your 5 most used words are "

        for i in range(0,5):
            if i <= 3:
                reply = reply + "'" + most_used_words[i][0] + "', "
            else:
                reply = reply + "and '" + most_used_words[i][0] + "'"

        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave word stats to " + user
        )

################################################################################

class CmdTimeStats:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        user_statuses = self.twitter.get_user_timeline(name=user)
        
        hour_count = {}
            
        for tweet in user_statuses:
            hour = time.strftime('%H', time.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
            
            hour = int(hour) - 5 # Time they give us is in UTC. We subtract 5 hours to convert it to EST

            if hour < 0:
                hour = 24 + hour
            if hour > 24:
                hour = hour - 24
            
            if hour in hour_count:
                hour_count[hour] = hour_count[hour] + 1
            else:
                hour_count[hour] = 1
                    
        reply = ""
        
        if len(hour_count) == 0:
            reply = "@" + user + ": Based on your last 200 tweets, you don't tweet... at all.. ???"
        else:
            common_hour = max(hour_count.iteritems(), key=operator.itemgetter(1))[0] 
            pm_or_am = "PM"
            
            percentage = round(float(hour_count[common_hour]) / len(user_statuses), 4) * 100
            
            if common_hour > 12:
                common_hour = common_hour - 12
            elif common_hour < 12:
                pm_or_am = "AM"
                
            reply = "@" + user + ": Based on your last 200 tweets, you tweet the most during the hour of " + str(common_hour) + " " + pm_or_am + " EST (" + str(percentage) + "%) #WilburBot"

        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave time stats to " + user
        )