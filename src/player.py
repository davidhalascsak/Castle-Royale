from src.soldier import *
from src.tower import *
from src.castle import *


class Player:

    def __init__(self, name, health, x, y):
        self._name = name
        self._gold = 0
        self._units = [Castle(self, health, x, y)]
        self._castle_tile = None
        self._state = None

    def add_unit(self, unit):
        self._units.append(unit)

    def add_castle_tile(self, tile):
        self._castle_tile = tile

    def calculate_gold_bonus(self):
        sum = 0
        for unit in self._units:
            if issubclass(type(unit), Soldier):
                sum += 10
        return sum

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


