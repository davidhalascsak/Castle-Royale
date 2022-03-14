import pygame
import random

class Tile:
    def __init__(self, posX, posY):
        self.x = posX * 48
        self.y = posY * 48
        self.width = 48
        self.height = 48
        # self.r = random.randint(0, 255)
        # self.g = random.randint(0, 255)
        # self.b = random.randint(0, 255)
        self.color = (255, 255, 255)
        self.hoverColor = (48, 241, 255)
        self.hover = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.getColor(), pygame.Rect(self.x, self.y, self.width, self.height))
        # pygame.display.flip()

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                self.hover = True
                return True
        self.hover = False

    def getColor(self):
        if self.hover:
            return self.hoverColor
        else:
            return self.color
