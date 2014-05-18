"""
peech.py - Phenny 'tupid 'peech Correction Module
"""

import re, sys, logging

def correct(phenny, input):
   matches = re.findall(r'(?:^|\s)s+[hz]?((?=(?=c[^i^e])|[bdfgjklmnpqrtvx]).*?)(?=$|\s)', input.group(), re.IGNORECASE)
   for match in matches:
      if (not "phinxchild" in match) and (input.nick != "prcjac"):
         logging.debug(input.nick + ' said s' + match + ' when they obviously meant \'' + match)
         phenny.reply("'" + match)
correct.rule = r'.*?(^|\s)[Ss]+[HZhz]?[bcdfgjklmnpqrtvxBCDFGJKLMNPQRTVWX].*'

