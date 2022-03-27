class Castle:
    def __init__(self, player, health, x, y):
        self._health = health
        self._x = x
        self._y = y
        self.owner = player

    @property
    def health(self):
        return self._health

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

