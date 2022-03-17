import src.unit


class Soldier(src.unit.Unit):

    def __init__(self, health, damage, stamina, x, y, tile, owner):
        super().__init__(health=health, damage=damage, x=x, y=y, tile=tile, owner=owner)
        self._stamina = stamina
        self._alive = True

    def move(self, x, y):
        new_x = self.x + x
        new_y = self.y + y
        self.x = new_x
        self.y = new_y

    def attack(self, enemy):
        if enemy.health - self.damage > 0:
            enemy.change_health(self.damage)
        else:
            enemy.health = 0
            enemy.alive = False

    @property
    def stamina(self):
        return self._stamina

    @property
    def alive(self):
        return self._alive

    @alive.setter
    def alive(self, change):
        self._alive = change


class Basic(Soldier):
    price = 30

    def __init__(self, x, y, tile, owner):
        super().__init__(health=100, damage=50, stamina=100, x=x, y=y, tile=tile, owner=owner)


class Climber(Soldier):
    price = 30

    def __init__(self, x, y, tile, owner):
        super().__init__(health=120, damage=50, stamina=80, x=x, y=y, tile=tile, owner=owner)

    def move(self, x, y):
        pass


class Tank(Soldier):
    price = 20

    def __init__(self, x, y, tile, owner):
        super().__init__(health=200, damage=75, stamina=80, x=x, y=y, tile=tile, owner=owner)

    def attack(self, enemy):
        pass


class Suicide(Soldier):
    price = 30

    def __init__(self, x, y, tile, owner):
        super().__init__(health=500, damage=100, stamina=30, x=x, y=y, tile=tile, owner=owner)

    def attack(self, enemy):
        pass



