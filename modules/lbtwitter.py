#!/usr/bin/env python
'''
twitter.py - Improved Phenny Twitter Module
Copyright Mark Hearn
'''

import re, os, twitter

# Do all the boring credentials stuff
CONSUMER_CREDENTIALS = os.path.expanduser('~/.phenny/consumercredentials')
if not os.path.exists(CONSUMER_CREDENTIALS):
   print 'Please create a file at ' + CONSUMER_CREDENTIALS
   print 'First line of the file should be the app\'s Twitter API key'
   print 'Second line of the file should be the app\'s Twitter API secret'
   quit()

consumer_token, consumer_secret = twitter.read_token_file(CONSUMER_CREDENTIALS)

TWITTER_CREDENTIALS = os.path.expanduser('~/.phenny/twittercredentials')
if not os.path.exists(TWITTER_CREDENTIALS):
   twitter.oauth_dance("Lackbot", 
                       consumer_token, 
                       consumer_secret,
                       TWITTER_CREDENTIALS)

oauth_token, oauth_secret = twitter.read_token_file(TWITTER_CREDENTIALS)

t = twitter.Twitter(auth=twitter.OAuth(oauth_token, oauth_secret, consumer_token, consumer_secret))

def readtweet(phenny, input):
   response = t.statuses.user_timeline(screen_name=input.group(2))
   phenny.say(response)
readtweet.commands = ['tw', 'twitter']
readtweet.thread = True

if __name__ == '__main__':
   print __doc__
