from colors import colors

class Card:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.setEffect()

    def playCard(self):
        print()

    def __str__(self):
        return colors[self.color] + str(self.name) + colors['end']

    def isWild(self):
        return self.name in ['☯', '❖']

    def draw2(self, game):
        targetPlayer = self.getNextPlayer(game)
        game.deck.dealCards(targetPlayer, 2)

    def draw4(self, color, game):
        targetPlayer =  self.getNextPlayer(game)
        game.deck.dealCards(targetPlayer, 4)
        self.color = color

    def wild(self, color, game=False):
        self.color = color
    
    def reverse(self, game):
        game.playOrder *= -1

    def skip(self, game):
        targetPlayer = self.getNextPlayer(game)
        targetPlayer.skipped = True
    
    def getNextPlayer(self, game):
        return game.players[(game.currentIndex + game.playOrder) % len(game.players)]

    def setEffect(self):
        if self.name == "◫":
            self.effect = self.draw2
        elif self.name == "☯":
            self.effect = self.wild
        elif self.name == "↺":
            self.effect = self.reverse
        elif self.name == "∅":
            self.effect = self.skip
        elif self.name == "❖":
            self.effect = self.draw4
        else:
            self.effect = False
    
    def useEffect(self, *args):
        if self.effect:
            self.effect(*args)


    