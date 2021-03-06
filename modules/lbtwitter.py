#!/usr/bin/env python
'''
twitter.py - Improved Phenny Twitter Module
Copyright Mark Hearn
'''

import re, os, twitter, logging, HTMLParser
h = HTMLParser.HTMLParser()

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

names = ['Bob', 'Bert', 'Keith', 'Clive', 'Nigel', 'Derek', 'Steve', 'Trevor', 'Fred', 'Kenneth', 'Gerry', 'Barry', 'Graham']

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
      message = response[0]['text'] + ' (@' + response[0]['user']['screen_name'] + ')'
      message = h.unescape(message)
      return message
   except IndexError:
      logging.debug('No tweets found for ' + username)
      return "No tweets found"
   
def replaceNewlines(tring):
   while '\n' in tring:
      tring = tring.replace('\n', ' | ')
   while ' |  | ' in tring:
      tring = tring.replace(' |  | ', ' | ')
   return tring
   
def readIDTweet(id):
   twitterAuth()
   response = twat.statuses.show(_id=id)
   
   try:
      logging.debug('Reading tweet with ID ' + id)
      message = response['text'] + ' (@' + response['user']['screen_name'] + ')'
      message = h.unescape(message)
      return message
   except IndexError:
      logging.debug('No tweet found with ID ' + id)
      return "Tweet not found"
      
def readTweet(phenny, input):
   """Gets the latest tweet for a username, or a specific tweet from a URL or tweet ID"""
   arg = input.group(2)
   if not arg:
      return phenny.reply("Give me a link, a username, or a tweet id")
   
   arg = arg.strip()
   if isinstance(arg, unicode):
      arg = arg.encode('utf-8')

   try:
      if arg.isdigit():
         logging.debug('.tw called with ID')
         message = readIDTweet(arg)
      elif r_username.match(arg):
         logging.debug('.tw called with username')
         message = readUserLatestTweet(arg)
      elif r_link.match(arg):
         logging.debug('.tw called with URL')
         tweetID = arg.split('/')[5]
         message = readIDTweet(tweetID)
      else: 
         phenny.reply("Give me a link, a username, or a tweet id")  
         return
      
      message = replaceNewlines(message)
      phenny.say(message)
   except:
      phenny.reply("Give me a link, a username, or a tweet id")  
readTweet.commands = ['tw']
readTweet.thread = True
readTweet.example = '.tw https://twitter.com/TCFMark/status/440861994263269376'
      
def getRandomTweet(searchterm=''):
   from ping import getWordList
   twitterAuth()
   
   for i in range(0,2):
      try:
         if not searchterm:
            searchterm = getWordList(1)[1]
         response = twat.search.tweets(q='%s' % searchterm)
         logging.debug('Returning random tweet: http://twitter.com/' + 
                       response['statuses'][0]['user']['screen_name'] + '/status/' +
                       response['statuses'][0]['id_str'])
         logging.debug('    Search term: ' + searchterm)
         tweet = response['statuses'][0]
         tweet = h.unescape(tweet)
         return tweet
      except IndexError:
         pass   
      
   return None

def searchTweet(phenny, input):
   arg = input.group(2)
   if not arg:
      return phenny.reply("I need a search term.")
   
   tweet = getRandomTweet(searchterm=arg)
   if tweet is None:
      logging.debug('.stw called with arg "' + arg + ', but no tweet found')
      phenny.say("I didn't find anything for " + arg)
      return

   output = tweet['text'] + ' (@' + tweet['user']['screen_name'] + ')'
   logging.debug('.stw called with arg "' + arg + '", saying tweet: ' + output)

   output = replaceNewlines(output)
   phenny.say(output)
searchTweet.commands = ['stw']
searchTweet.thread = True
searchTweet.example = '.stw cumpkin'

def randomTweet(phenny, input):
   tweet = getRandomTweet()
   
   if tweet is None:
      logging.debug('.rtw called, but no tweet found')
      phenny.say('Sorry, I\'m rubbish at this')
      return
   
   output = tweet['text'] + ' (@' + tweet['user']['screen_name'] + ')'
   logging.debug('.rtw called, saying tweet: ' + output)
   
   output = replaceNewlines(output)
   phenny.say(output)
randomTweet.commands = ['rtw']
randomTweet.thread = True

def mangleRandomTweet():
   import tcfparty
   
   tweet = getRandomTweet()
   
   if tweet is None:
      logging.warn('No tweets found.')
      return 'I\'m sorry, I didn\'t find any tweets.'
      quit()
   
   text = tweet['text']
   
   # Replace usernames with real names
   if '@' in text:
      import random
      logging.debug('Replacing usernames with real names')
      matches = re.findall(r'(?:^|\s)(@.+?)(?=$|\s)', text)
      matches = set(matches)
      for match in matches:
         logging.debug('    Name found: ' + match)
         text = text.replace(match, random.choice(names))

   text = text.replace('#', '')
   text = tcfparty.tcfparty(text)
   return text

def mood(phenny, input):
   """Mangles a tweet through TCFParty because the Internet"""
   logging.debug('.mood called, mangling a random tweet')
   phenny.say(mangleRandomTweet())
mood.commands = ['mood']
mood.thread = True

if __name__ == '__main__':
   print __doc__
