#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''TCFParty: Unofficial Translation Party API
'''
from goslate import Goslate
gs = Goslate()

def tcfparty(en1):
	en2 = None
	en0 = None
	count = 0
	for x in range(0, 32):
		count += 1
		en1 = limitLen(en1, 1600)
		ja = gs.translate(en1, 'ja', 'en')
		ja = limitLen(ja, 1600)
		en2 = gs.translate(ja, 'en', 'ja')
		if en1 == en2:
			break
		if en2 == en0:
			break
		en0 = en1
		en1 = en2
	return en2

def limitLen(tring, limit):
	if len(tring) > limit:
		tring = tring[0:limit]
		tring.rsplit(' ',1)[0]
	return tring
