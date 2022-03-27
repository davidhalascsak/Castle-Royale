from src.player import Player
from src.tile import Tile
from src.castle import Castle
import random

terrain_type = {"DIRT", "MOSS", "MOUNT"}


class Game:

    def __init__(self):
        self._player_1 = None
        self._player_2 = None
        self._map = []
        self._starting_player = None
        self._current_player = None
        self.map_height = 14
        self.map_width = 26

    def new_game(self, start_gold, name_1, name_2):
        # Configure Players
        self._player_1 = Player(name_1, 1000, 0, self.map_height // 2)
        self._player_2 = Player(name_2, 1000, self.map_width-1, self.map_height // 2)

        self._player_1.gold = start_gold
        self._player_2.gold = start_gold

        # Determine Starting Player
        self._current_player = random.sample({self._player_1, self._player_2}, 1)[0]
        self._starting_player = self._current_player
        # Generate Map
        for x in range(0, self.map_width):
            self._map.append([])
            for y in range(0, self.map_height):
                t = Tile(self, x, y)
                t.type = random.sample(terrain_type, 1)[0]
                self._map[len(self._map) - 1].append(t)
                if self._player_1.units[0].x == x and self._player_1.units[0].y == y:
                    t.add_castle(self._player_1.units[0])
                    self._player_1.add_castle_tile(t)
                elif self._player_2.units[0].x == x and self._player_2.units[0].y == y:
                    t.add_castle(self._player_2.units[0])
                    self._player_2.add_castle_tile(t)

    def load_game(self):
        pass

    def save_game(self):
        pass

    def next_round(self):
        if self._current_player == self._player_1:
            self._current_player = self._player_2
        else:
            self._current_player = self._player_1
        if self._current_player == self._starting_player:
            self._player_1.gold = (self._player_1.gold + self._player_1.calculate_gold_bonus())
            self._player_2.gold = (self._player_2.gold + self._player_2.calculate_gold_bonus())
        self._player_1.state = None
        self._player_2.state = None

    @property
    def map(self):
        return self._map

    @property
    def player_1(self):
        return self._player_1

    @property
    def player_2(self):
        return self._player_2

    @property
    def current_player(self):
        return self._current_player





