import pygame
import random


class Tile:
    def __init__(self, pos_x, pos_y):
        self._x = pos_x * 48
        self._y = pos_y * 48
        self._width = 48
        self._height = 48
        # self.r = random.randint(0, 255)
        # self.g = random.randint(0, 255)
        # self.b = random.randint(0, 255)
        self._color = (255, 255, 255)
        self._hover_color = (48, 241, 255)
        self._hover = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.get_color(), pygame.Rect(self._x, self._y, self._width, self._height))
        # pygame.display.flip()

    def is_over(self, pos):
        if self._x < pos[0] < self._x + self._width:
            if self._y < pos[1] < self._y + self._height:
                self._hover = True
                return True
        self._hover = False

    def get_color(self):
        if self._hover:
            return self._hover_color
        else:
            return self._color
