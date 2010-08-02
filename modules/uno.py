
from modules import unobot
import time

bot = unobot.unobot ()

def uno(jenny, input):
    bot.start (jenny, input.nick)
uno.commands = ['uno']
uno.priority = 'low'

def unostop(jenny, input):
    bot.stop (jenny, input)
unostop.commands = ['unostop']
unostop.priority = 'low'

def join(jenny, input):
    bot.join (jenny, input)
join.rule = '^join$'
join.priority = 'low'

def deal(jenny, input):
    bot.deal (jenny, input)
deal.commands = ['deal']
deal.priority = 'low'

def play(jenny, input):
    bot.play_part1 (jenny, input)
play.commands = ['play']
play.priority = 'low'

def draw(jenny, input):
    bot.draw (jenny, input)
draw.commands = ['draw']
draw.priority = 'low'

def passs(jenny, input):
    bot.passs (jenny, input)
passs.commands = ['pass']
passs.priority = 'low'

def unotop10 (jenny, input):
    bot.top10 (jenny)
unotop10.commands = ['unotop10']
unotop10.priority = 'low'

def show_user_cards (jenny, input):
    bot.showCards (jenny, input.nick)
show_user_cards.commands = ['cards']
show_user_cards.priority = 'low'

def jenny_join(jenny, input):
    if bot.allowed_to_play == True:
        time.sleep(2)
        jenny.say("I'm also joining the game.")
        input.nick = jenny.config.nick
        bot.join(jenny, input)
jenny_join.rule = '^.uno$'

#def take_turn(jenny, input):
#    uno_alg.make_a_move()
#    print str(uno_alg.make_a_move.my_cards)
#take_turn.rule = r'$nickname\'s\sturn.\sTop\sCard\:'

def permission_to_play(jenny, input):
    text = input.group().split(": ")
    if text[1] == 'play':
        bot.allowed_to_play = True
    elif text[1] == 'stop':
        bot.allowed_to_play = False
permission_to_play.rule = r'(?ims)^(jenny|$nickname)\:\s.*'
