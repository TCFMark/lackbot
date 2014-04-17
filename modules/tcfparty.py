#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''TCFParty: Unofficial Translation Party API
'''

import translate

def tcfparty(en1):
	en2 = None
	en0 = None
	count = 0
	en1 = en1.encode('utf-8')

	for x in range(0, 32):
		count += 1

		# Translate to Japanese
		en1 = limitLen(en1, 400)
		try:
			ja, _lang = translate.translate(en1, 'en', 'ja')
		except ValueError:
			break
		ja = ja.encode('utf-8')

		# Translate back to English
		ja = limitLen(ja, 400)
		try:
			en2, _lang = translate.translate(ja, 'ja', 'en')
		except ValueError:
			break
		en2 = en2.encode('utf-8')

		if en1 == en2:
			break
		if en2 == en0:
			break
		en0 = en1
		en1 = en2

	en2 = en2.replace(' ,', ',')
	en2 = en2.replace(' .', '.')

	return en2

def limitLen(tring, limit):
	if len(tring) > limit:
		tring = tring[0:limit]
		tring.rsplit(' ',1)[0]
	return tring
