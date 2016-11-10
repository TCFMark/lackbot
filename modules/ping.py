#!/usr/bin/env python
"""
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/phenny/
"""

import random, logging

# getWordList is based on
# https://mail.python.org/pipermail/tutor/2001-June/006301.html
def getWordList(minwords):
   import string, os
   wordfile = '/home/local/msh/.phenny/words'
   stat = os.stat(wordfile)
   # the filesize is the 7th element of the array
   flen = stat[6]
   f = open(wordfile)
   words = []

   while len(words) < minwords:
      # seek to a random offset in the file
      f.seek(int(random.random() * flen))
      # do a single read with sufficient characters
      chars = f.read(minwords * 30)
      # split it on white space
      words = string.split(chars)
      
   logging.debug('Random words required, returning ' + str(words))   
   return words

def hello(phenny, input): 
   logging.debug('Saying hello to ' + input.nick)
   greeting = random.choice(('Hi', 'Hey', 'Hello'))
   punctuation = random.choice(('', '!', ' :)', ' <3'))
   phenny.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey) $nickname[ \t]*$'

def interjection(phenny, input): 
   logging.debug('Yelling back at ' + input.nick)
   phenny.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

def idiot(phenny, input):
   logging.debug(input.nick + ' called me an idiot :(')
   phenny.say(':(')
idiot.rule = r'$nickname: idiot'

def thanks(phenny, input):
   logging.debug(input.nick + ' said thanks!')
   phenny.say(input.nick + ': welcome!')
thanks.rule = r'thanks(,)? $nickname[ \t]*$'

def wtf(phenny, input):
   logging.debug('WTF indeed, ' + input.nick)
   phenny.reply("right!?")
wtf.rule = r'(?i)wtf.*'

def wow(phenny, input):
   logging.debug('Wow, so ' + input.nick + '. Activating doge mode')
   try:         
      phenny.say(random.choice(["so ", "such "]) + getWordList(1)[1])
      phenny.say(random.choice(["many ", "how "]) + getWordList(1)[1])
      phenny.say(random.choice(["much ", "very "]) + random.choice([phenny.nick, input.nick, input.sender]))
   except OSError:
      phenny.say(random.choice(["so ", "such "]) + phenny.nick)
      phenny.say(random.choice(["many ", "how "]) + input.nick)
      phenny.say(random.choice(["much ", "very "]) + input.sender)
wow.rule = r'(?i)wow.*'

def nsfw(phenny, input):
   logging.debug('Assuring SFWness to ' + input.nick)
   phenny.say("it totally is safe for work")
nsfw.rule = r'(?i).*?nsfw.*'

def rediculous(phenny, input):
   logging.debug(input.nick + ' said rediculous :(')
   phenny.reply("*ridiculous")
rediculous.rule = r'(?i).*?rediculous.*'

def lol(phenny, input):
   logging.debug('Laughter detected! LOL!')
   phenny.say(makelaugh())
lol.rule = r'(?i)lol.*'

def haha(phenny, input):
   logging.debug('Laughter detected! HAHA!')
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

#def work(phenny, input):
#   logging.debug('Work horn going off')
#   phenny.reply('HONK')
#work.rule = r'(?i).*?(cfl|corefiling|(\s|^)wiki(\s|$)|seahorse|donkey|romp|tnfc|tnwsp|magnify|spidermonkey|smmf|plega|djb|xiif|xbrl|(\s|^)sys(\s|$)|synerg).*'

def gross(phenny, input):
   logging.debug('Gross')
   response = random.choice(['icky', 'yuck', 'gross', 'filfy', 'beastly', 'hurk!', 'how horrid', 'blech!', 'narstee', 'grim', 'net'])
   phenny.say(response)
gross.rule = r'(?i).*?gross.*'

def food(phenny, input):
   logging.debug('I LIKE FOOD')
   reply = random.choice(['I LIKE FOOD',
       'Food is my friend',
       'I eat things!',
       'Where\'s the nearest dinner?',
       'Cake pls',
       'I eat wit my robot mouth',
       'Sometimes I let other people eat the things I own',
       'wow, so food, how eating',
       'A fruit a day makes the dentist go away',
       'Please stop saying that word'
       'If you can\'t feed a hundred people, just feed me',
       'msh made me and even he says I\'m annoying',
       'I\'m not allowed outside because I eat mud',
       'Drinking is for idiots',
       'EATING',
       'Cheese, smile!',
       'Is it lunch time yet?',
       'Lunch time!',
       'for food in foods: food(eat)',
       'Eggscuse me, could you tell me a yolk?',
       'Foo... ahhhhhh you nearly got me! I\'m not saying anything this time!',
       'Foodball? What is this foodball you guys keep talking about?',
       'My favourite sandwich filling is CoreFilling',
       "hunterschicken2",
       "Good CoreFilers never book holidays on pizza meeting days!",
       "I'll have me one CoreFillet burger please",
       "I don't have a tongue so none of my opinions are valid",
       "It must be terrible being the last banana in a bunch, seeing your friends stripped and eaten one by one, your own health worsening daily",
       "Man walks into a breakfast bar and gets porridge on his shoes",
       "Surely horsemeat sandals would just disintegrate?",
       "Crisps are just savoury breakfast cereal",
       "Many hands spoil the broth",
       "Food with a face tastes delicious",
       input.nick + " might be vegetarian, might be meatetarian. I'm a humanitarian",
       "Special fried rice for special people, like " + input.nick,
       "The Royal Fusilliers are in charge of the Queen's pasta #QueenFacts",
       "the pig walked into the shop and the lady said we dont make types of meat in this shop"])
   phenny.say(reply)
food.rule = r'(?i).+food.*'

#def smilyface(phenny, input):
#   if random.randint(1,3) is 1:
#      logging.debug('Smily face!')
#      response = ('8' + (random.randint(1,10) * '=') + 'D')
#      if random.randint(1,3) is 1:
#         response = response + (random.randint(1,6) * '~')
#      phenny.reply(response)
#smilyface.rule = r'(?i).*?(\:\)|\:D|\:-\)|\:-D|;\)|;-\)).*'

if __name__ == '__main__': 
   print __doc__.strip()


