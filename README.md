# WilburBot 2.0

WilburBot is a friendly twitter bot developed by Wilhelm Willie. Starting off as an experiment with python and the twitter API, WilburBot has turned into a somewhat-intelligent bot capable of processing a variety of commands. 

Listed below are some of the things Wilbur can do:
  - Generate random somewhat intelligible text through the use of markov chains
  - Create online reports on a user's twitter profile on request ([example])
  - Calculate a variety of stats for a user's twitter profile such as his/her most used words, their average retweets/favorites per tweet, and more
  - Give users random motivation/inspiration, quote Drake lyrics, or give fortune cookie fortunes

To read more about Wilbur see: http://wilbur.wilhelmwillie.com  
To see a list of commands: http://wilbur.wilhelmwillie.com/commands

WilburBot was created by Wilhelm Willie ([twitter])  
If you have any questions, feel free to contact me. If you would like to use my code, create your own bot, or contribute to WilburBot, go ahead. I currently don't have instructions on how to create your own bot using this code but if you flip through my code, it might become clear.

### How Wilbur Works

Wilbur relies on twitter's streaming API to detect requests and mentions. When Wilbur is started, he starts a twitter stream for collecting input. In addition, he uses APScheduler to schedule an output method to be called every 40 seconds.

The twitter stream runs on the main thread and will sit and wait for new incoming tweets. On detection, Wilbur will make sure the tweet actually mentions Wilbur and isn't a retweet. If the tweet meets the requirements, it is fed to the Brain.

Inside the Brain, Wilbur will figure out which command the user has requested. After finding the appropriate command, Wilbur will process the tweet and create a Response that will be pushed to a tweet queue. If the tweet doesn't match any command, Wilbur will generate random text using markov chains (I will write something about this some other time, it's a fascinating subject) and push that to the tweet queue.

Now, back to the scheduled method for outputting processed tweets. Every 40 seconds, a method will be called that grabs the oldest tweet in the queue and attempts to tweet it. This queue functionality means that Wilbur doesn't reply instantly. However, in return, if Wilbur gets flooded with requests in a short period of time, the queue and timer will ensure that Wilbur doesn't tweet too many tweets all at once therefore resulting in twitter jail.

### Tech

Wilbur depends on a variety of libraries and technologies to function
  - APScheduler - Allows for methods to be run on intervals, simplifies the process of threading and etc.
  - Tweepy - Allows for accessing the twitter API
  - PyMongo and MongoDB - Used for storing tweets and reports

Note: MongoDB is used rather than MySQL because many of my projects on wilhelmwillie.com use NodeJS/MongoDB. Instead of installing an additional MySQL database, I went ahead and had Wilbur use PyMongo to interface with the existing Mongo database. 

### License
The MIT License (MIT)

Copyright (c) 2015 Wilhelm Willie

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

[example]:http://wilbur.wilhelmwillie.com/report/Willieminati
[twitter]:http://twitter.com/Willieminati