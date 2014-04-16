#!/usr/bin/env python
"""
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random

def hello(phenny, input): 
   greeting = random.choice(('Hi', 'Hey', 'Hello'))
   punctuation = random.choice(('', '!', ' :)', ' <3'))
   phenny.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey) $nickname[ \t]*$'

def interjection(phenny, input): 
   phenny.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

def idiot(phenny, input):
   phenny.say(':(')
idiot.rule = r'$nickname: idiot'

def thanks(phenny, input):
   phenny.say(input.nick + ': welcome!')
thanks.rule = r'thanks(,)? $nickname[ \t]*$'

def wtf(phenny, input):
   phenny.reply("right!?")
wtf.rule = r'(?i)wtf.*'

def wow(phenny, input):
   phenny.say(random.choice(["so ", "such "]) + phenny.nick)
   phenny.say(random.choice(["many ", "how "]) + input.nick)
   phenny.say(random.choice(["much ", "very "]) + input.sender)
wow.rule = r'(?i)wow$'

def nsfw(phenny, input):
   phenny.say("it totally is safe for work")
nsfw.rule = r'(?i).*?nsfw.*'

def rediculous(phenny, input):
   phenny.reply("R-I-D... ridiculous")
rediculous.rule = r'(?i).*?rediculous.*'

def lol(phenny, input):
   phenny.say(makelaugh())
lol.rule = r'(?i)lol.*'

def haha(phenny, input):
   phenny.say(makelaugh())
haha.rule = r'(?i)hah.*'

def makelaugh():
   laugh = random.choice([makelol(), makehaha()])
   if random.choice([True, False]):
      return laugh.upper()
   else:
      return laugh

def makelol():
   somelols = 'l'
   for i in range(0, random.randint(1,8)):
      somelols = somelols + 'ol'
   return somelols

def makehaha():
   hahaha = ''
   for i in range(0, random.randint(1,8)):
      hahaha = hahaha + 'ha'
   return hahaha

def work(phenny, input):
   phenny.reply('BZZZZZZZT')
work.rule = r'(?i).*?(cfl|corefiling|(\s|^)wiki(\s|$)|(\s|^)(s|\')tory(\s|$)|seahorse|donkey|romp|tnfc|tnwsp|magnify|spidermonkey|smmf|plega|djb|xiif|xbrl|(\s|^)sys(\s|$)|synerg).*'

if __name__ == '__main__': 
   print __doc__.strip()
