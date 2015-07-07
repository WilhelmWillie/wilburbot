import operator
import stats
import util

PRIORITY = 1

'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "word stat" in tweet or "most used word" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    statuses = author.timeline(count=200, include_rts=False)

    word_count = stats.get_word_count(statuses)

    most_used_words = sorted(word_count.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]

    response = "Based on your last 200 tweets, your " + str(len(most_used_words)) + " most used words are "

    for i in range(len(most_used_words)):
        response = response + "'" + most_used_words[i][0] + "' "
            
    # Store data in tweets collection
    util.add_tweets(statuses, wilbur)

    return response