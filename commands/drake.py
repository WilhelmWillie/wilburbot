#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ======================================== #
# File: drake.py                           #
# Logic for drake lyrics command           #
# ======================================== #

import random

class CmdDrake:
    twitter = None
    
    def __init__(self, twitter):
        self.twitter = twitter
        
    def execute(self, user, tweet_id, text):
        messages = [
                "I know they say the first love is the sweetest, but that first cut is the deepest.",
                "I live for the nights that I can't remember with the people that I won't forget.",
                "Better late than never but never late is better",
                "Lately I've been drinking like there's a message in a bottle",
                "Lights get low and that's when I have my brightest ideas",
                "You know its real when your latest nights are your greatest nights",
                "Tables turn, bridges burn, you live and learn.",
                "Last name Ever, first name Greatest, Like a sprained ankle, boy I ain't nothing to play with",
                "Everybody dies, but not everybody lives",
                "Somewhere between I want it and I got it",
                "Started from the bottom now we're here",
                "Swanging, eyes closed just swanging",
                "Cause you're a good girl and you know it. You act so different around me",
                "Just hold on, we're going home..",
                "Done saying, I'm done playing. Last time was on the outro",
                "I think I'm scared of what the future holds",
                "And no, I'm not saying I'm the nicest, I just live life like it",
                "Cry if you need to, but I can't stay to watch you, that's the wrong thing to do",
                "I realized I waited too long, but please don't move on",
                "I never had you, although I would be glad to",
                "I'm willing to work it out however long it takes you",
                "I better find your heart, I bet if I give all my love, then nothing's going to tear us apart",
                "I'm scared that every girl I care for will find a better man and end up happier in the long run",
                "I pop bottles because I bottle my emotions",
                "When the party's over, just don't forget me",
                "I tried to keep us together, you were busy keeping secrets",
                "I just hate sleeping alone",
                "I need you to rescue me from my destiny, I'm trying to live right and give you whatever's left of me",
                "You could have my heart or we could share it like the last slice.",
                "Baby you're my everything, you're all I ever wanted",
                "We could do it real big, bigger than you ever done it",
                "Sweat pants, hair tied, chillin' with no make-up on / That's when you're the prettiest",
                "Never pay attention to the remours and what they assume",
                "I'm more than just an option / Refuse to be forgotten",
                "I'd better find your lovin / I'd better find your heart",
                "I'm more than just a number / I doubt you'll find another",
                "You can't have my heart, the doctor told me I'd be dead without it",
                "Rest in peace to BIG and praises to the most high",
                "Rich enough that I don't have to tell 'em that I'm rich",
                "I dropped the ball on some personal shit, I need to embrace it",
                "I'm honest, I make mistakes, I'd be the second to admit it",
                "Think that's why I need her in my life, to check me when I'm trippin",
                "Bench players talkin' like starters.. I hate it",
                "Born a perfectionist, guess that makes me a bit obsessive",
                "You're still the one that I adore / Ain't much out there to have feelings for",
                "When the last time you did something for the first time?",
                "It's yours. It's always gonna be yours",
                "I've always liked my women book and street smart",
                "Time heals all, and heels hurt to walk in",
                "And my [DUVAL] girls, let me see your hands",
                "I feel like when she moves - the time doesn't",
                "The way I'm feeling, the things I say / all just happen",
                "I'm looking forward to the memories of right now/ Never forgettin from where I came from",
                "I think I have a chance at love but knowing me I miss it",
                "I'm in the world where things are taken, never given",
                "I need you right now, are you down to listen to me?",
                "I'm just saying you could do better",
                "But jealousy is just love and hate at the same time",
                "Jealousy in the air tonight, I could tell / I will never understand that but oh well",
                "I can't even listen / I'd much rather sit here in silence",
                "Take my crown to the grave, I'm an underground king",
                "Tell me lies, make it sound good",
                "I'm still in love, cause when it's that real, it's when it doesn't fade"
        ]
        
        index = random.randint(0, len(messages)-1)
        reply = "@" + user + ": \"" + messages[index] + "\" - Drake"
        
        self.twitter.reply(
            reply = reply, 
            reply_to = tweet_id, 
            success_log = "Gave Drake lyrics to " + user
        )