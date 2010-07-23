"""
uno.py - Computer Playing Bot
"""

import random

class uno:
    def __init__ (self):
        self.game_on = False
        self.current_cards = { }

def game_start(jenny, input):
    if input.nick == 'phenny_osu' and uno.game_uno == False:
        jenny.say("I can see the game started.")
game_start.rule = r'.*\x0300,01IRC-UNO started by.*'
