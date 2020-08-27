from Deck import Deck
from Player import Player


class Game:

    def __init__(self, nPlayers):
        cls = lambda: print('\n'*10)
        cls()
        self.discard = []
        self.deck = Deck(self.discard)
        self.playOrder = 1 #clockwise
        self.currentIndex = 0
        self.players = []
        self.gameOver = False

        for i in range(nPlayers):
            player = Player(self, i, [])
            self.deck.dealCards(player, 7)

            self.players.append(player)
            player.printHand()
        
        print("\nGAME START:\n")

        while(not self.gameOver):
            currentPlayer = self.players[self.currentIndex]
            print(str(currentPlayer) + "'s turn. Top card is " + str(self.discard[-1]))
            
            currentPlayer.printHand()
            currentPlayer.playTurn()
            self.currentIndex = (self.currentIndex + self.playOrder) % len(self.players)
        
        print("\nGAME OVER:\n")

            
    

