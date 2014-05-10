"""
quip.py - Phenny patel pyquips module
"""

import sys, pyquips, cgi, os

def quip(phenny, input):
   logging.debug('Adding quip: ' + input.group(2))
   pyquips.run(input.group(2) + "\n")
   phenny.reply("Quip added! Check it out at http://tcfmark.dnsd.info/quips/")
quip.commands = ['quip']

