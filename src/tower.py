from src.unit import *


class Tower(Unit):
    def __init__(self, health, damage, range, clean_time, tile, owner, x, y):
        super().__init__(health=health, damage=damage, tile=tile, owner=owner, x=x, y=y)
        self._range = range
        self._clean_time = clean_time
        self._is_in_ruins = False
        self._is_ready_to_demolish = False

    def upgrade(self):
        pass

    def demolish(self):
        if self._is_in_ruins is True:
            if self._clean_time - 1 >= 0:
                self._clean_time -= 1
            else:
                self._is_ready_to_demolish = True

    def shoot(self):
        pass

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
    price = 30

    def __init__(self, tile, owner, x, y):
        super().__init__(health=5000, damage=20, range=3, clean_time=2, tile=tile, owner=owner, x=x, y=y)

    def shoot(self):
        pass


class Slow(Tower):
    price = 30

    def __init__(self, tile, owner, x, y):
        super().__init__(health=5000, damage=50, range=2, clean_time=2, tile=tile, owner=owner, x=x, y=y)

    def shoot(self):
        pass
