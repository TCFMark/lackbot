'''
chat.py - handle incoming $nick: requests sensibly
'''

import sys, random

def chat(phenny, input):
   phrase = input.group(1).strip()
   selector = random.randint(1,5)
   if selector <= 1:
      import vincent
      phenny.reply(vincent.question(phrase))
   elif selector <= 2:
      import lbtwitter
      phenny.reply(lbtwitter.mangleRandomTweet())
   else:
      import tcfparty
      phenny.reply(tcfparty.tcfparty(phrase))
chat.rule = r'$nickname:\s+(.*)'

