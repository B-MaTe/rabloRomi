import pygame as p
from settings import Settings
from deck import FrenchDeck
from card import Card

class Main:
    
    def __init__(self):
        self.active = True
        self.settings = Settings()
        self.screen = self.settings.screen
        self.restart = False
        self.frenchDeck = FrenchDeck()
        self.deck = p.sprite.Group()
        self.firstPlayer = p.sprite.LayeredUpdates()
        self.secondPlayer = p.sprite.LayeredUpdates()
        self.middleSprite = p.sprite.LayeredUpdates()
        self.middleCards = []
        self.pickedCards = set()
        self.cardW, self.cardH = self.getImageSize()
        self.createDeck()
        self.dealCards()
        """
        self.turn = 1 ----> first player
        self.turn = 2 ----> second player
        """
        self.translateTurn = {
            1: self.firstPlayer,
            2: self.secondPlayer
        }
        self.turn = 1
        self.drawButtonFont = self.settings.drawButtonFont.render("Húzok", True, self.settings.drawButtonColor)
        self.madeMove = False
        self.dragging = False
        self.clickedCard = None
        
        
    def createDeck(self):
        for card in self.frenchDeck._cards:
            newCard = Card(card[1], card[0])
            self.deck.add(newCard)
            
        
    def getImageSize(self):
        ### CREATE AN INSTANCE CARD TO GET THE WIDTH OF THE IMAGE
        instanceCard = Card("h", "2")
        w = instanceCard.image.get_width() + self.settings.seperator
        h = instanceCard.image.get_height() + self.settings.seperator
        del instanceCard
        return w, h
        
        
    def drawButton(self):
        button = p.Rect(self.settings.W - 200, self.settings.H - 50, 200, 50)
        return button
    
    
    def getFirstCardX(self, player):
        length = len(player)    
        if length:
            w = self.settings.W
            return (w - (length * self.cardW)) / 2
        return False
    
    
    def arrangeCards(self, player):
        
        length = len(player)
        firstCard = self.getFirstCardX(player)
        for index, card in enumerate(player):
            card.y = self.settings.H - self.cardH
            if index == 0:
                card.x = firstCard
            else:
                card.x = index * self.cardW + firstCard
            card.rect.x, card.rect.y = card.x, card.y
    
    
    def checkTerc(self, listCards):
        key = None
        if len(listCards) < 3:
            return False
        for i, card in enumerate(listCards):
            if i == 0:
                suit = card.suit
            else:
                if suit != card.suit:
                    key = "rank"
                    break
        if not key:
            ### SAME SUIT
            values = {
                "J" : 11,
                "Q" : 12,
                "K" : 13,
                "A" : [1, 14],
                1: 1,
                2:2,
                3:3,
                4:4,
                5:5,
                6:6,
                7:7,
                8:8,
                9:9,
                10:10
            }
            
            ### SORT THE CARDS
            indexList = None
            cardList = None
            for card in listCards:
                if card.rank in list("JQKA"):
                    rank = values[card.rank]
                    if rank == [1, 14]:
                        for innerCard in listCards:
                            if innerCard.rank == 2:
                                rank = 1
                                break
                            elif innerCard.rank == "K":
                                rank = 14
                                break
                else:
                    rank = card.rank
                        
                if not indexList:
                    indexList = [rank]
                    cardList = [card]
                else:
                    inserted = False
                    for i in range(len(indexList)):
                        if rank < indexList[i]:
                            indexList.insert(i, rank)
                            cardList.insert(i, card)
                            inserted = True
                            break
                    if not inserted:
                        indexList.append(rank)
                        cardList.append(card)
                        
            for i in range(1, len(cardList)):
                if cardList[i].rank == "A":
                    if abs(cardList[i-1].rank - 1) != 1 and abs(cardList[i-1].rank - 14) != 1:
                        return False
                elif cardList[i-1].rank == "A":
                    if abs(cardList[i].rank - 1) != 1 and abs(cardList[i].rank - 14) != 1:
                        return False
                elif abs(values[cardList[i].rank] - values[cardList[i-1].rank]) != 1:
                    return False
                
            return cardList
                
        else:
            ### SAME RANK
            suits = []
            rank = None
            for card in listCards:
                if not rank:
                    rank = card.rank
                else:
                    if card.rank != rank:
                        return False
                    if card.suit in suits:
                        return False
                    suits.append(card.suit)
            return listCards

    
    def dealCards(self):
        for cardNum in range(self.settings.cardNum * 2):
            card = None
            for newCard in self.deck:
                card = newCard
                break
            if cardNum % 2 == 0:
               ### FIRST PLAYER
                self.firstPlayer.add(card)
                
            else:
                ### SECOND PLAYER
                self.secondPlayer.add(card)
                
            card.remove(self.deck)
        self.arrangeCards(self.firstPlayer)
        self.arrangeCards(self.secondPlayer)
        
        
    def drawCard(self, numberOfCards, player):
        for _ in range(numberOfCards):
            card = None
            for newCard in self.deck:
                card = newCard
                break
            length = len(player)
            firstCardX = self.getFirstCardX(player)
            card.x = card.x = length * self.cardW + firstCardX
            card.y = self.settings.H - self.cardH
            card.rect.x, card.rect.y = card.x, card.y
            player.add(card)
            
        card.remove(self.deck)
    
    
    def moveToMiddle(self, cards, player):
        for card in cards:
            ### REMOVE FROM HAND
            player.remove(card)
            self.middleSprite.add(card)
        self.middleCards.append(cards)
        self.arrangeMiddleCards()
        self.arrangeCards(player)
            
            
    def arrangeMiddleCards(self):
        if self.middleCards:
            width, height = self.settings.W, self.settings.H
            x = width * 0.02
            y = height * 0.02
            for terc in self.middleCards:
                for i in range(len(terc)):
                    card = terc[i]
                    card.x, card.y = x + i * self.cardW, y
                    card.rect.x, card.rect.y = card.x, card.y
                x += len(terc) * self.cardW + width * 0.02
                if x + 3 * self.cardW >= width:
                    x = width * 0.02
                    y += self.cardH + height * 0.02
        self.pickedCards = set()
                
                    
    def changeTurn(self):
        if not self.madeMove:
            self.drawCard(1, self.translateTurn[self.turn])
            self.arrangeCards(self.translateTurn[self.turn])
        self.turn = self.settings.swapTurn[self.turn]
        self.madeMove = False
        self.pickedCards = set()

         
    def events(self):
        for event in p.event.get():
            if event.type == p.QUIT:
                self.active = False
                
            elif event.type == p.KEYDOWN:
                if event.key == p.K_p:
                    self.active = False
                elif event.key == p.K_r:
                    self.restart = True
                    
            elif event.type == p.MOUSEBUTTONDOWN:
                self.dragging = True
                x, y = event.pos
                if x >= self.settings.W - 200 and y >= self.settings.H - 50:
                    self.changeTurn()
                else:
                    for card in self.translateTurn[self.turn]:
                        if card.checkHit(x, y):
                            self.dragging = True
                            self.translateTurn[self.turn].move_to_front(card)
                            if event.button == 1:
                                self.pickedCards.add(card)
                                if self.checkTerc(self.pickedCards):
                                    self.moveToMiddle(list(self.pickedCards), self.translateTurn[self.turn])
                            elif event.button == 3:
                                self.pickedCards.remove(card)
                                if self.checkTerc(self.pickedCards):
                                    self.moveToMiddle(list(self.pickedCards), self.translateTurn[self.turn])
                            """card.rect.x = x - self.cardW / 2
                            card.rect.y = y - self.cardH / 2"""
                            self.clickedCard = card
                            break
                    
            elif event.type == p.MOUSEMOTION:
                """
                if self.dragging and self.clickedCard:
                    x, y = event.pos
                    self.clickedCard.rect.x = x - self.cardW / 2
                    self.clickedCard.rect.y = y - self.cardH / 2"""
            
            
            elif event.type == p.MOUSEBUTTONUP:
                self.dragging = False
                self.clickedCard = None
                
                
    def run(self):
        ### BG
        self.screen.fill(self.settings.bgColor)
        
        ### drawButton
        p.draw.rect(self.screen, self.settings.drawButtonBG, self.drawButton())
        self.screen.blit(self.drawButtonFont, (self.settings.W - 160, self.settings.H - 53))
        
        ### CARDS
        if self.turn == 1:
            self.firstPlayer.draw(self.screen)
        else:
            self.secondPlayer.draw(self.screen)
        self.middleSprite.draw(self.screen)
        self.middleSprite.update()
        
        p.display.flip()