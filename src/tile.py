import pygame
import random
import src.tower
from src.soldier import *
from src.tower import *


class Tile:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self._x = pos_x * 48
        self._y = pos_y * 48
        self._width = 48
        self._height = 48
        self.type = None
        # self.r = random.randint(0, 255)
        # self.g = random.randint(0, 255)
        # self.b = random.randint(0, 255)
        self._color = {
            None: (255, 255, 255),
            "DIRT": (161, 146, 101),
            "MOSS": (13, 64, 18),
            "MOUNT": (120, 125, 123)
        }
        self._hover_color = (48, 241, 255)
        self._hover = False
        #self._structures = []
        self._units = []
        self.font = pygame.font.SysFont('Arial', 20)

    def build(self, player, type):
        if len(self._units) == 0:
            unit_price = eval("src.tower." + type).price
            if (player.gold - unit_price) > 0:
                player.gold = (player.gold - unit_price)
                unit = eval("src.tower." + type)(self.x, self.y, self, player)
                player.add(unit)
                self._units.append(unit)
                print(unit.__dict__)

    def draw(self, surface):
        pygame.draw.rect(surface, self.get_color(), pygame.Rect(self._x, self._y, self._width, self._height))
        # pygame.display.flip()
        if self._hover and len(self._units) > 0 and issubclass(type(self._units[0]), Soldier):
            basic = 0
            climber = 0
            tank = 0
            suicide = 0
            for unit in self._units:
                if isinstance(unit, Basic_Soldier):
                    basic += 1
                elif isinstance(unit, Climber):
                    climber += 1
                elif isinstance(unit, Tank):
                    tank += 1
                elif isinstance(unit, Suicide):
                    suicide += 1
            surface.blit(self.font.render(str(basic), True, (0,0,0)), (self._x, self._y-self._width/10))
            surface.blit(self.font.render(str(climber), True, (0,0,0)), (self._x+self._width/16*13, self._y-self._width/10))
            surface.blit(self.font.render(str(tank), True, (0,0,0)), (self._x, self._y-self._width/10+self._width/4*2.7))
            surface.blit(self.font.render(str(suicide), True, (0,0,0)), (self._x+self._width/16*13, self._y-self._width/10+self._width/4*2.7))
        if len(self._units) > 0 and isinstance(self._units[0], Tower):
            color = (0,0,0)
            if isinstance(self._units[0], Basic_Tower):
                    color = (0,255,255)
            elif isinstance(self._units[0], Splash):
                color = (255,0,255)
            elif isinstance(self._units[0], Slow):
                color = (255,255,0)

            pygame.draw.rect(surface, self.get_owner_color(), pygame.Rect(self._x + self._width / 4 - self._width / 16,
                                                                          self._y + self._height / 4 - self._width / 16,
                                                                          self._width - self._width / 2 + self._width / 8,
                                                                          self._height - self._height / 2 + self._width / 8))

            pygame.draw.rect(surface, color, pygame.Rect(self._x + self._width / 4,
                                                         self._y + self._height / 4,
                                                         self._width - self._width / 2,
                                                         self._height - self._height / 2))

        if len(self._units) > 0 and isinstance(self._units[0], Soldier):
            print(self._units[0]._owner)
            surface.blit(self.font.render(str(len(self._units)), True, self.get_owner_color()), (self._x+self._width/24*10, self._y+self._width/4))

        # Barakk kirajzolás
        # pygame.draw.polygon(surface, (0,0,0), points=[(self._x + self._width/2,self._y + self._height/3), (self._x + self._width/4, self._y + self._height/3*2), (self._x + self._width/4*3,self._y + self._height/3 * 2)])

    def is_over(self, pos):
        if self._x < pos[0] < self._x + self._width:
            if self._y < pos[1] < self._y + self._height:
                self._hover = True
                return True
        self._hover = False

    def get_color(self):
        if self._hover:
            return self._hover_color
        else:
            return self._color[self.type]

    def get_owner_color(self):
        if self._units[0]._owner == "Player1":
            return (255,0,0)
        elif self._units[0]._owner == "Player2":
            return (0,0,255)
        return (0,0,0)
