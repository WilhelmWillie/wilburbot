import operator

PRIORITY = 1

'''
Returns true if user input is valid for this command
Usually some sort of RegEx or "x in y" statement would go here
'''
def is_valid(tweet):
    return "favorite stat" in tweet or "favorites stat" in tweet or "most favorited" in tweet

'''
Command logic goes here. 
When a tweet is processed, we return a response that will be added to the tweet queue
'''
def process(id, text, author, wilbur):
    favorites = wilbur.twitter_api.favorites(screen_name=author.screen_name, count=200)

    favorites_count = {}

    for tweet in favorites:
        author = tweet.user.screen_name

        if author in favorites_count:
            favorites_count[author] = favorites_count[author] + 1
        else:
            favorites_count[author] = 1

    

    if len(favorites_count) == 0:
        response = "Based on your last 200 tweets, you don't favorite anyone?"
    else:
        most_favorited = max(favorites_count.iteritems(), key=operator.itemgetter(1))[0]
        response = "Based on your last 200 favorites, you favorite @" + most_favorited + " (" + str(favorites_count[most_favorited]) + ") the most"
            
    return response