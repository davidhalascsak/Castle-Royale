from src.soldier import *
from src.tower import *
from src.castle import *


class Player:

    def __init__(self, name, health, x, y, game):
        self._name = name
        self._gold = 0
        self._units = [Castle(self, health, x, y)]
        self._castle_tile = None
        self._state = None
        self._to_simulate = []
        self._game = game

    def add_unit(self, unit):
        self._units.append(unit)
        if issubclass(type(unit), Soldier):
            unit.destination = self._game.not_active_player().castle_tile
        self._to_simulate.append(unit)

    def add_castle_tile(self, tile):
        self._castle_tile = tile

    def calculate_gold_bonus(self):
        sum = 50
        for unit in self._units:
            if issubclass(type(unit), Soldier):
                sum += 10
        return sum

    def simulate(self):
        stuck = True
        for unit in self._to_simulate:
            if issubclass(type(unit), Soldier):
                if issubclass(type(unit), Suicide) and (len(unit.destination.units) == 0 or unit.destination.units[0].is_in_ruins):
                    if self == self._game.player_1:
                        new_destination = self._game.player_2.closest_tower(unit.tile)
                    else:
                        new_destination = self._game.player_1.closest_tower(unit.tile)
                    if new_destination is None:
                        self._units.remove(unit)
                        self._to_simulate.remove(unit)
                        unit.tile.units.remove(unit)
                    else:
                        unit.destination = new_destination
                        unit.move()
                else:
                    unit.move()
                stuck = stuck and unit.stuck
            elif issubclass(type(unit), Tower):
                if not unit.is_in_ruins:
                    if self == self._game.player_1:
                        unit.shoot(self._game.player_2.units)
                    else:
                        unit.shoot(self._game.player_1.units)

        return stuck

    def reset_stamina(self):
        for unit in self._to_simulate:
            if issubclass(type(unit), Soldier):
                unit.last_stuck = False
                unit.current_stamina = unit.stamina
            elif issubclass(type(unit), Tower) and unit.is_in_ruins:
                unit.round_done = False

    @staticmethod
    def distance(tower, tile):
        x = tower.x
        y = tower.y
        distance = math.sqrt(pow(x - tile.x, 2) + pow(y - tile.y, 2))
        return distance

    def has_tower(self):
        for u in self._units:
            if issubclass(type(u), Tower):
                return True

        return False

    def closest_tower(self, tile):
        closest = None
        for u in self._units:
            if issubclass(type(u), Tower) and \
                not u.is_in_ruins and \
                (closest is None or self.distance(u.tile, tile) < self.distance(closest, tile)):
                        closest = u.tile
                        
        return closest

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, change):
        self._gold = change

    @property
    def name(self):
        return self._name

    @property
    def units(self):
        return self._units

    @property
    def castle_tile(self):
        return self._castle_tile

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    @property
    def to_simulate(self):
        return self._to_simulate

    @property
    def game(self):
        return self._game

    def get_castle_health(self):
        return self._units[0].health
