from src.unit import *


class Soldier(Unit):
    def __init__(self, health, damage, stamina, tile, owner, x, y):
        super().__init__(health=health, damage=damage, tile=tile, owner=owner, x=x, y=y)
        self.current_stamina = stamina
        self._stamina = stamina
        self._alive = True
        self.path = None
        self.destination = None
        self._tile = tile
        self.game = tile.game_ref

    def move(self):
        if self.path and self.destination:
            if len(self.path) > 0 and self._current_stamina > 0:
                self._current_stamina -= 1
                next = self.path.pop(0)
                self._tile.units.remove(self)
                self._x = next[0]
                self._y = next[1]
                self._tile = self.game.map[self.x][self.y]
                self._tile.units.append(self)

                if self.tile == self.destination:
                    self.destination.units[0].hit(self.health)
                    self.tile.units.remove(self)
                    self.owner.units.remove(self)

    def take_damage(self, damage):
        self.change_health(damage)
        if self._health <= 0:
            self.alive = False
            self.owner.units.remove(self)
            self.tile.units.remove(self)

    @property
    def stamina(self):
        return self._stamina

    @property
    def current_stamina(self):
        return self._current_stamina

    @current_stamina.setter
    def current_stamina(self, value):
        self._current_stamina = value

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, change):
        self._alive = change


class BasicSoldier(Soldier):
    price = 100
    max_health = 100

    def __init__(self, tile, owner, x, y):
        super().__init__(health=100, damage=50, stamina=5, tile=tile, owner=owner, x=x, y=y)


class Climber(Soldier):
    price = 150
    max_health = 120

    def __init__(self, tile, owner, x, y):
        super().__init__(health=120, damage=50, stamina=5, tile=tile, owner=owner, x=x, y=y)


class Tank(Soldier):
    price = 150
    max_health = 200

    def __init__(self, tile, owner, x, y):
        super().__init__(health=200, damage=75, stamina=5, tile=tile, owner=owner, x=x, y=y)

    def attack(self, enemy):
        pass


class Suicide(Soldier):
    price = 200
    max_health = 500

    def __init__(self, tile, owner, x, y):
        super().__init__(health=500, damage=100, stamina=5, tile=tile, owner=owner, x=x, y=y)

    def attack(self, enemy):
        pass
