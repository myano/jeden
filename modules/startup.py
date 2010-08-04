#!/usr/bin/env python
"""
startup.py - jenny Startup Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

def startup(jenny, input): 
	if hasattr(jenny.config, 'serverpass'): 
		jenny.write(('PASS', jenny.config.serverpass))

	if hasattr(jenny.config, 'password'): 
		jenny.msg('NickServ', 'IDENTIFY %s' % jenny.config.password)
		__import__('time').sleep(5)

	# Cf. http://swhack.com/logs/2005-12-05#T19-32-36
	for channel in jenny.channels: 
		jenny.write(('JOIN', channel))
startup.rule = r'(.*)'
startup.event = '251'
startup.priority = 'low'

if __name__ == '__main__': 
	print __doc__.strip()
