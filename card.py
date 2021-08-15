import pygame as p
import os
from settings import Settings

class Card(p.sprite.Sprite):
    
    def __init__(self, suit, rank):
        super().__init__()
        self.settings = Settings()
        self.screen = self.settings.screen
        self.rank = rank
        try:
            self.rank = int(self.rank)
        except:
            pass
        self.suit = suit
        self.side = None
        self.image = self.createSingleCard()
        self.rect = self.image.get_rect()
        self.x = self.rect.x
        self.y = self.rect.y
    
    
    def createSingleCard(self):
        if self.rank == "J" and not self.suit:
            image = p.image.load(self.getImagePath("Joker"))
        elif self.rank == "back" and not self.suit:    
            image = p.image.load(self.getImagePath("back"))
        else:
            image = p.image.load(self.getImagePath())
        w, h = image.get_width(), image.get_height()
        image = p.transform.scale(image, (w // ((self.settings.W + self.settings.H) // 1000), h // ((self.settings.W + self.settings.H) // 1000)))
        return image
    
    
    def getImagePath(self, typeOfCard=False):
        filepath = os.path.dirname(__file__)
        if typeOfCard == "back":
            return os.path.join(filepath, "img", "back.png")
        elif typeOfCard == "Joker":
            return os.path.join(filepath, "img", "J.png")

        return os.path.join(filepath, "img", self.suit[0] + str(self.rank) + ".png")
    
    
    def checkHit(self, x, y):
        if self.rect.collidepoint(x, y):
            return True
        return False