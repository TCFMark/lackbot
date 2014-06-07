#!/usr/bin/env python
# coding=utf-8
"""
calc.py - Phenny Calculator Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, logging
import web, HTMLParser

r_result = re.compile(r'(?i)<A NAME=results>(.*?)</A>')
r_tag = re.compile(r'<\S+.*?>')

subs = [
   (' in ', ' -> '), 
   (' over ', ' / '), 
   (u'£', 'GBP '), 
   (u'€', 'EUR '), 
   ('\$', 'USD '), 
   (r'\bKB\b', 'kilobytes'), 
   (r'\bMB\b', 'megabytes'), 
   (r'\bGB\b', 'kilobytes'), 
   ('kbps', '(kilobits / second)'), 
   ('mbps', '(megabits / second)')
]

def calc(phenny, input): 
   """Use the Frink online calculator."""   
   q = input.group(2)
   if not q:
      return phenny.say('0?')
   
   logging.debug('Using Frink calculator (.calc) to calculate ' + input.group(2))

   query = q[:]
   for a, b in subs: 
      query = re.sub(a, b, query)
   query = query.rstrip(' \t')

   precision = 5
   if query[-3:] in ('GBP', 'USD', 'EUR', 'NOK'): 
      precision = 2
   query = web.urllib.quote(query.encode('utf-8'))

   uri = 'http://futureboy.us/fsp/frink.fsp?fromVal='
   bytes = web.get(uri + query)
   m = r_result.search(bytes)
   if m: 
      result = m.group(1)
      result = r_tag.sub('', result) # strip span.warning tags
      result = result.replace('&gt;', '>')
      result = result.replace('(undefined symbol)', '(?) ')

      if '.' in result: 
         try: result = str(round(float(result), precision))
         except ValueError: pass

      if not result.strip(): 
         result = '?'
      elif ' in ' in q: 
         result += ' ' + q.split(' in ', 1)[1]

      logging.debug('.calc returned ' + result[:350])
      phenny.say(q + ' = ' + result[:350])
   else:
      logging.debug('.calc failed') 
      phenny.reply("Sorry, can't calculate that.")
calc.commands = ['calc', 'c']
calc.example = '.calc 5 + 3'

def py(phenny, input): 
   """Uses Oblique's python service to run a python command"""
   query = input.group(2).encode('utf-8')
   logging.debug('Using Python service (.py) to run: ' + query)
   uri = 'http://tumbolia.appspot.com/py/'
   answer = web.get(uri + web.urllib.quote(query))
   if answer: 
      logging.debug('.py returned ' + answer)
      phenny.say(answer)
   else:
      logging.debug('.py returned no result') 
      phenny.reply('Sorry, no result.')
py.commands = ['py']
py.example('.py import random; print random.choice(["yes", "no"])')

def wa(phenny, input): 
   """Searches Wolfram Alpha"""
   if not input.group(2):
      return phenny.reply("No search term.")
   query = input.group(2).encode('utf-8')
   logging.debug('Using Wolfram Alpha (.wa) to run: ' + query)
   uri = 'http://tumbolia.appspot.com/wa/'
   answer = web.get(uri + web.urllib.quote(query.replace('+', '%2B')))
   if answer: 
      answer = HTMLParser.HTMLParser().unescape(answer)
      answer = answer.replace('->', ': ')
      answer = answer.replace(';', ' | ')
      logging.debug('.wa returned ' + answer)
      phenny.say(answer)
   else: 
      logging.debug('.wa returned no result') 
      phenny.reply('Sorry, no result.')
wa.commands = ['wa']
wa.example = ['.wa weather London UK']

if __name__ == '__main__': 
   print __doc__.strip()
