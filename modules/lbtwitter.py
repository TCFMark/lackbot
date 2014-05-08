#!/usr/bin/env python
'''
twitter.py - Improved Phenny Twitter Module
Copyright Mark Hearn
'''

import re, os, twitter, logging

r_username = re.compile(r'^[a-zA-Z0-9_]{1,15}$')
r_link = re.compile(r'^https?://twitter.com/\S+$')

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

def firstTimeAuth():
   logging.debug('Performing first time Twitter authentication')
   twat = twitter.Twitter(auth=twitter.OAuth(oauth_token, oauth_secret, consumer_token, consumer_secret))
   return twat

def twitterAuth():
   if 'twat' not in globals():
      global twat
      twat = firstTimeAuth()

def readUserLatestTweet(username):
   twitterAuth()
   response = twat.statuses.user_timeline(screen_name=username)
   
   try: 
      logging.debug('Reading ' + username + '\'s latest tweet')
      return response[0]['text'] + ' (@' + response[0]['user']['screen_name'] + ')'
   except IndexError:
      logging.debug('No tweets found for ' + username)
      return "No tweets found"
   
def readIDTweet(id):
   twitterAuth()
   response = twat.statuses.show(_id=id)
   
   try:
      logging.debug('Reading tweet with ID ' + id)
      return response['text'] + ' (@' + response['user']['screen_name'] + ')'
   except IndexError:
      logging.debug('No tweet found with ID ' + id)
      return "Tweet not found"
      
def readTweet(phenny, input):
   arg = input.group(2)
   if not arg:
      return phenny.reply("Give me a link, a username, or a tweet id")
   
   arg = arg.strip()
   if isinstance(arg, unicode):
      arg = arg.encode('utf-8')

   try:
      if arg.isdigit():
         logging.debug('.tw called with ID')
         phenny.say(readIDTweet(arg))
      elif r_username.match(arg):
         logging.debug('.tw called with username')
         phenny.say(readUserLatestTweet(arg))
      elif r_link.match(arg):
         logging.debug('.tw called with URL')
         tweetID = arg.split('/')[5]
         phenny.say(readIDTweet(tweetID))
      else: phenny.reply("Give me a link, a username, or a tweet id")  
   except:
      phenny.reply("Give me a link, a username, or a tweet id")  
   
readTweet.commands = ['tw']
readTweet.thread = True
      
def getRandomTweet():
   from ping import getWordList
   twitterAuth()
   
   for i in range(0,2):
      try:
         response = twat.search.tweets(q='%s' % getWordList(1)[0])
         logging.debug('Returning random tweet')
         return response['statuses'][0]
      except IndexError:
         pass   
      
   return None

def randomTweet(phenny, input):
   tweet = getRandomTweet()
   
   if tweet is None:
      logging.debug('.rtw called, but no tweet found')
      phenny.say('Sorry, I\'m rubbish at this')
      quit()
   
   output = tweet['text'] + ' (@' + tweet['user']['screen_name'] + ')'
   logging.debug('.rtw called, saying tweet: ' + output)
   phenny.say(output)
randomTweet.commands = ['rtw']
randomTweet.thread = True

def mangleRandomTweet():
   import tcfparty
   
   tweet = getRandomTweet()
   
   if tweet is None:
      return 'I \'m Sorry an error'
      quit()
   
   text = tweet['text']
   text = text.replace('@', '')
   text = text.replace('#', '')
   text = tcfparty.tcfparty(text)
   return text

def mood(phenny, input):
   logging.debug('.mood called, mangling a random tweet')
   phenny.say(mangleRandomTweet())
mood.commands = ['mood']
mood.thread = True

if __name__ == '__main__':
   print __doc__
