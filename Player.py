class Player:
    def __init__(self, game, index, hand = []):
        self.game = game
        self.index = index
        self.hand = hand
        self.skipped = False
        self.assessedHand = {}

    def playTurn(self):
        if(self.skipped):
            print(str(self) + " skipped\n")
            self.skipped = False
            return
        
        #self.printHand()
        self.assessHandAndPlayCard()

    def assessHandAndPlayCard(self):
        self.resetAssessment()
        
        for card in self.hand:
            self.assessLegality(card)
            self.assessColor(card)

        if(len(self.assessedHand["legal"]) == 0):
            self.game.deck.dealCards(self,1)
            if(self.assessLegality(self.hand[-1])):
                self.playCard({"card": self.hand[-1:], "index": len(self.hand) - 1})
            return
        
        cardScores = self.scoreLegalOptions()
        cardScores.sort(key = lambda card : card["score"])
        carToPlay = cardScores[-1]

        self.playCard(carToPlay)


    def resetAssessment(self):
        self.assessedHand = {
            "legal": [],
            "blue": 0,
            "red": 0,
            "green": 0,
            "yellow": 0,
            "wild": 0
        }

    def assessLegality(self, card):
        topCard = self.game.discard[-1]
        if card.isWild() or card.color == topCard.color or card.name == topCard.name :
            self.assessedHand["legal"].append(card)
    
    def assessColor(self, card):
        if card.isWild():
            self.assessedHand["wild"] += 1
        else:
            self.assessedHand[card.color] += 1

    def scoreLegalOptions(self):
        rankings = self.assessOtherPlayers()
        topCard =  self.game.discard[-1] 
        nextPlayer = self.game.players[(self.index + self.game.playOrder) % len(self.game.players)]
        previousPlayers = self.game.players[(self.index + self.game.playOrder) % len(self.game.players)]

        cardScores = []

        for card in self.assessedHand["legal"]:
            score = 0
            if(card.isWild()):
                if card.name == '❖':
                    score = 100 if self.closeToWinning(nextPlayer) else 0 if self.isWinning(self, nextPlayer, rankings) else 20
                else:
                    score= 1
            
            elif(card.name == '◫'):
                if card.color == topCard.color:
                    score = 50 if self.closeToWinning(nextPlayer) else 2 if self.isWinning(self, nextPlayer, rankings) else 15
                else:
                    score = 16 if self.closeToWinning(nextPlayer) else 1 if self.isWinning(self, nextPlayer, rankings) else 8

            elif(card.name == '∅'):
                if card.color == topCard.color:
                    score =  30 if self.closeToWinning(nextPlayer) else 3 if self.isWinning(self, nextPlayer, rankings) else 14
                else:
                    score = 14 if self.closeToWinning(nextPlayer) else 1 if self.isWinning(self, nextPlayer, rankings) else 7

            elif(card.name == '↺'):
                if card.color == topCard.color:
                    score = 20 if self.isWinning(nextPlayer, previousPlayers, rankings)\
                                or (self.closeToWinning(nextPlayer) and not self.closeToWinning(previousPlayers))\
                            else 4
                else:
                    score = 13 if self.closeToWinning(nextPlayer) else 1 if self.isWinning(self, nextPlayer, rankings) else 7


            elif(card.color == topCard.color):
                if self.assessedHand[card.color] == 1:
                    score = 12
                elif self.assessedHand[card.color] > 4:
                    score = 11
                else:
                    score = 10
            
            elif self.assessedHand[card.color] > self.assessedHand[topCard.color]:
                if self.assessedHand[card.color] > 4:
                    score = 6
                else:
                    score = 5
            elif self.assessedHand[card.color] == 1:
                    score = 9
            else:
                score = 4

            cardScores.append({"card": card, "score": score})

        
        self.printOptions(cardScores)
        return cardScores


    def isWinning(self, player, otherPlayer, rankings):
        return len(player.hand) <= len(otherPlayer.hand)
    
    def closeToWinning(self, player):
        return len(player.hand) <= 2

    def assessOtherPlayers(self):

        playerRankings = [
            {'cards':len(player.hand), 'index':i} for i, player in enumerate(self.game.players)
        ]
        playerRankings.sort(key=lambda p : p['cards'])
        
        rankings = [
            {**playerRanking, 'rank': i } for i, playerRanking in enumerate(playerRankings)
        ]
        
        return rankings

    def chooseWildColor(self):
        colorArr = [{
                "color": 'blue',
                "count": self.assessedHand['blue']
            },{
                "color": 'red',
                "count": self.assessedHand['red']
            },{
                "color": 'yellow',
                "count": self.assessedHand['yellow']
            },{
                "color": 'green',
                "count": self.assessedHand['green']
            }]
        
        colorArr.sort(key=lambda color : color['count'])
        return colorArr[-1]["color"]

    def playCard(self, cardToPlay):
        print(str(self) + " plays: " + str(cardToPlay["card"]))
        cardIndex = self.hand.index(cardToPlay["card"])
        card = self.hand.pop(cardIndex)
        self.game.discard.append(card)

        if len(self.hand) == 1:
            print(str(self) +": UNO!")
        if len(self.hand) == 0:
            print("player" + str(self.index) +" wins!!")
            self.game.gameOver = True

        print()


        self.useCardEffect(card)

        #TO:DO implement effects

    def useCardEffect(self, card):
        if card.effect:
            if card.isWild():
                card.useEffect(self.chooseWildColor(), self.game)
            else:
                card.useEffect(self.game)

    def printHand(self):
        print(str(self) + "'s hand:" )
        for i, card in enumerate(self.hand):
            print(str(card), end = '' if i == len(self.hand) else '⎦')
        print()

    def printOptions(self, options):
        print("Weighing Options:")
        for option in options:
            print(str(option['card']) + " with score of " + str(option['score']) )

    def __str__(self):
        return 'player' + str(self.index)
