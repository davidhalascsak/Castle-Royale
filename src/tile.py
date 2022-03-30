import pygame
import random
from src.castle import *
from src.soldier import *
from src.tower import *


class Tile:
    def __init__(self, game, pos_x, pos_y):
        self._game_ref = game
        self.x = pos_x
        self.y = pos_y
        self._x = pos_x * 48
        self._y = pos_y * 48
        self._width = 48
        self._height = 48
        self._color = {
            None: (255, 255, 255),
            "DIRT": (161, 146, 101),
            "MOSS": (13, 64, 18),
            "MOUNT": (120, 125, 123)
        }
        self._hover_color = (48, 241, 255)
        self._hover = False
        self._is_castle = False
        self._units = []
        self._font = pygame.font.SysFont('Arial', 20)

    def add_castle(self, castle):
        self._units.append(castle)
        self._is_castle = True

    def build(self, player, type):
        if len(self._units) == 0:
            unit_price = eval(type).price
            if (player.gold - unit_price) > 0:
                player.gold = (player.gold - unit_price)
                unit = eval(type)(self, player, self.x, self.y)
                player.add_unit(unit)
                self._units.append(unit)

    def train(self, player, soldier):
        count = 0
        for unit in self._units:
            if issubclass(type(unit), Soldier):
                count += 1

        if count < 4:
            unit_price = eval(soldier).price
            if (player.gold - unit_price) > 0:
                player.gold = (player.gold - unit_price)
                unit = eval(soldier)(self, player, self.x, self.y)
                player.add_unit(unit)
                self._units.append(unit)

    def draw(self, surface):
        if self._is_castle:
            pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self._x, self._y, self._width, self._height))
        else:
            pygame.draw.rect(surface, self.get_color(), pygame.Rect(self._x, self._y, self._width, self._height))
        # pygame.display.flip()

        if self._hover and ((len(self._units) > 0 and issubclass(type(self._units[0]), Soldier)) or
                            (self._is_castle and len(self._units) > 1 and issubclass(type(self._units[1]), Soldier))):
            start = 0
            ind = 0
            length = len(self._units)
            if self._is_castle:
                start = 1
                length -= 1
            if self._x < 14 * 48:
                pygame.draw.rect(surface, pygame.Color(0, 0, 0), pygame.Rect(self._x + 48, self._y, 170, length * 18))
                for i in range(start, len(self._units)):
                    text = pygame.font.SysFont('Arial', 17).render("{0} - {1}/{2}".
                                                                   format(type(self._units[i]).__name__,
                                                                          self._units[i].health,
                                                                          eval(type(self._units[i]).__name__).max_health),
                                                                   False, self.get_owner_color(i))
                    surface.blit(text, (self._x + 48, self._y + (ind * 16)))
                    ind += 1
            else:
                pygame.draw.rect(surface, pygame.Color(0, 0, 0), pygame.Rect(self._x - 170, self._y, 170, length * 18))
                for i in range(start, len(self._units)):
                    text = pygame.font.SysFont('Arial', 17).render("{0} - {1}/{2}".
                                                                   format(type(self._units[i]).__name__,
                                                                          self._units[i].health,
                                                                          eval(type(self._units[i]).__name__).max_health),
                                                                   False, self.get_owner_color(i))
                    surface.blit(text, (self._x - 170, self._y + (ind * 16)))
                    ind += 1

        # tower draw
        if len(self._units) > 0 and isinstance(self._units[0], Tower):
            color = (0, 0, 0)
            if isinstance(self._units[0], BasicTower):
                color = (0, 255, 255)
            elif isinstance(self._units[0], Splash):
                color = (255, 0, 255)
            elif isinstance(self._units[0], Slow):
                color = (255, 255, 0)

            pygame.draw.rect(surface, self.get_owner_color(), pygame.Rect(self._x + self._width / 4 - self._width / 16,
                                                                          self._y + self._height / 4 - self._width / 16,
                                                                          self._width - self._width / 2 + self._width / 8,
                                                                          self._height - self._height / 2 + self._width / 8))

            pygame.draw.rect(surface, color, pygame.Rect(self._x + self._width / 4,
                                                         self._y + self._height / 4,
                                                         self._width - self._width / 2,
                                                         self._height - self._height / 2))
        # count of the soldiers on the tile
        if len(self._units) > 0 and (isinstance(self._units[0], Soldier)):
            surface.blit(self._font.render(str(len(self._units)), True, self.get_owner_color()),
                         (self._x + self._width / 24 * 10, self._y + self._width / 4))
        elif len(self._units) > 1 and self._is_castle:
            surface.blit(self._font.render(str(len(self._units) - 1), True, self.get_owner_color()),
                         (self._x + self._width / 24 * 10, self._y + self._width / 4))

        # barrack draw
        # pygame.draw.polygon(surface, (0, 0, 0), points=[(self._x + self._width/2,self._y + self._height/3),
        #                                               (self._x + self._width/4, self._y + self._height/3*2),
        #                                               (self._x + self._width/4*3,self._y + self._height/3 * 2)])

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

    def get_owner_color(self, index=0):
        if self._units[index].owner == self._game_ref.player_1:
            return 255, 0, 0
        elif self._units[index].owner == self._game_ref.player_2:
            return 0, 0, 255
        return 0, 0, 0

    @property
    def units(self):
        return self._units

    @property
    def font(self):
        return self._font
