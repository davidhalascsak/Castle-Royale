import src.unit


class Soldier(src.unit.Unit):

    def __init__(self, health, damage, stamina, price, x, y):
        super().__init__(health=health, damage=damage, price=price, x=x, y=y)
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

    def __init__(self, x, y):
        super().__init__(health=100, damage=50, stamina=100, price=30, x=x, y=y)


class Climber(Soldier):

    def __init__(self, x, y):
        super().__init__(health=120, damage=50, stamina=80, price=30, x=x, y=y)

    def move(self, x, y):
        pass


class Tank(Soldier):

    def __init__(self, x, y):
        super().__init__(health=200, damage=75, stamina=80, price=50, x=x, y=y)

    def attack(self, enemy):
        pass


class Suicide(Soldier):

    def __init__(self, x, y):
        super().__init__(health=500, damage=100, stamina=30, price=80, x=x, y=y)

    def attack(self, enemy):
        pass



