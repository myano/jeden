"""
uno.py - Computer Playing Bot
"""

import random

class Uno_Game:
    def __init__ (self):
        self.allowed_to_play = False
        self.game_on = False
        self.current_cards = { }
        self.player_list = [ ]


uno = Uno_Game()

def game_start(jenny, input):
    if input.nick == 'phenny_uno' and uno.game_on == False and uno.allowed_to_play == False:
        uno.game_on = True
game_start.rule = r'IRC-UNO started by.*'

def permission_to_play(jenny, input):
    uno.allowed_to_play = True
permission_to_play.rule = r'(?ims)^(jenny|$nickname)\:\splay'

def get_cards(jenny,input):
    jenny.say(str(input.group()))
get_cards.rule = r'Cards\:'
