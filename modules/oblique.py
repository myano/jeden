#!/usr/bin/env python
"""
oblique.py - Web Services Interface
Copyright 2008-9, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/jenny/
"""

import re, urllib
import web

definitions = 'http://github.com/nslater/oblique/wiki'

r_item = re.compile(r'(?i)<li>(.*?)</li>')
r_tag = re.compile(r'<[^>]+>')

def mappings(uri): 
   result = {}
   bytes = web.get(uri)
   for item in r_item.findall(bytes): 
      item = r_tag.sub('', item).strip(' \t\r\n')
      if not ' ' in item: continue

      command, template = item.split(' ', 1)
      if not command.isalnum(): continue
      if not template.startswith('http://'): continue
      result[command] = template.replace('&amp;', '&')
   return result

def service(jenny, input, command, args): 
   t = o.services[command]
   template = t.replace('${args}', urllib.quote(args.encode('utf-8')))
   template = template.replace('${nick}', urllib.quote(input.nick))
   uri = template.replace('${sender}', urllib.quote(input.sender))

   bytes = web.get(uri)
   lines = bytes.splitlines()
   if not lines: 
      return jenny.reply('Sorry, the service is broken.')
   jenny.say(lines[0][:350])

def o(jenny, input): 
   """Call a webservice."""
   text = input.group(2)
   if hasattr(jenny.config, 'services'): 
      services = jenny.config.services
   else: services = definitions

   if (not o.services) or (text == 'refresh'): 
      old = o.services
      o.services = mappings(services)
      if text == 'refresh': 
         msg = 'Okay, found %s services.' % len(o.services)
         added = set(o.services) - set(old)
         if added: 
            msg += ' Added: ' + ', '.join(sorted(added)[:5])
            if len(added) > 5: msg += ', &c.'
         return jenny.reply(msg)

   if not text: 
      return jenny.reply('Try %s for details.' % services)

   if ' ' in text: 
      command, args = text.split(' ', 1)
   else: command, args = text, ''
   command = command.lower()

   if command == 'service': 
      msg = o.services.get(args, 'No such service!')
      return jenny.reply(msg)

   if not o.services.has_key(command): 
      return jenny.reply('Sorry, no such service. See %s' % services)

   if hasattr(jenny.config, 'external'): 
      default = jenny.config.external.get('*')
      manifest = jenny.config.external.get(input.sender, default)
      if manifest: 
         commands = set(manifest)
         if (command not in commands) and (manifest[0] != '!'): 
            return jenny.reply('Sorry, %s is not whitelisted' % command)
         elif (command in commands) and (manifest[0] == '!'): 
            return jenny.reply('Sorry, %s is blacklisted' % command)
   service(jenny, input, command, args)
o.commands = ['o']
o.example = '.o servicename arg1 arg2 arg3'
o.services = {}

def py(jenny, input): 
   service(jenny, input, 'py', input.group(2))
py.commands = ['py']

if __name__ == '__main__': 
   print __doc__.strip()
