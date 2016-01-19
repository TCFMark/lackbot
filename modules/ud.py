'''
ud.py - phenny urban dictionary definitions module
'''

import logging, json, urllib2
from urllib import quote

# Useful example: http://api.urbandictionary.com/v0/define?term=rungient

def fetchJson(term):
   opener = urllib2.build_opener()
   term = quote(term)
   logging.debug('Fetching from http://api.urbandictionary.com/v0/define?term=' + term)
   result = opener.open('http://api.urbandictionary.com/v0/define?term=' + term)
   data = json.load(result)
   return data

def removeSquareBrackets(tring):
   while(('[' or ']') in tring):
      tring = tring.replace('[', '')
      tring = tring.replace(']', '')
   return tring

def format(tring):
   removeSquareBrackets(tring)
   while '\n' in tring:
      tring = tring.replace('\n', ' | ')
   while ' |  | ' in tring:
      tring = tring.replace(' |  | ', ' | ')
   return tring

def ud(phenny, input):
   term = input.group(2)
   if not term:
      phenny.say('No term specified')
      quit()
   
   logging.debug('Getting Urban Dictionary definition for ' + term)
   
   data = fetchJson(term)
   try:
      definition = data['list'][0]['definition']
      example = data['list'][0]['example']
   except IndexError:
      return phenny.say('Definition not found for ' + term)
   
   # Remove square brackets (which indicate links) from definition and example
   definition = format(definition)
   if example is not None:
      example = format(example)
   
   logging.debug('Definition returned for ' + term + ': ' + definition)
   if example is not None:
      logging.debug('    Example: ' + example)
   else:
      logging.debug('    Example not found')

   phenny.say(term + ': ' + definition)
   if example is not None and example != "":
      phenny.say('Example: ' + example)
ud.commands = ['ud']
ud.priority = 'high'
