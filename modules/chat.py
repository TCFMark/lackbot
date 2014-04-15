'''
chat.py - handle incoming $nick: requests sensibly
'''

import sys, random
import translate, vincent

def chat(phenny, input):
   phrase = input.group(1).strip()
   selector = random.randint(1,4)
   if selector == 1:
      phenny.reply(vincent.question(phrase))
   else:
      phenny.reply(translate.mangle(phrase))
chat.rule = r'$nickname:\s+(.*)'

