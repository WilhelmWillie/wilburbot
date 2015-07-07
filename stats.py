# -*- coding: utf-8 -*-
import re
import time
import operator

'''
Stats module stores helper methods (Used by stat and report command)
'''

# INPUT: List of tweets
# OUTPUT: tuple containing (avg favorites, avg retweets)
def get_averages(statuses):
    fav_total, rt_total = 0, 0
    tweet_total = len(statuses)

    for tweet in statuses:
        fav_total += tweet.favorite_count
        rt_total += tweet.retweet_count

    fav_per_tweet = fav_total / float(tweet_total)
    rt_per_tweet = rt_total / float(tweet_total)

    return fav_per_tweet, rt_per_tweet

# INPUT: List of tweets
# OUTPUT: tuple containing (hour, pm/am)
def get_hour(statuses):
    hour_count = {}

    for tweet in statuses:
        # print tweet.text, str(tweet.created_at)
        hour = time.strftime('%H', time.strptime(str(tweet.created_at), '%Y-%m-%d %H:%M:%S'))
        
        hour = int(hour) - 4 # We have to subtract 4 hours from UTC

        if hour < 0:
            hour = 24 + hour
        if hour > 24:
            hour = hour - 24
        
        if hour in hour_count:
            hour_count[hour] = hour_count[hour] + 1
        else:
            hour_count[hour] = 1

    common_hour = max(hour_count.iteritems(), key=operator.itemgetter(1))[0]
    pm_or_am = "PM"

    percentage = round(float(hour_count[common_hour]) / len(statuses), 4) * 100

    if common_hour > 12:
        common_hour = common_hour - 12
    elif common_hour < 12:
        if common_hour == 0:
            common_hour = 12 # Fixed bug where user might receive 0 AM as their most common time
        pm_or_am = "AM"

    return common_hour, pm_or_am

# INPUT: List of tweets
# OUTPUT: Dictionary with emoji count
def get_emoji(statuses):
    emoji_count = {}

    # Found online, RegEx pattern for finding emojis
    try:
        emoji_pattern = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        emoji_pattern = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    for tweet in statuses:
        emojis_in_tweet = emoji_pattern.findall(tweet.text)

        for e in emojis_in_tweet:
            if e in emoji_count:
                emoji_count[e] = emoji_count[e] + 1
            else:
                emoji_count[e] = 1

    if len(emoji_count) == 0:
        res = "N/A"
    else:
        res = max(emoji_count.iteritems(), key=operator.itemgetter(1))[0]

    return res

# INPUT: List of tweets
# OUTPUT: Dictionary with word count
def get_word_count(statuses):
    word_count = {}

    # Words in common_words will not be included in word count
    common_words = ['ur','was','am','we','did','had','like','always','away','u','is','me','so', 'if', 'who','are','than','just','can','your','you','what','when','where','how','stats','time', 'person', 'year', 'way', 'day', 'thing', 'man', 'world', 'life', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point', 'government', 'company', 'number', 'group', 'problem', 'fact', 'be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see', 'come', 'think', 'look', 'want', 'give', 'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try', 'leave', 'call', 'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own', 'other', 'old', 'right', 'big', 'high', 'different', 'small', 'large', 'next', 'early', 'young', 'important', 'few', 'public', 'bad', 'same', 'able', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'beneath', 'under', 'above', 'the', 'and', 'a', 'that', 'i', 'it', 'im', 'u', 'ur', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'EXIT', '', 'break;', 'time', 'person', 'year', 'way', 'day', 'thing', 'man', 'world', 'life', 'hand', 'part', 'child', 'eye', 'woman', 'place', 'work', 'week', 'case', 'point', 'government', 'company', 'number', 'group', 'problem', 'fact', 'be', 'have', 'do', 'say', 'get', 'make', 'go', 'know', 'take', 'see', 'come', 'think', 'look', 'want', 'give', 'use', 'find', 'tell', 'ask', 'work', 'seem', 'feel', 'try', 'leave', 'call', 'good', 'new', 'first', 'last', 'long', 'great', 'little', 'own', 'other', 'old', 'right', 'big', 'high', 'different', 'small', 'large', 'next', 'early', 'young', 'important', 'few', 'public', 'bad', 'same', 'able', 'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'over', 'after', 'beneath', 'under', 'above', 'the', 'and', 'a', 'that', 'i', 'it', 'not', 'he', 'as', 'you', 'this', 'but', 'his', 'they', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their']
          
    for tweet in statuses:
        words = tweet.text.lower().split()

        for word in words:
            if word not in common_words and word.isalpha():
                if word in word_count:
                    word_count[word] = word_count[word] + 1
                else:
                    word_count[word] = 1

    return word_count

 # INPUT: List of tweets
 # OUTPUT: Dictionary with mention count
def get_mention_count(statuses):
    mention_count = {}

    for tweet in statuses:
        user_mentions = tweet.entities['user_mentions']

        for mention in user_mentions:
            user_mentioned = mention['screen_name']

            if user_mentioned in mention_count:
                mention_count[user_mentioned] = mention_count[user_mentioned] + 1
            else:
                mention_count[user_mentioned] = 1

    return mention_count