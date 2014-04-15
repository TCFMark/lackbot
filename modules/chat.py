'''
chat.py - handle incoming $nick: requests sensibly
'''

import sys, random

sys.path.append('/home/mark/ircbots/phenny/modules')

import translate, vincent

def chat(phenny, input):
   phrase = input.group(2).strip()
   selector = random.randint(1,4)
   if selector == 1:
      phenny.reply(vincent.question(phrase))
   else:
      phenny.reply(translate.mangle(phrase))
chat.rule = r'(lackbot:)\s+(.*)'

