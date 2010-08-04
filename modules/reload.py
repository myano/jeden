#!/usr/bin/env python
"""
reload.py - jenny Module Reloader Module
Copyright 2008, Sean B. Palmer, inamidst.com
Licensed under the Eiffel Forum License 2.

http://inamidst.com/phenny/
"""

import irc

def f_reload(jenny, input): 
    """Reloads a module, for use by admins only.""" 
    if not input.admin: return

    name = input.group(2)
    if name == jenny.config.owner: 
        return jenny.reply('What?')

    if (not name) or (name == '*'): 
        jenny.setup()
        return jenny.reply('done')

    try: module = getattr(__import__('modules.' + name), name)
    except ImportError: 
        module = getattr(__import__('opt.' + name), name)
    reload(module)
    if hasattr(module, 'setup'): 
        module.setup(jenny)

    if hasattr(module, '__file__'): 
        import os.path, time
        mtime = os.path.getmtime(module.__file__)
        modified = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(mtime))
    else: modified = 'unknown'

    jenny.register(vars(module))
    jenny.bind_commands()

    jenny.reply('%r (version: %s)' % (module, modified))
f_reload.name = 'reload'
f_reload.rule = ('$nick', ['reload'], r'(\S+)?')
f_reload.priority = 'low'

if __name__ == '__main__': 
    print __doc__.strip()
