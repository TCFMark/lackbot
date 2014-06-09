#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''TCFParty: Unofficial Translation Party API
'''

import translate, logging, re

def tcfparty(en1):
	en2 = None
	en0 = None
	en1 = en1.encode('utf-8')
	input = en1
	
	logging.debug('Starting a TCFParty!')
	
	# Extract URLs from phrase
	urls = re.findall(r'.*?(http[s]?://[^<> "\x01]+)[,.]?', en1)
	if urls:
		logging.debug('URLs found in party phrase: ')
		for url in urls:
			logging.debug('    ' + url)
			en1 = en1.replace(url, '', 1)

	for x in range(0, 20):
		# Translate to Japanese
		en1 = limitLen(en1, 400)
		try:
			logging.debug('    auto to ja: ' + en1)
			ja, _lang = translate.translate(en1, 'auto', 'ja')
		except ValueError:
			logging.debug('ValueError means the party\'s over.')
			break
		ja = ja.encode('utf-8')

		# Translate back to English
		ja = limitLen(ja, 400)
		try:
			logging.debug('    ja to en: ' + ja)
			en2, _lang = translate.translate(ja, 'ja', 'en')
		except ValueError:
			logging.debug('ValueError means the party\'s over.')
			break
		en2 = en2.encode('utf-8')

		# Stops returning nonsense if the encoding falls over (see issue #29)
		if ('ã' in en2) or ('â' in en2):
			logging.debug('Encoding nonsense encountered, ending party.')
			en2 = en1
			break

		if en1 == en2:
			break
		if en2 == en0:
			break
		en0 = en1
		en1 = en2

	if en2 is not None:
		en2 = en2.replace(' ,', ',')
		en2 = en2.replace(' .', '.')
	else:
		logging.debug('Returned empty; returning input.')
		return input

	# Plonk URLs back on the end of the string
	if urls:
		en2 = en2 + ' -'
		for url in urls:
			en2 = en2 + ' ' + url

	logging.debug('Party over; returning: ' + en2)
	return en2

def party(phenny, input):
	"""Runs a phrase through TCFParty, lackbot's unofficial Translation Party feature"""
	phrase = input.group(2)
	if not phrase:
		phenny.say('Please enter a phrase.')
		return
	
	logging.debug('.party called')
	phrase = tcfparty(phrase)
	phenny.reply(phrase)
party.commands = ['party']
party.example = '.party Do a dance for me, lackbot'

def limitLen(tring, limit):
	if len(tring) > limit:
		tring = tring[0:limit]
		tring.rsplit(' ',1)[0]
	return tring
