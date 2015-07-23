#!/usr/bin/env python
"""
wikipedia.py - Phenny Wikipedia Module
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import urllib, urllib2, json
import tcfparty, logging

wikiuri = 'https://%s.wikipedia.org/w/api.php?'

def wikipedia(term, language):
   opener = urllib2.build_opener()
   term = urllib.quote(term)
   u = wikiuri % language
   logging.debug("Fetching from " + u + "action=query&prop=extracts&exintro=&explaintext=&exsentences=1&format=json&titles=" + term)
   result = opener.open(u + "action=query&prop=extracts&exintro=&explaintext=&exsentences=1&format=json&titles=" + term)
   data = json.load(result)
   sentence = data['query']['pages'].itervalues().next()['extract']

   if sentenceOnly is True:
      return sentence

   return sentence + (' - http://%s.wikipedia.org/wiki/%s' % (language, term))

def wikwrapper(origterm):
   origterm = origterm.encode('utf-8')

   term = urllib.unquote(origterm)
   language = 'en'
   if term.startswith(':') and (' ' in term):
      a, b = term.split(' ', 1)
      a = a.lstrip(':')
      if a.isalpha():
         language, term = a, b
   term = term[0].upper() + term[1:]
   term = term.replace(' ', '_')

   try: result = wikipedia(term, language)
   except IOError:
      args = (language, wikiuri % (language, term))
      error = "Can't connect to %s.wikipedia.org (%s)" % args
      return error

   if result is not None:
      return result
   else:
      return 'Can\'t find anything in Wikipedia for "%s".' % origterm

def wik(phenny, input):
   if not input.group(2):
      phenny.say('Perhaps you meant ".wik Zen"?')
      return

   global sentenceOnly
   sentenceOnly = False
   logging.debug('Getting Wikipedia article for ' + input.group(2))
   result = wikwrapper(input.group(2)).decode('utf-8')
   logging.debug('"' + input.group(2) + '" returned ' + result)
   phenny.say(result)
wik.commands = ['wik']
wik.priority = 'high'

def randomArticle():
   import xml.etree.ElementTree as ET

   from urllib2 import Request, urlopen, URLError
   request = Request('http://en.wikipedia.org/w/api.php?action=query&list=random&rnnamespace=0&rnlimit=1&format=xml')
   try:
      response = urlopen(request).read()
      root = ET.fromstring(response)
      for page in root.iter('page'):
         atts = page.attrib
         return wikwrapper(atts['title'])
   except URLError, e:
      return "No response from Wikipedia, sorry."

def rwik(phenny, input):
   global sentenceOnly
   sentenceOnly = False
   logging.debug('.rwik called, getting random article')
   result = randomArticle()
   logging.debug('.rwik returned ' + result)
   phenny.say(result)
rwik.commands = ['rwik']
rwik.priority = 'high'

def getFact():
   global sentenceOnly
   sentenceOnly = True

   factoid = randomArticle()
   try:
      factoid = tcfparty.tcfparty(factoid)
      return factoid
   except UnicodeDecodeError:
      logging.debug('getFact failed, lackbot having a mood')
      import lbtwitter
      return lbtwitter.mangleRandomTweet()

   sentenceOnly = False

def fact(phenny, input):
   logging.debug('.fact called, getting "fact"')
   factoid = getFact()
   phenny.say("Fact! " + factoid)
fact.rule = r'(?i).*fact.*'
fact.priority = 'high'

if __name__ == '__main__':
   print __doc__.strip()
