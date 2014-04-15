#!/usr/bin/env python
# coding=utf-8
"""
translate.py - Phenny Translation Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

logdir = "/home/mark/irclogs/lackbot/translate/"

import re, urllib
import web
import random

def translate(text, input='auto', output='en'): 
   raw = False
   if output.endswith('-raw'): 
      output = output[:-4]
      raw = True

   import urllib2, json
   opener = urllib2.build_opener()
   opener.addheaders = [(
      'User-Agent', 'Mozilla/5.0' + 
      '(X11; U; Linux i686)' + 
      'Gecko/20071127 Firefox/2.0.0.11'
   )]

   input, output = urllib.quote(input), urllib.quote(output)
   text = urllib.quote(text)

   result = opener.open('http://translate.google.com/translate_a/t?' +
      ('client=t&hl=en&sl=%s&tl=%s&multires=1' % (input, output)) + 
      ('&otf=1&ssel=0&tsel=0&uptl=en&sc=1&text=%s' % text)).read()

   while ',,' in result: 
      result = result.replace(',,', ',null,')
   data = json.loads(result)

   if raw: 
      return str(data), 'en-raw'

   try: language = data[2] # -2][0][0]
   except: language = '?'

   return ''.join(x[0] for x in data[0]), language

def tr(phenny, context): 
   """Translates a phrase, with an optional language hint."""
   input, output, phrase = context.groups()

   phrase = phrase.encode('utf-8')

   if (len(phrase) > 350) and (not context.admin): 
      return phenny.reply('Phrase must be under 350 characters.')

   input = input or 'auto'
   input = input.encode('utf-8')
   output = (output or 'en').encode('utf-8')

   if input != output: 
      msg, input = translate(phrase, input, output)
      if isinstance(msg, str): 
         msg = msg.decode('utf-8')
      if msg: 
         msg = web.decode(msg) # msg.replace('&#39;', "'")
         msg = '"%s" (%s to %s, translate.google.com)' % (msg, input, output)
      else: msg = 'The %s to %s translation failed, sorry!' % (input, output)

      phenny.reply(msg)
   else: phenny.reply('Language guessing failed, so try suggesting one!')

tr.rule = ('$nick', ur'(?:([a-z]{2}) +)?(?:([a-z]{2}|en-raw) +)?["“](.+?)["”]\? *$')
tr.example = '$nickname: "mon chien"? or $nickname: fr "mon chien"?'
tr.priority = 'low'

def tr2(phenny, input): 
   """Translates a phrase, with an optional language hint."""
   command = input.group(2)
   if not command:
      return phenny.reply("Need something to translate!")
   command = command.encode('utf-8')

   def langcode(p): 
      return p.startswith(':') and (2 < len(p) < 10) and p[1:].isalpha()

   args = ['auto', 'en']

   for i in xrange(2): 
      if not ' ' in command: break
      prefix, cmd = command.split(' ', 1)
      if langcode(prefix): 
         args[i] = prefix[1:]
         command = cmd
   phrase = command

   # if (len(phrase) > 350) and (not input.admin): 
   #    return phenny.reply('Phrase must be under 350 characters.')

   src, dest = args
   if src != dest: 
      msg, src = translate(phrase, src, dest)
      if isinstance(msg, str): 
         msg = msg.decode('utf-8')
      if msg: 
         msg = web.decode(msg) # msg.replace('&#39;', "'")
         if len(msg) > 450: msg = msg[:450] + '[...]'
         msg = '"%s" (%s to %s, translate.google.com)' % (msg, src, dest)
      else: msg = 'The %s to %s translation failed, sorry!' % (src, dest)

      phenny.reply(msg)
   else: phenny.reply('Language guessing failed, so try suggesting one!')

tr2.commands = ['tr']
tr2.priority = 'low'

def mangle(tring): 
   import time
   loglist = []
   
   phrase = tring.encode('utf-8')
   loglist.append(phrase)
   languages = ['zh-CN', 'fi', 'hu', 'ru', 'ja', 'zh-TW', 'ko', 'ar', 'iw', 'hi', 'ur']
   random.shuffle(languages)
   for i in range(0, 6): 
      backup = phrase[:]
      try:
         phrase, _lang = translate(phrase, 'en', languages[i])
      except ValueError:
         break
      phrase = phrase.encode("utf-8")
      loglist.append(phrase + " (en -> " + languages[i] + ")")

      if not phrase: 
         phrase = backup[:]
         break
      time.sleep(0.25)

      backup = phrase[:]
      try:
         phrase, _lang = translate(phrase, languages[i], 'en')
      except ValueError:
         break
      phrase = phrase.encode("utf-8")
      loglist.append(phrase + " (" + languages[i] + " -> en)")

      if not phrase: 
         phrase = backup[:]
         break
      time.sleep(0.25)

   logfile = open(logdir + "mangle-" + time.strftime("%Y%m%d") + ".txt", "a+")
   for line in loglist:
      logfile.write(line + "\n")
   logfile.write("--------\n")
   logfile.close()

   phrase = phrase.replace(' ,', ',').replace(' .', '.')
   phrase = phrase.strip(' ,')
   return phrase
#mangle.commands = ['mangle']
#mangle.rule = r'(lackbot:)\s+(.*)'

if __name__ == '__main__': 
   print __doc__.strip()
