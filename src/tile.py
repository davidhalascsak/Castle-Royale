import pygame
import random
from src.castle import *
from src.soldier import *
from src.tower import *


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), 1)
    surface.blit(shape_surf, rect)


class Tile:

    def __init__(self, game, pos_x, pos_y):
        self.game_ref = game
        self.x = pos_x
        self.y = pos_y
        self._x = pos_x * 48
        self._y = pos_y * 48
        self._width = 48
        self._height = 48
        self._is_castle = False
        self._has_building = False
        self._units = []
        self.type = None
        self._selected = None
        self._waypoint = None
        self._hover = False

    def add_castle(self, castle):
        self._units.append(castle)
        self._is_castle = True
        self._has_building = True

    def build(self, player, type):
        if len(self._units) == 0 and self.type == "PLAIN":
            unit_price = eval(type).price
            if (player.gold - unit_price) >= 0:
                self.game_ref.path_finder.loadObstacles(False, None)
                self.game_ref.path_finder.set_obstacle(self.x, self.y, 1)
                if self.game_ref.path_finder.isPath(7, 0, 7, 25, False)[0]:
                    player.gold = (player.gold - unit_price)
                    unit = eval(type)(self, player, self.x, self.y)
                    player.add_unit(unit)
                    self._units.append(unit)
                    self._has_building = True
                else:
                    self.game_ref.path_finder.set_obstacle(self.x, self.y, 0)

    def upgrade_tower(self):
        unit = None
        for u in self._units:
            if issubclass(type(u), Tower):
                unit = u

        unit.upgrade()

    def demolish_tower(self):
        unit = None
        for u in self._units:
            if issubclass(type(u), Tower):
                unit = u
        self.game_ref.path_finder.set_obstacle(self.x, self.y, 0)
        unit.demolish()

    def remove_tower_ruin(self):
        if self._units[0].owner == self.game_ref._current_player:
            unit = None
            for u in self._units:
                if issubclass(type(u), Tower):
                    unit = u

            unit.remove_ruins()

    def train(self, player, soldier):
        count = 0
        for unit in self._units:
            if issubclass(type(unit), Soldier):
                count += 1

        if count < 5:
            unit_price = eval(soldier).price
            if (player.gold - unit_price) >= 0:
                if soldier != "Suicide":
                    player.gold = (player.gold - unit_price)
                    unit = eval(soldier)(self, player, self.x, self.y)
                    player.add_unit(unit)
                    self._units.append(unit)
                    unit.destination = player.game.not_active_player().castle_tile
                else:
                    if self.game_ref.player_1 == player:
                        if self.game_ref.player_2.has_tower():
                            player.gold = (player.gold - unit_price)
                            unit = eval(soldier)(self, player, self.x, self.y)
                            player.add_unit(unit)
                            self._units.append(unit)
                            unit.destination = self.game_ref.player_2.closest_tower(player.castle_tile)
                    elif self.game_ref.player_2 == player:
                        if self.game_ref.player_1.has_tower():
                            player.gold = (player.gold - unit_price)
                            unit = eval(soldier)(self, player, self.x, self.y)
                            player.add_unit(unit)
                            self._units.append(unit)
                            unit.destination = self.game_ref.player_1.closest_tower(player.castle_tile)


    def is_over(self, pos):
        if self._y < pos[0] < self._y + self._width:
            if self._x < pos[1] < self._x + self._height:
                self._hover = True
                return True
        self._hover = False

    @property
    def units(self):
        return self._units

    @property
    def is_castle(self):
        return self._is_castle

    @property
    def has_building(self):
        return self._has_building

    @has_building.setter
    def has_building(self, new_value):
        self._has_building = new_value