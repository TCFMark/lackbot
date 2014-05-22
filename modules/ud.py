'''
ud.py - phenny urban dictionary definitions module
'''

import logging, json, urllib2

# Useful example: http://api.urbandictionary.com/v0/define?term=rungient

def fetchJson(term):
   opener = urllib2.build_opener()
   logging.debug('Fetching from http://api.urbandictionary.com/v0/define?term=' + term)
   result = opener.open('http://api.urbandictionary.com/v0/define?term=' + term)
   data = json.load(result)
   return data

def removeSquareBrackets(tring):
   while(('[' or ']') in tring):
      tring = tring.replace('[', '')
      tring = tring.replace(']', '')
   return tring

def ud(phenny, input):
   term = input.group(2)
   if not term:
      phenny.say('No term specified')
      quit()
   
   logging.debug('Getting Urban Dictionary definition for ' + term)
   
   data = fetchJson(term)
   definition = data['list'][0]['definition']
   example = data['list'][0]['example']
   
   # Remove square brackets (which indicate links) from definition and example
   definition = removeSquareBrackets(definition)
   example = removeSquareBrackets(example)
   
   logging.debug('Definition returned for ' + term + ': ' + definition)
   logging.debug('    Example: ' + example)
   phenny.say(term + ': ' + definition)
   phenny.say('Example: ' + example)
ud.commands = ['ud']
ud.priority = 'high'
