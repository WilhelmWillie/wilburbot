#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: cmd_words.py                       #
# Logic for words command                  #
# ======================================== #
import re
import operator

class Words:
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

        if self.twitter.reply(reply=reply, reply_to=tweet_id) == True:
            print "[UPDATE] Gave word stats to " + user
        else:
            print "[ERROR] Something went wrong giving word stats to " + user