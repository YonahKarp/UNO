from Card import Card
import random

class Deck:
    def __init__(self, discard):
        self.cards = []
        self.generateDeck()
        self.discard = discard
        random.shuffle(self.cards)

        topCard = self.cards.pop()
        if(topCard.isWild()):
            colors = ['blue', 'red', 'green', 'yellow']
            topCard.wild(random.choice(colors))
        discard.append(topCard)

    def __str__(self):
        return str(self.name) + ":" + self.colsor

    def generateDeck(self):
        colors = ['blue', 'red', 'green', 'yellow']

        for i in range(2):
            for color in colors:
                for j in range(10):
                    if i + j == 0:
                        continue
                    self.cards.append(Card(j, color))

                self.cards.append(Card('◫', color)) #draw2
                self.cards.append(Card('↺', color)) #reverse
                self.cards.append(Card('∅', color)) #skip
                if i == 0:
                    self.cards.append(Card('☯', '')) #wild
                else:
                    self.cards.append(Card('❖', '')) #draw4

    def dealCards(self, player, numCards):
        for _ in range(numCards):
            if(len(self.cards) == 0):
                self.flipDiscard()

            card = self.cards.pop()
            if(card.isWild()):
                card.color = ''
            player.hand.append(card)
           


    def flipDiscard(self):
        tempDiscard = self.discard.pop()
        self.cards = self.discard
        self.discard = [tempDiscard]
        random.shuffle(self.cards)


    def print(self):
        for card in self.cards:
            print(str(card))
