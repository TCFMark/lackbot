'''
chat.py - handle incoming $nick: requests sensibly
'''

import sys, random, logging

def chat(phenny, input):
   phrase = input.group(1).strip()
   selector = random.randint(1,6)
   logging.debug('Selector rolled a ' + str(selector))
   if selector <= 1:
      logging.debug('Doing a Vincent reply')
      import vincent
      phenny.reply(vincent.question(phrase))
   elif selector <= 2:
      logging.debug('I LIKE FOOD')
      phenny.reply("I LIKE FOOD")
   elif selector <= 3:
      logging.debug('Replying with a "fact"')
      import wikipedia
      phenny.reply(wikipedia.getFact())
   else:
      logging.debug('Replying with a party of the input')
      import tcfparty
      phenny.reply(tcfparty.tcfparty(phrase))
chat.rule = r'(?i)$nickname:\s+(.*)'

def mention(phenny, input):
   phrase = input.group(1).strip()
   selector = random.randint(1,2)
   logging.debug('lackbot mentioned, selector rolled a ' + str(selector))
   if selector <= 1:
      logging.debug('Confused reply')
      reply = random.choice(["What's that?", "Too right!", "Say whaat?!?", "Hmm?", "Pardon?"])
      phenny.reply(reply)
   elif selector <= 2:
      logging.debug('Replying with a party of the input')
      import tcfparty
      phrase = phrase.replace(phenny.nick, input.nick)
      phenny.reply(tcfparty.tcfparty(phrase))
mention.rule = r'(?i)(.*$nickname(?!:).*)'

