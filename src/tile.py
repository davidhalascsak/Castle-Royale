import pygame
import random
import src.tower
import src.soldier


class Tile:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self._x = pos_x * 48
        self._y = pos_y * 48
        self._width = 48
        self._height = 48
        self.type = None
        # self.r = random.randint(0, 255)
        # self.g = random.randint(0, 255)
        # self.b = random.randint(0, 255)
        self._color = {
              None: (255, 255, 255),
              "DIRT": (161, 146, 101),
              "MOSS": (13, 64, 18),
              "MOUNT": (120, 125, 123)
        }
        self._hover_color = (48, 241, 255)
        self._hover = False
        self._structures = []

    def build(self, player, type):
        if len(self._structures) == 0:
            unit_price = eval("src.tower." + type).price
            if (player.gold - unit_price) > 0:
                player.gold = (player.gold - unit_price)
                unit = eval("src.tower." + type)(self.x, self.y, self, player)
                player.add(unit)
                self._structures.append(unit)
                print(unit.__dict__)

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
            return self._color[self.type]
