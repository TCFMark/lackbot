'''
vincent.py - what's vincent.py?
'''

import string, re

def question(tring):
   regex = re.compile('[%s]' % re.escape(string.punctuation))
   tring = regex.sub('', tring)
   word = max(tring.split(), key=len)
   return "What\'s " + word + "?"

