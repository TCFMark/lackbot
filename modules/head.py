#!/usr/bin/env python
"""
head.py - Phenny HTTP Metadata Utilities
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import re, urllib, urllib2, httplib, urlparse, time, logging
from htmlentitydefs import name2codepoint
import web
from tools import deprecated

def head(phenny, input): 
   """Provide HTTP HEAD information."""
   uri = input.group(2)
   uri = (uri or '').encode('utf-8')
   if ' ' in uri: 
      uri, header = uri.rsplit(' ', 1)
   else: uri, header = uri, None

   if not uri and hasattr(phenny, 'last_seen_uri'): 
      try: uri = phenny.last_seen_uri[input.sender]
      except KeyError: return phenny.say('?')

   if not uri.startswith('htt'): 
      uri = 'http://' + uri
   # uri = uri.replace('#!', '?_escaped_fragment_=')
   
   logging.debug('Getting header information for ' + uri)

   try: info = web.head(uri)
   except IOError: return phenny.say("Can't connect to %s" % uri)
   except httplib.InvalidURL: return phenny.say("Not a valid URI, sorry.")

   if not isinstance(info, list): 
      try: info = dict(info)
      except TypeError: 
         return phenny.reply('Try .head http://example.org/ [optional header]')
      info['Status'] = '200'
   else: 
      newInfo = dict(info[0])
      newInfo['Status'] = str(info[1])
      info = newInfo

   if header is None: 
      data = []
      if info.has_key('Status'): 
         data.append(info['Status'])
      if info.has_key('content-type'): 
         data.append(info['content-type'].replace('; charset=', ', '))
      if info.has_key('last-modified'): 
         modified = info['last-modified']
         modified = time.strptime(modified, '%a, %d %b %Y %H:%M:%S %Z')
         data.append(time.strftime('%Y-%m-%d %H:%M:%S UTC', modified))
      if info.has_key('content-length'): 
         data.append(info['content-length'] + ' bytes')
      phenny.reply(', '.join(data))
   else: 
      headerlower = header.lower()
      if info.has_key(headerlower): 
         phenny.say(header + ': ' + info.get(headerlower))
      else: 
         msg = 'There was no %s header in the response.' % header
         phenny.say(msg)
head.commands = ['head']
head.example = '.head http://www.w3.org/'

r_title = re.compile(r'(?ims)<title[^>]*>(.*?)</title\s*>')
r_entity = re.compile(r'&[A-Za-z0-9#]+;')

def f_title(uri): 
   if not ':' in uri: 
      uri = 'http://' + uri
   uri = uri.replace('#!', '?_escaped_fragment_=')
   
   logging.debug('Getting title for ' + uri)

   localhost = [
      'http://localhost/', 'http://localhost:80/', 
      'http://localhost:8080/', 'http://127.0.0.1/', 
      'http://127.0.0.1:80/', 'http://127.0.0.1:8080/', 
      'https://localhost/', 'https://localhost:80/', 
      'https://localhost:8080/', 'https://127.0.0.1/', 
      'https://127.0.0.1:80/', 'https://127.0.0.1:8080/', 
   ]
   for s in localhost: 
      if uri.startswith(s): 
         return 'Sorry, access forbidden.'

   try: 
      redirects = 0
      while True: 
         headers = {
            'Accept': 'text/html', 
            'User-Agent': 'Mozilla/5.0 (Phenny)'
         }
         req = urllib2.Request(uri, headers=headers)
         u = urllib2.urlopen(req)
         info = u.info()
         u.close()
         # info = web.head(uri)

         if not isinstance(info, list): 
            status = '200'
         else: 
            status = str(info[1])
            info = info[0]
         if status.startswith('3'): 
            uri = urlparse.urljoin(uri, info['Location'])
         else: break

         redirects += 1
         if redirects >= 25: 
            return "Too many redirects"

      try: mtype = info['content-type']
      except: 
         err = ": Couldn't get the Content-Type, sorry"
         return err
      if not (('/html' in mtype) or ('/xhtml' in mtype)): 
         return "Document isn't HTML"

      u = urllib2.urlopen(req)
      bytes = u.read(262144)
      u.close()

   except IOError: 
      return "Can't connect to %s" % uri

   m = r_title.search(bytes)
   if m: 
      title = m.group(1)
      title = title.strip()
      title = title.replace('\t', ' ')
      title = title.replace('\r', ' ')
      title = title.replace('\n', ' ')
      while '  ' in title: 
         title = title.replace('  ', ' ')
      if len(title) > 200: 
         title = title[:200] + '[...]'
      
      def e(m): 
         entity = m.group(0)
         if entity.startswith('&#x'): 
            cp = int(entity[3:-1], 16)
            return unichr(cp).encode('utf-8')
         elif entity.startswith('&#'): 
            cp = int(entity[2:-1])
            return unichr(cp).encode('utf-8')
         else: 
            char = name2codepoint[entity[1:-1]]
            return unichr(char).encode('utf-8')
      title = r_entity.sub(e, title)

      if title: 
         try: title.decode('utf-8')
         except: 
            try: title = title.decode('iso-8859-1').encode('utf-8')
            except: title = title.decode('cp1252').encode('utf-8')
         else: pass
      else: title = '[The title is empty.]'

      title = title.replace('\n', '')
      title = title.replace('\r', '')
      return title
   else:
      return 'No title found'

def title(phenny, input):
   """.title <URI> - Return the title of URI."""
   uri = input.group(2)
   uri = (uri or '').encode('utf-8')

   if not uri and hasattr(phenny.bot, 'last_seen_uri'): 
      uri = phenny.bot.last_seen_uri.get(input.nick)
   if not uri: 
      phenny.reply('I need a URI to give the title of...')
   
   phenny.reply(f_title(uri))
title.commands = ['title']

def noteuri(phenny, input): 
   # Don't duplicate when .title is used
   if '.title' in input.group(0):
      return
   
   uri = input.group(1).encode('utf-8')
   logging.debug('Found URI: ' + uri)
   if not hasattr(phenny.bot, 'last_seen_uri'): 
      phenny.bot.last_seen_uri = {}
   phenny.bot.last_seen_uri[input.sender] = uri
   
   # Print title anyway
   phenny.reply(f_title(uri))
noteuri.rule = r'.*(http[s]?://[^<> "\x01]+)[,.]?'

if __name__ == '__main__': 
   print __doc__.strip()
