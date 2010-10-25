#!/usr/bin/env python
"""
ping.py - Phenny Ping Module
Author: Sean B. Palmer, inamidst.com
About: http://inamidst.com/jenny/
"""

import random

def hello(jenny, input): 
   greeting = random.choice(('Hi', 'Hey', 'Hello'))
   punctuation = random.choice(('', '!'))
   jenny.say(greeting + ' ' + input.nick + punctuation)
hello.rule = r'(?i)(hi|hello|hey) $nickname\b'

def interjection(jenny, input): 
   jenny.say(input.nick + '!')
interjection.rule = r'$nickname!'
interjection.priority = 'high'
interjection.thread = False

if __name__ == '__main__': 
   print __doc__.strip()
