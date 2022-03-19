class Castle:
    def __init__(self, health, x, y):
        self._health = health
        self._x = x
        self._y = y

    @property
    def health(self):
        return self._health

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

