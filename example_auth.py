#!/usr/bin/env python

# ======================================== #
# File: example_auth.py                    #
# Copy of auth.py except all confidential  #
# data is redacted                         #
# ======================================== #

from twitter import *

# File for Wilbur's OAuth credentials (Generated once using oauth_dance provided by twitter package)
WILBUR_AUTH = "./wilbur_auth"

# Twitter API consumer keys, necessary for authentication to twitter
CONSUMER_KEY = "key.to.bill.gates.mansion"
CONSUMER_SECRET = "the.illuminati"

OAUTH_TOKEN, OAUTH_SECRET = read_token_file(WILBUR_AUTH)

def get_oauth():
    return OAuth(AUTH_TOKEN, OAUTH_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

