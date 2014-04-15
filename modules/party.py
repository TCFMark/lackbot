"""
party.py - Implements tcfparty.py
"""
#Rule disabled while goslate is buggered

import sys, tcfparty

def party(phenny, input):
	phenny.say(input.nick + ": " + tcfparty.tcfparty(input.group(2)))
#party.rule = r'(lackbot:)\s+(.*)'
party.commands = ['party']
