import stats
import operator
import util
import datetime

PRIORITY = 1

'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "generate report" in tweet or "report" in tweet or "generate my report" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    statuses = author.timeline(count=200, include_rts=False)

    # Part 1 = Get statistical data for reports
    fav_per_tweet, rt_per_tweet = stats.get_averages(statuses)

    # Round our numbers
    fav_per_tweet = round(fav_per_tweet, 3)
    rt_per_tweet = round(rt_per_tweet, 3)

    emoji = stats.get_emoji(statuses)
    hour = str(stats.get_hour(statuses)[0]) + " " + stats.get_hour(statuses)[1]

    word_count = stats.get_word_count(statuses)
    mention_count = stats.get_mention_count(statuses)

    sorted_words = sorted(word_count.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]
    sorted_mention = sorted(mention_count.iteritems(), key=operator.itemgetter(1), reverse=True)[:5]

    most_used_words = []
    for word in sorted_words:
        most_used_words.append(word[0])

    most_mentioned = []
    for mention in sorted_mention:
        most_mentioned.append(mention[0]);

    # Part 2 = Store data in reports collection
    data = {
        'twitterHandle': author.screen_name,
        'avgFavorites': fav_per_tweet,
        'avgRetweets': rt_per_tweet,
        'mostUsedEmoji': emoji,
        'mostActiveHour': hour,
        'mostUsedWords': most_used_words,
        'mostMentioned': most_mentioned,
        'updated': datetime.datetime.now().strftime("%m/%d %H:%M")
    }

    wilbur.reports.update({'twitterHandle': author.screen_name}, {"$set": data}, upsert=True)

    response = "View your report at http://wilbur.wilhelmwillie.com/report/" + author.screen_name

    # Part 3 = Store data in tweets collection
    util.add_tweets(statuses, wilbur)

    return response