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
            "PLAIN": (161, 146, 101),
            "LAKE": (13, 64, 18),
            "HILL": (120, 125, 123)
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
                self._game_ref.path_finder.set_obstacle(self.x, self.y, 1)
                if self._game_ref.path_finder.isPath(7, 0, 7, 25, False)[0]:
                    print(self._game_ref.path_finder.isPath(7, 0, 7, 25)[0])
                    player.gold = (player.gold - unit_price)
                    unit = eval(type)(self, player, self.x, self.y)
                    player.add_unit(unit)
                    self._units.append(unit)
                else:
                    self._game_ref.path_finder.set_obstacle(self.x, self.y, 0)

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
            pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(self._y, self._x, self._width, self._height))
        else:
            pygame.draw.rect(surface, self.get_color(), pygame.Rect(self._y, self._x, self._width, self._height))
        # pygame.display.flip()

    def draw_buildings_and_soldiers(self, surface):
        # tower draw
        if len(self._units) > 0 and isinstance(self._units[0], Tower):
            color = (0, 0, 0)
            if isinstance(self._units[0], BasicTower):
                color = (0, 255, 255)
            elif isinstance(self._units[0], Splash):
                color = (255, 0, 255)
            elif isinstance(self._units[0], Slow):
                color = (255, 255, 0)

            pygame.draw.rect(surface, self.get_owner_color(), pygame.Rect(self._y + self._width / 4 - self._width / 16,
                                                                          self._x + self._height / 4 - self._width / 16,
                                                                          self._width - self._width / 2 + self._width / 8,
                                                                          self._height - self._height / 2 + self._width / 8))

            pygame.draw.rect(surface, color, pygame.Rect(self._y + self._width / 4,
                                                         self._x + self._height / 4,
                                                         self._width - self._width / 2,
                                                         self._height - self._height / 2))
        # count of the soldiers on the tile
        if len(self._units) > 0 and (isinstance(self._units[0], Soldier)):
            surface.blit(self._font.render(str(len(self._units)), True, self.get_owner_color()),
                         (self._y + self._width / 24 * 10, self._x + self._width / 4))
        elif len(self._units) > 1 and self._is_castle:
            surface.blit(self._font.render(str(len(self._units) - 1), True, self.get_owner_color()),
                         (self._y + self._width / 24 * 10, self._x + self._width / 4))

        # barrack draw
        # pygame.draw.polygon(surface, (0, 0, 0), points=[(self._x + self._width/2,self._y + self._height/3),
        #                                               (self._x + self._width/4, self._y + self._height/3*2),
        #                                               (self._x + self._width/4*3,self._y + self._height/3 * 2)])

    def draw_context_menu_for_tiles(self, surface):
        # context menu for soldiers on a tile
        if self._hover and ((len(self._units) > 0 and issubclass(type(self._units[0]), Soldier)) or
                            (self._is_castle and len(self._units) > 1 and issubclass(type(self._units[1]), Soldier))):
            start = 0
            ind = 0
            length = len(self._units)
            if self._is_castle:
                start = 1
                length -= 1
            if self._y > 600:
                horizontal_alignment = -122
            else:
                horizontal_alignment = 0
            if self._x > 330:
                vertical_alignment = - length * 18
            else:
                vertical_alignment = 48
            pygame.draw.rect(surface, pygame.Color(0, 0, 0),
                             pygame.Rect(self._y + horizontal_alignment, self._x + vertical_alignment, 170,
                                         length * 18))
            for i in range(start, len(self._units)):
                text = pygame.font.SysFont('Arial', 17).render("{0} - {1}/{2}".
                                                               format(type(self._units[i]).__name__,
                                                                      self._units[i].health,
                                                                      eval(type(self._units[i]).__name__).max_health),
                                                               False, self.get_owner_color(i))
                surface.blit(text, (self._y + horizontal_alignment, self._x + vertical_alignment + (ind * 16)))
                ind += 1

    def is_over(self, pos):
        if self._y < pos[0] < self._y + self._width:
            if self._x < pos[1] < self._x + self._height:
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

    @property
    def is_castle(self):
        return self._is_castle
