class unogame:
    def __init__ (self):
        self.allowed_to_play = False

    def make_a_move (self):
        self.my_cards = STRINGS['YOUR_CARDS'] % unobot.renderCards (unobot.players["jenny_osu"])

