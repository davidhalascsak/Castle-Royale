import pygame.event

from src.unit import *
import pygame


class Soldier(Unit):
    def __init__(self, health, max_health, damage, stamina, tile, owner, x, y):
        super().__init__(health=health, max_health=max_health, damage=damage, tile=tile, owner=owner, x=x, y=y)
        self.current_stamina = stamina
        self._stamina = stamina
        self._alive = True
        self.path = None
        self.destination = None
        self._tile = tile
        self._game = tile.game_ref
        self._last_time = 0
        self.waypoints = []
        self.stuck = False
        self.last_stuck = None

    def move(self):
        self.stuck = False
        if self._alive and self.destination:
            if pygame.time.get_ticks() - self.get_speed() > self._last_time:
                self._last_time = pygame.time.get_ticks()

                self.path = (False, [])
                if len(self.waypoints) > 0:
                    if issubclass(type(self), Suicide):
                        self.path = self._game.path_finder.isPath(self._tile.x, self._tile.y, self.waypoints[0][0],
                                                                  self.waypoints[0][1], True, issubclass(type(self), Climber),
                                                                  self.destination)
                    else:
                        self.path = self._game.path_finder.isPath(self._tile.x, self._tile.y,  self.waypoints[0][0],
                                                                  self.waypoints[0][1], True, issubclass(type(self), Climber))
                else:
                    if issubclass(type(self), Suicide):
                        self.path = self._game.path_finder.isPath(self._tile.x, self._tile.y, self.destination.x,
                                                                  self.destination.y, True, issubclass(type(self), Climber),
                                                                  self.destination)
                    else:
                        self.path = self._game.path_finder.isPath(self._tile.x, self._tile.y, self.destination.x,
                                                                  self.destination.y, True, issubclass(type(self), Climber))
                if self.path[0] and self._current_stamina > 0:
                    next = self.path[1][1]
                    if issubclass(type(self), Tank) and len(self._game._map[next[0]][next[1]].units) > 0:
                        for unit in self._game._map[next[0]][next[1]].units:
                            if unit.owner == self._game.other_player(self.owner) and issubclass(type(unit), Soldier):
                                unit.take_damage(self.damage)
                    
                    previous_tile = self._tile
                    self._current_stamina -= 1
                    self._tile.units.remove(self)
                    [self._x, self._y] = next
                    self._tile = self._game.map[self._x][self._y]
                    self._tile.units.append(self)

                    if issubclass(type(self), Tank) and len(previous_tile.units) > 0:
                        for unit in previous_tile.units:
                            if unit.owner == self._game.other_player(self.owner) and issubclass(type(unit), Soldier):
                                unit.take_damage(self.damage)
                    

                    if self._tile == self.destination:
                        self.destination.units[0].hit(self.damage)
                        self.tile.units.remove(self)
                        self.owner.units.remove(self)
                        self.owner.to_simulate.remove(self)

                    if len(self.waypoints) > 0 and next == self.waypoints[0]:
                        self.waypoints.pop(0)
                else:
                    self.stuck = True
                    self.last_stuck = self.stuck
            else:
                if self.last_stuck:
                    self.stuck = self.last_stuck
        else:
            self.stuck = True
            self.last_stuck = self.stuck

    @staticmethod
    def get_speed():
        return 800

    def take_damage(self, damage):
        if(self.health > 0):
            self.health -= damage
            if self.health <= 0:
                self.alive = False
                self._game.other_player(self.owner)._gold += 30
                if self in self.owner.units:
                    self.owner.units.remove(self)
                if self in self.tile.units:
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

    @property
    def game(self):
        return self._game

    @property
    def last_time(self):
        return self._last_time

    @property
    def tile(self):
        return self._tile


class BasicSoldier(Soldier):
    price = 100

    def __init__(self, tile, owner, x, y):
        super().__init__(health=100, max_health=100, damage=50, stamina=5, tile=tile, owner=owner, x=x, y=y)


class Climber(Soldier):
    price = 150

    def __init__(self, tile, owner, x, y):
        super().__init__(health=120, max_health=120, damage=50, stamina=5, tile=tile, owner=owner, x=x, y=y)

    def get_speed(self):
        return 1000


class Tank(Soldier):
    price = 150

    def __init__(self, tile, owner, x, y):
        super().__init__(health=200, max_health=200, damage=75, stamina=3, tile=tile, owner=owner, x=x, y=y)

    def get_speed(self):
        return 2000


class Suicide(Soldier):
    price = 20

    def __init__(self, tile, owner, x, y):
        super().__init__(health=500, max_health=500, damage=100, stamina=5, tile=tile, owner=owner, x=x, y=y)

    def get_speed(self):
        return 500
