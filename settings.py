import pygame as p

class Settings:
    
    def __init__(self):
        self.screen = p.display.set_mode((0, 0), p.FULLSCREEN)
        self.W, self.H = self.screen.get_width(), self.screen.get_height()
        self.bgColor = (50,205,50)
        self.Jokers = 4 ### NUMBER OF JOKERS
        self.cardNum = 5 ### NUMBER OF CARDS AT THE START
        self.seperator = 10 ### PX BETWEEN TWO CARD
        self.swapTurn = {
            1: 2,
            2: 1
        }
        
        self.drawButtonColor = (111, 122, 143)
        self.drawButtonBG = (40,205,255)
        p.font.init()
        self.drawButtonFont = p.font.SysFont("arial", 45, True)
        
        