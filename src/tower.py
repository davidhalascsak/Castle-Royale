from src.unit import *
from src.soldier import *
import math


class Tower(Unit):
    def __init__(self, health, damage, range, clean_time, tile, owner, x, y):
        super().__init__(health=health, damage=damage, tile=tile, owner=owner, x=x, y=y)
        self._range = range
        self._clean_time = clean_time
        self._is_in_ruins = False
        self._is_ready_to_demolish = False
        self._locked_unit = None

    def upgrade(self):
        pass

    def demolish(self):
        if self._is_in_ruins is True:
            if self._clean_time - 1 >= 0:
                self._clean_time -= 1
            else:
                self._is_ready_to_demolish = True

    def distance(self, unit):
        x = unit.x
        y = unit.y
        distance = math.sqrt(pow(x - self._x, 2) + pow(y - self._y, 2))
        return distance

    def shoot(self, units):
        if self._locked_unit is not None and self.distance(self._locked_unit) > self._range:
            self._locked_unit = None
        if self._locked_unit is None:
            for unit in units:
                if issubclass(type(unit), Soldier):
                    if self._locked_unit is None and self.distance(unit) <= self._range:
                        self._locked_unit = unit
                    elif self._locked_unit is not None and self.distance(unit) < self.distance(self._locked_unit):
                        self._locked_unit = unit

        if self._locked_unit is not None:
            self._locked_unit.take_damage(self._damage)
            if not self._locked_unit.alive:
                self._locked_unit = None

    @property
    def range(self):
        return self._range

    @property
    def clean_time(self):
        return self._clean_time

    @property
    def range(self):
        return self._range

    @property
    def is_in_ruins(self):
        return self._is_in_ruins

    @is_in_ruins.setter
    def is_in_ruins(self, new):
        self._is_in_ruins = new

    @property
    def is_ready_to_demolish(self):
        return self._is_ready_to_demolish

    @is_ready_to_demolish.setter
    def is_ready_to_demolish(self, new):
        self._is_ready_to_demolish = new


class BasicTower(Tower):
    price = 30

    def __init__(self, tile, owner, x, y):
        super().__init__(health=5000, damage=50, range=2, clean_time=2, tile=tile, owner=owner, x=x, y=y)


class Splash(Tower):
    price = 40

    def __init__(self, tile, owner, x, y):
        super().__init__(health=5000, damage=25, range=3, clean_time=2, tile=tile, owner=owner, x=x, y=y)

    def shoot(self, units):
        locked_units = []
        for unit in units:
            if issubclass(type(unit), Soldier):
                if self.distance(unit) < self._range:
                    locked_units += unit

        for unit in locked_units:
            unit.take_damage(self._damage)


class Slow(Tower):
    price = 30

    def __init__(self, tile, owner, x, y):
        super().__init__(health=5000, damage=40, range=3, clean_time=2, tile=tile, owner=owner, x=x, y=y)
