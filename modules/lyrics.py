'''
lyrics.py - Utilises the LyricWiki API to grab song lyrics
'''

import logging, string, urllib2, json
from urllib import quote

def getLyrics(artist, song):
   artist, song = quote(artist), quote(song)
   url = 'http://lyrics.wikia.com/api.php?artist=' + artist + '&song=' + song + '&fmt=realjson'
   
   logging.debug('Sending URL: ' + url)
   opener = urllib2.build_opener()
   result = opener.open(url)
   data = json.load(result)

   if data['lyrics'] == "Not found":
      return "Sorry, no lyrics found"
   else:
      return data['url']

def lyrics(phenny, input):
   args = input.group(2)

   if (not args) or (not ',' in args):
      phenny.say('Perhaps you meant ".lyrics Radiohead, Paranoid Android?"')
      return
   
   args = string.split(args, ',', 1)
   artist, song = args[0], args[1]
   artist, song = string.strip(artist), string.strip(song)
   
   logging.debug('Getting lyrics for ' + song + ' by ' + artist)
   url = getLyrics(artist, song)
   logging.debug('getLyrics response: ' + url)
   phenny.reply(url)
lyrics.commands = ['lyrics']
lyrics.example = '.lyrics Radiohead, Paranoid Android'