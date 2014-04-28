"""
peech.py - Phenny 'tupid 'peech Correction Module
"""

import re, sys

def correct(phenny, input):
   matches = re.findall(r'(?:^|\s)s+[hz]?((?=(?=c[^i^e])|[bdfgjklmnpqrtvwx]).*?)(?=$|\s)', input.group(), re.IGNORECASE)
   for match in matches:
      if (not "phinxchild" in match) and (input.nick != "prcjac"):
            phenny.reply("'" + match)
correct.rule = r'.*?(^|\s)[Ss]+[HZhz]?[bcdfgjklmnpqrtvwxBCDFGJKLMNPQRTVWX].*'

