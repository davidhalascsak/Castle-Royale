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
            unit.destination = self._game.other_player().castle_tile
            # print(unit.destination)
            # unit.waypoints.append((0, 0))
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
        pass
        # # count = 0
        # # print(self)
        # # print(self._to_simulate)
        stuck = True
        for unit in self._to_simulate:
            if issubclass(type(unit), Soldier):
                unit.move()
                stuck = stuck and unit.stuck
                # pass
                # count += unit.move()
            # elif issubclass(type(unit), Tower):
            #     if self == self._game.player_1:
            #         pass
            #         # count += unit.shoot(self._game.player_2.units)
            #     else:
            #         pass
            #         # count += unit.shoot(self._game.player_1.units)
        #
        # # print(stuck)
        return stuck

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

    @property
    def game(self):
        return self._game

    def get_castle_health(self):
        return self._units[0].health


