
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
play.commands = ['play', 'p']
play.priority = 'low'

def draw(jenny, input):
    bot.draw (jenny, input)
draw.commands = ['draw', 'd']
draw.priority = 'low'

def passs(jenny, input):
    bot.passs (jenny, input)
passs.commands = ['pass', 'pa']
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
        time.sleep(1)
        input.nick = jenny.config.nick
        bot.join(jenny, input)
jenny_join.rule = '^.uno$'

def permission_to_play(jenny, input):
    text = input.group().split(": ")
    if text[1] == 'play':
        bot.allowed_to_play = True
        jenny.say("I will join the next game.")
    elif text[1] == 'stop':
        bot.allowed_to_play = False
        jenny.say("I will only host the next game.")
permission_to_play.rule = r'(?i)^(jenny|$nickname)\:\s.*'
