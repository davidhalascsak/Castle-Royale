class Unit:
    def __init__(self, health, damage, tile, owner, x, y):
        self._health = health
        self._damage = damage
        self._tile = tile
        self._owner = owner
        self._x = x
        self._y = y

    def change_health(self, damage):
        new = self._health - damage
        self.health = new

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, change):
        self._health = change

    @property
    def damage(self):
        return self._damage

    @property
    def owner(self):
        return self._owner

    @property
    def tile(self):
        return self._tile

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @x.setter
    def x(self, new):
        self._x = new

    @y.setter
    def y(self, new):
        self._y = new


