"""
Copyright 2010 Tamas Marki. All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are
permitted provided that the following conditions are met:

   1. Redistributions of source code must retain the above copyright notice, this list of
      conditions and the following disclaimer.

   2. Redistributions in binary form must reproduce the above copyright notice, this list
      of conditions and the following disclaimer in the documentation and/or other materials
      provided with the distribution.

THIS SOFTWARE IS PROVIDED BY TAMAS MARKI ``AS IS'' AND ANY EXPRESS OR IMPLIED
WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL TAMAS MARKI OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


[18:03] <Lako> .play w 3
[18:03] <unobot> TopMobil's turn. Top Card: *]
[18:03] [Notice] -unobot- Your cards: [4][9][4][8][D2][D2]
[18:03] [Notice] -unobot- Next: hatcher (5 cards) - Lako (2 cards)
[18:03] <TopMobil> :O
[18:03] <Lako> :O
"""

import random
from datetime import datetime, timedelta

CHANNEL = '##torvalds'
SCOREFILE = "/home/yano/jenny/unoscores.txt"

STRINGS = {
    'ALREADY_STARTED' : '\x0300,01Game already started by %s! Type join to join!',
    'GAME_STARTED' : '\x0300,01IRC-UNO started by %s - Type join to join!',
    'GAME_STOPPED' : '\x0300,01Game stopped.',
    'CANT_STOP' : '\x0300,01%s is the game owner, you can\'t stop it!',
    'DEALING_IN' : '\x0300,01Dealing %s into the game as player #%s!',
    'JOINED' : '\x0300,01Dealing %s into the game as player #%s!',
    'ENOUGH' : '\x0300,01There are enough players, type .deal to start!',
    'NOT_STARTED' : '\x0300,01Game not started, type .uno to start!',
    'NOT_ENOUGH' : '\x0300,01Not enough players to deal yet.',    
    'NEEDS_TO_DEAL' : '\x0300,01%s needs to deal.',
    'ALREADY_DEALT' : '\x0300,01Already dealt.',
    'ON_TURN' : '\x0300,01It\'s %s\'s turn.',
    'DONT_HAVE' : '\x0300,01You don\'t have that card, %s',
    'DOESNT_PLAY' : '\x0300,01That card does not play, %s',
    'UNO' : '\x0300,01UNO! %s has ONE card left!',
    'WIN' : '\x0300,01We have a winner! %s!!!! This game took %s',
    'DRAWN_ALREADY' : '\x0300,01You\'ve already drawn, either .pass or .play!',
    'DRAWS' : '\x0300,01%s draws a card',
    'DRAWN_CARD' : '\x0300,01Drawn card: %s',
    'DRAW_FIRST' : '\x0300,01%s, you need to draw first!',
    'PASSED' : '\x0300,01%s passed!',
    'NO_SCORES' : '\x0300,01No scores yet',
    'SCORE_ROW' : '\x0300,01#%s %s (%s points %s games, %s won, %s wasted)',
    'TOP_CARD' : '\x0300,01%s\'s turn. Top Card: %s',
    'YOUR_CARDS' : '\x0300,01Your cards: %s',
    'NEXT_START' : '\x0300,01Next: ',
    'NEXT_PLAYER' : '\x0300,01%s (%s cards)',
    'D2' : '\x0300,01%s draws two and is skipped!',
    'CARDS' : '\x0300,01Cards: %s',
    'WD4' : '\x0300,01%s draws four and is skipped!',
    'SKIPPED' : '\x0300,01%s is skipped!',
    'REVERSED' : '\x0300,01Order reversed!',
    'GAINS' : '\x0300,01%s gains %s points!',
}

class unobot:
    def __init__ (self):
        self.colored_card_nums = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'R', 'S', 'D2' ]
        self.special_scores = { 'R' : 20, 'S' : 20, 'D2' : 20, 'W' : 50, 'WD4' : 50}
        self.colors = 'RGBY'
        self.special_cards = [ 'W', 'WD4' ]
        self.players = { }
        self.playerOrder = [ ]
        self.game_on = False
        self.currentPlayer = 0
        self.topCard = None
        self.way = 1
        self.drawn = False
        self.scoreFile = SCOREFILE
        self.deck = [ ]

        #========
        self.allowed_to_play = False
        self.my_cards = "" 
        #========
    
    def start(self, jenny, owner):
        if self.game_on:
            jenny.msg (CHANNEL, STRINGS['ALREADY_STARTED'] % self.game_on)
        else:
            self.game_on = owner
            self.deck = [ ]
            jenny.msg (CHANNEL, STRINGS['GAME_STARTED'] % owner)
            self.players = { }
            self.players[owner] = [ ]
            self.playerOrder = [ owner ]
    
    def stop (self, jenny, input):
        if input.nick == self.game_on:
            jenny.msg (CHANNEL, STRINGS['GAME_STOPPED'])
            self.game_on = False
        elif self.game_on:
            jenny.msg (CHANNEL, STRINGS['CANT_STOP'] % self.game_on)
            
    def join (self, jenny, input):
        #print dir (jenny.bot)
        #print dir (input)
        jenny.say("I'm joining a person to the game.")
        if self.game_on:
            jenny.say("Game is on.")
            if input.nick not in self.players:
                jenny.say("if input.nick not in self.players")
                self.players[input.nick] = [ ]
                self.playerOrder.append (input.nick)
                if self.deck:
                    jenny.say("if self.deck")
                    for i in xrange (0, 7):
                        self.players[input.nick].append (self.getCard ())
                    jenny.msg (CHANNEL, STRINGS['DEALING_IN'] % (input.nick, self.playerOrder.index (input.nick) + 1))
                else:
                    jenny.msg (CHANNEL, STRINGS['JOINED'] % (input.nick, self.playerOrder.index (input.nick) + 1))
                    if len (self.players) > 1:
                        jenny.msg (CHANNEL, STRINGS['ENOUGH'])
        else:
            jenny.msg (CHANNEL, STRINGS['NOT_STARTED'])
    
    def deal (self, jenny, input):
        if not self.game_on:
            jenny.msg (CHANNEL, STRINGS['NOT_STARTED'])
            return
        if len (self.players) < 2:
            jenny.msg (CHANNEL, STRINGS['NOT_ENOUGH'])
            return
        if input.nick != self.game_on:
            jenny.msg (CHANNEL, STRINGS['NEEDS_TO_DEAL'] % self.game_on)
            return
        if len (self.deck):
            jenny.msg (CHANNEL, STRINGS['ALREADY_DEALT'])
            return
        self.startTime = datetime.now ()
        self.deck = self.createnewdeck ()
        for i in xrange (0, 7):
            for p in self.players:
                self.players[p].append (self.getCard ())
        self.topCard = self.getCard ()
        while self.topCard in ['W', 'WD4']: self.topCard = self.getCard ()
        self.currentPlayer = 1
        self.cardPlayed (jenny, self.topCard)
        self.showOnTurn (jenny, input)
    
    def play_part1 (self, jenny, input):
        if not self.game_on or not self.deck:
            return
        if input.nick != self.playerOrder[self.currentPlayer]:
            jenny.msg (CHANNEL, STRINGS['ON_TURN'] % self.playerOrder[self.currentPlayer])
            return
        tok = [z.strip () for z in str (input).upper ().split (' ')]
        if len (tok) != 3:
            return
        searchcard = ''
        if tok[1] in self.special_cards:
            searchcard = tok[1]
        else:
            searchcard = (tok[1] + tok[2])
        if searchcard not in self.players[self.playerOrder[self.currentPlayer]]:
            jenny.msg (CHANNEL, STRINGS['DONT_HAVE'] % self.playerOrder[self.currentPlayer])
            return
        playcard = (tok[1] + tok[2])
        if not self.cardPlayable (playcard):
            jenny.msg (CHANNEL, STRINGS['DOESNT_PLAY'] % self.playerOrder[self.currentPlayer])
            return

        self.play_part2 (jenny, input, searchcard, playcard)

    def play_part2 (self, jenny, input, searchcard, playcard):
        print "searchcard: " + str(searchcard)
        print "playcard: " + str(playcard)
        self.drawn = False
        self.players[self.playerOrder[self.currentPlayer]].remove (searchcard)
        
        pl = self.currentPlayer
        
        self.incPlayer ()
        self.cardPlayed (jenny, playcard)

        if len (self.players[self.playerOrder[pl]]) == 1:
            jenny.msg (CHANNEL, STRINGS['UNO'] % self.playerOrder[pl])
        elif len (self.players[self.playerOrder[pl]]) == 0:
            jenny.msg (CHANNEL, STRINGS['WIN'] % (self.playerOrder[pl], (datetime.now () - self.startTime)))
            self.gameEnded (jenny, self.playerOrder[pl])
            return
            
        self.showOnTurn (jenny, input)

    def draw (self, jenny, input):
        if not self.game_on or not self.deck:
            return
        if input.nick != self.playerOrder[self.currentPlayer]:
            jenny.msg (CHANNEL, STRINGS['ON_TURN'] % self.playerOrder[self.currentPlayer])
            return
        if self.drawn:
            jenny.msg (CHANNEL, STRINGS['DRAWN_ALREADY'])
            return
        self.drawn = True
        jenny.msg (CHANNEL, STRINGS['DRAWS'] % self.playerOrder[self.currentPlayer])
        c = self.getCard ()
        self.players[self.playerOrder[self.currentPlayer]].append (c)
        jenny.notice (input.nick, STRINGS['DRAWN_CARD'] % self.renderCards ([c]))
        if input.nick == jenny.config.nick:
            self.make_a_move(jenny, input) 
    # this is not a typo, avoiding collision with Python's pass keyword
    def passs (self, jenny, input):
        if not self.game_on or not self.deck:
            return
        if input.nick != self.playerOrder[self.currentPlayer]:
            jenny.msg (CHANNEL, STRINGS['ON_TURN'] % self.playerOrder[self.currentPlayer])
            return
        if not self.drawn:
            jenny.msg (CHANNEL, STRINGS['DRAW_FIRST'] % self.playerOrder[self.currentPlayer])
            return
        self.drawn = False
        jenny.msg (CHANNEL, STRINGS['PASSED'] % self.playerOrder[self.currentPlayer])
        self.incPlayer ()
        self.showOnTurn (jenny, input)
    
    def top10 (self, jenny):
        from copy import copy
        prescores = [ ]
        try:
            f = open (self.scoreFile, 'r')
            for l in f:
                t = l.replace ('\n', '').split (' ')
                if len (t) < 4: continue
                prescores.append (copy (t))
                if len (t) == 4: t.append (0)
            f.close ()
        except: pass
        prescores = sorted (prescores, lambda x, y: cmp ((y[1] != '0') and (float (y[3]) / int (y[1])) or 0, (x[1] != '0') and (float (x[3]) / int (x[1])) or 0))
        if not prescores:
            jenny.say(STRINGS['NO_SCORES'])
        i = 1
        for z in prescores[:10]:
            jenny.say(STRINGS['SCORE_ROW'] % (i, z[0], z[3], z[1], z[2], timedelta (seconds = int (z[4]))))
            i += 1

    
    def createnewdeck (self):
        ret = [ ]
        for a in self.colored_card_nums:
            for b in self.colors:
                ret.append (b + a)
        for a in self.special_cards: 
            ret.append (a)
            ret.append (a)
        
        ret *= 2
        random.shuffle (ret)
        return ret
    
    def getCard(self):
        ret = self.deck[0]
        self.deck.pop (0)
        if not self.deck:
            self.deck = self.createnewdeck ()        
        return ret
    
    def showOnTurn (self, jenny, input):
        jenny.msg (CHANNEL, STRINGS['TOP_CARD'] % (self.playerOrder[self.currentPlayer], self.renderCards ([self.topCard])))
        if self.playerOrder[self.currentPlayer] == jenny.config.nick:
            self.make_a_move(jenny, input)
        jenny.notice (self.playerOrder[self.currentPlayer], STRINGS['YOUR_CARDS'] % self.renderCards (self.players[self.playerOrder[self.currentPlayer]]))
        msg = STRINGS['NEXT_START']
        tmp = self.currentPlayer + self.way
        if tmp == len (self.players):
            tmp = 0
        if tmp < 0:
            tmp = len (self.players) - 1
        arr = [ ]
        while tmp != self.currentPlayer:
            arr.append (STRINGS['NEXT_PLAYER'] % (self.playerOrder[tmp], len (self.players[self.playerOrder[tmp]])))
            tmp = tmp + self.way
            if tmp == len (self.players):
                tmp = 0
            if tmp < 0:
                tmp = len (self.players) - 1
        msg += ' - '.join (arr)
        jenny.notice (self.playerOrder[self.currentPlayer], msg)
    
    def showCards (self, jenny, user):
        if not self.game_on or not self.deck:
            return
        jenny.notice (user, STRINGS['YOUR_CARDS'] % self.renderCards (self.players[user]))

    def renderCards (self, cards):
        ret = [ ]
        for c in sorted (cards):
            if c in ['W', 'WD4']:
                ret.append ('\x0300,01[' + c + ']')
                continue
            if c[0] == 'W':
                c = c[-1] + '*'
            t = '\x0300,01\x03'
            if c[0] == 'B':
                t += '11,01['
            if c[0] == 'Y':
                t += '08,01['
            if c[0] == 'G':
                t += '09,01['
            if c[0] == 'R':
                t += '04,01['
            t += c[1:] + ']\x0300,01'
            ret.append (t)
        return ''.join (ret)
    
    def cardPlayable (self, card):
        if card[0] == 'W' and card[-1] in self.colors:
            return True
        if self.topCard[0] == 'W':
            return card[0] == self.topCard[-1]
        return (card[0] == self.topCard[0]) or (card[1] == self.topCard[1])
    
    def cardPlayed (self, jenny, card):
        if card[1:] == 'D2':
            jenny.msg (CHANNEL, STRINGS['D2'] % self.playerOrder[self.currentPlayer])
            z = [self.getCard (), self.getCard ()]
            jenny.notice(self.playerOrder[self.currentPlayer], STRINGS['CARDS'] % self.renderCards (z))
            self.players[self.playerOrder[self.currentPlayer]].extend (z)
            self.incPlayer ()
        elif card[:2] == 'WD':
            jenny.msg (CHANNEL, STRINGS['WD4'] % self.playerOrder[self.currentPlayer])
            z = [self.getCard (), self.getCard (), self.getCard (), self.getCard ()]
            jenny.notice(self.playerOrder[self.currentPlayer], STRINGS['CARDS'] % self.renderCards (z))
            self.players[self.playerOrder[self.currentPlayer]].extend (z)
            self.incPlayer ()
        elif card[1] == 'S':
            jenny.msg (CHANNEL, STRINGS['SKIPPED'] % self.playerOrder[self.currentPlayer])
            self.incPlayer ()
        elif card[1] == 'R' and card[0] != 'W':
            jenny.msg (CHANNEL, STRINGS['REVERSED'])
            if len(self.players) > 2:
                self.way = -self.way
                self.incPlayer ()
                self.incPlayer ()
            else:
                self.incPlayer ()
        self.topCard = card
    
    def gameEnded (self, jenny, winner):
        try:
            score = 0
            for p in self.players:
                for c in self.players[p]:
                    if c[0] == 'W':
                        score += self.special_scores[c]
                    elif c[1] in [ 'S', 'R', 'D' ]:
                        score += self.special_scores[c[1:]]
                    else:
                        score += int (c[1])
            jenny.msg (CHANNEL, STRINGS['GAINS'] % (winner, score))
            self.saveScores (self.players.keys (), winner, score, (datetime.now () - self.startTime).seconds)
        except Exception, e:
            print 'Score error: %s' % e
        self.players = { }
        self.playerOrder = [ ]
        self.game_on = False
        self.currentPlayer = 0
        self.topCard = None
        self.way = 1
        
    
    def incPlayer (self):
        self.currentPlayer = self.currentPlayer + self.way
        if self.currentPlayer == len (self.players):
            self.currentPlayer = 0
        if self.currentPlayer < 0:
            self.currentPlayer = len (self.players) - 1
    
    def saveScores (self, players, winner, score, time):
        from copy import copy
        prescores = { }
        try:
            f = open (self.scoreFile, 'r')
            for l in f:
                t = l.replace ('\n', '').split (' ')
                if len (t) < 4: continue
                if len (t) == 4: t.append (0)
                prescores[t[0]] = [t[0], int (t[1]), int (t[2]), int (t[3]), int (t[4])]
            f.close ()
        except: pass
        for p in players:
            if p not in prescores:
                prescores[p] = [ p, 0, 0, 0, 0 ]
            prescores[p][1] += 1
            prescores[p][4] += time
        prescores[winner][2] += 1
        prescores[winner][3] += score
        try:
            f = open (self.scoreFile, 'w')
            for p in prescores:
                f.write (' '.join ([str (s) for s in prescores[p]]) + '\n')
            f.close ()
        except Exception, e:
            print 'Failed to write score file %s' % e
    
    #=====
    def make_a_move (self, jenny, input):
        self.my_cards = self.players[jenny.config.nick]
        print "My cards: " + str(self.my_cards)

        top_card = self.renderCards ([self.topCard])
        print "Top Card: " + str(self.topCard)

        card_to_play = None
        points_for_play = 0
        playable_cards = [ ]

        # Make a list of all possible cards that *could* be played
        for each_current in self.my_cards:
            if self.topCard[0] == "W" and len(self.topCard) == 2:
                if topCard[1] == each_current[0]:
                    playable_cards.append(each_current)
            elif len(each_current) == 2: # If card is standard colour plus number.
                if str(each_current[1]) == str(self.topCard[1]):
                    playable_cards.append(each_current)
                elif str(each_current[0]) == str(self.topCard[0]):
                    playable_cards.append(each_current)
            elif len(each_current) == 3: # If the card is a WD4 (wild card plus draw four)
                if str(each_current) == "WD4":
                    playable_cards.append(each_current)
                elif str(each_current[0]) == str(self.topCard[0]):
                    playable_cards.append(each_current)
            else:
                print "There is something seriously wrong!"

        print "playable_cards: " + str(playable_cards)

        # Determine which card among the ones which can be played is the best
        # choice to make. Basically if the card is worth the most points, it
        # should be played before any other playable card.

        # self.special_scores
        # self.colored_card_nums = [ '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'R', 'S', 'D2' ]
        # self.special_scores = { 'R' : 20, 'S' : 20, 'D2' : 20, 'W' : 50, 'WD4' : 50}

        points_dict = { } 
        # Create a dictionary with the point values of the cards that can play
        for item in playable_cards:
            if len(playable_cards) == 1:
                card_to_play = item
            elif len(playable_cards) == 2:
                if item[1] == "S" or item[1] == "R":
                    points_dict[item] = 20
                else:
                    points_dict[item] = item[1]
            elif len(playable_cards) == 3:
                #if item == "WD4":
                #    points_
                if item[1:3] == "D2":
                    points_dict[item] = 20

        print "points_dict: " + str(points_dict)

        # Find highest value in dictionary
        if len(points_dict) > 0:
            b = points_dict.keys()
            b.sort( key = points_dict.__getitem__ )
            card_to_play = b[-1]

        if card_to_play is None:
            # Draw a new card
            input.nick = jenny.config.nick
            self.draw(jenny, input)
        else:
            color_to_play = random.choice(['R', 'G', 'B', 'Y'])
            # Play the card
            if len(card_to_play) == 3:
                jenny.say(".play " + str(card_to_play[0:3]) + " " + str(color_to_play))
            elif len(card_to_play) == 2:
                jenny.say(".play " + str(card_to_play[0]) + " " + str(card_to_play[1]))
            elif len(card_to_play) == 1:
                jenny.say(".play " + str(card_to_play[0]) + " " + str(color_to_play))

            self.play_part2 (jenny, input, card_to_play, card_to_play)

        print "My Cards: " + str(self.players[jenny.config.nick])
        print "=========="
if __name__ == '__main__':
       print __doc__.strip()
