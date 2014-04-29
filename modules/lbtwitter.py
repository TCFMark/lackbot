#!/usr/bin/env python
'''
twitter.py - Improved Phenny Twitter Module
Copyright Mark Hearn
'''

import re, os, twitter

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
      return response[0]['text'] + ' (@' + response[0]['user']['screen_name'] + ')'
   except IndexError:
      return "No tweets found"
   
def readIDTweet(id):
   twitterAuth()
   response = twat.statuses.show(_id=id)
   
   try:
      return response['text'] + ' (@' + response['user']['screen_name'] + ')'
   except IndexError:
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
         phenny.say(readIDTweet(arg))
      elif r_username.match(arg):
         phenny.say(readUserLatestTweet(arg))
      elif r_link.match(arg):
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
         return response['statuses'][0]
      except IndexError:
         pass   
      
   return None

def randomTweet(phenny, input):
   tweet = getRandomTweet()
   
   if tweet is None:
      phenny.say('Sorry, I\'m rubbish at this')
      quit()
   
   phenny.say(tweet['text'] + ' (@' + tweet['user']['screen_name'] + ')')
randomTweet.commands = ['rtw']
randomTweet.thread = True

def mangleRandomTweet():
   import tcfparty
   
   tweet = getRandomTweet()
   
   if tweet is None:
      phenny.say('I \'m Sorry an error')
      quit()
   
   text = tweet['text']
   text = tcfparty.tcfparty(text)
   return text

def mood(phenny, input):
   phenny.say(mangleRandomTweet())
mood.commands = ['mood']
mood.thread = True

if __name__ == '__main__':
   print __doc__
