from modules import unobot

bot = unobot.unobot ()
STRINGS = unobot.STRINGS

class unogame:
    def __init__ (self):
        self.allowed_to_play = False

    def make_a_move (self):
        self.my_cards = unobot.STRINGS['YOUR_CARDS'] % bot.renderCards (bot.players[jenny.config.nick])

