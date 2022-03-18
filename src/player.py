from src.soldier import *
import src.tower


class Player:

    def __init__(self, name):
        self._name = name
        self._gold = 0
        self._units = []  #structures volt
        self.state = None

    def add(self, unit):
        self._units.append(unit)

    def calculate_gold_bonus(self):
        sum = 0
        for unit in self._units:
            if issubclass(type(unit), Soldier):
                sum += 10
        return sum

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, change):
        self._gold = change

    @property
    def name(self):
        return self._name

