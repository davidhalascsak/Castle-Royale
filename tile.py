import pygame
import random

class Tile:
    def __init__(self, posX, posY):
        self.x = posX * 48
        self.y = posY * 48
        self.r = random.randint(0, 255)
        self.g = random.randint(0, 255)
        self.b = random.randint(0, 255)

    def draw(self, surface):
        pygame.draw.rect(surface, (self.r, self.g, self.b), pygame.Rect(self.x, self.y, 48, 48))
        pygame.display.flip()
