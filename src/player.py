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
        self._to_simulate.append(unit)

    def add_castle_tile(self, tile):
        self._castle_tile = tile

    def calculate_gold_bonus(self):
        sum = 0
        for unit in self._units:
            if issubclass(type(unit), Soldier):
                sum += 10
        return sum

    def simulate(self):
        count = 0
        for unit in self._to_simulate:
            if issubclass(type(unit), Soldier):
                count += unit.move()
            elif issubclass(type(unit), Tower):
                if self == self._game.player_1:
                    count += unit.shoot(self._game.player_2.units)
                else:
                    count += unit.shoot(self._game.player_1.units)
        return count > 0

    def reset_stamina(self):
        for unit in self._to_simulate:
            if issubclass(type(unit), Soldier):
                unit.current_stamina = unit.stamina

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

    def get_castle_health(self):
        return self._units[0].health


