#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''TCFParty: Unofficial Translation Party API
'''

import translate, logging

def tcfparty(en1):
	en2 = None
	en0 = None
	en1 = en1.encode('utf-8')
	input = en1
	
	logging.debug(__name__ + ': Starting a TCFParty!')

	for x in range(0, 32):
		# Translate to Japanese
		en1 = limitLen(en1, 400)
		try:
			logging.debug(__name__ + ': en to ja: ' + en1)
			ja, _lang = translate.translate(en1, 'en', 'ja')
		except ValueError:
			logging.debug(__name__ + ': ValueError means the party\'s over.')
			break
		ja = ja.encode('utf-8')

		# Translate back to English
		ja = limitLen(ja, 400)
		try:
			logging.debug(__name__ + ': ja to en: ' + ja)
			en2, _lang = translate.translate(ja, 'ja', 'en')
		except ValueError:
			logging.debug(__name__ + ': ValueError means the party\'s over.')
			break
		en2 = en2.encode('utf-8')

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
		logging.debug(__name__ + ': Returned empty; returning input.')
		return input

	logging.debug(__name__ + ': Party over; returning: ' + en2)
	return en2

def limitLen(tring, limit):
	if len(tring) > limit:
		tring = tring[0:limit]
		tring.rsplit(' ',1)[0]
	return tring
