from src.player import Player
from src.tile import Tile
import random


class Game:
    def __init__(self):
        self.player_1 = None
        self.player_2 = None
        self.gold_increase = 0
        self.map = []
        self.now_playing = None

    def new_game(self, start_gold, gold_increase, name_1, name_2):
        self.gold_increase = gold_increase

        # Configure Players
        self.player_1 = Player(name_1)
        self.player_2 = Player(name_2)

        self.player_1.set_gold(start_gold)
        self.player_2.set_gold(start_gold)

        # Determine Starting Player
        self.now_playing = random.sample({self.player_1, self.player_2}, 1)[0]

        # Generate Map
        self.map = []
        for x in range(0, 26):
            self.map.append([])
            for y in range(0, 15):
                self.map[len(self.map) - 1].append(Tile(x, y))

    def load_game(self):
        pass

    def next_round(self):
        if self.now_playing == self.player_1:
            self.now_playing = self.player_2
        else:
            self.now_playing = self.player_1
        self.player_1.gold += (self.gold_increase + self.player_1.get_gold_bonus())
        self.player_2.gold += (self.gold_increase + self.player_2.get_gold_bonus())



