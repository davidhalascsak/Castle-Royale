from src.player import Player
from src.tile import Tile
from src.castle import Castle
from src.mapgeneration import MapGeneration
import random
from src.astar import AStar
from src.soldier import Soldier
from src.core import *

terrain_type = {"PLAIN", "LAKE", "HILL"}


class Game:

    def __init__(self):
        self._player_1 = None
        self._player_2 = None
        self._map = []
        self._starting_player = None
        self._current_player = None
        self.map_height = 14
        self.map_width = 26
        self._is_ended = False
        self._winner = None
        self._path_finder = None
        self._start_simulation = False
        self.selected_tile = None
        self.current_tile = None

    def simulate(self):
        if self._start_simulation:
            player1_stuck = self._player_1.simulate()
            player2_stuck = self._player_2.simulate()
            self._start_simulation = not (player1_stuck and player2_stuck)
            # for u in self._player_1.to_simulate:
            #     u.print_stats()

            # self._start_simulation = False
    def reset_stats(self):
        self._player_1.reset_stamina()
        self._player_2.reset_stamina()

    def select_current_tile(self):
        if tile_has_soldier(self.current_tile):
            if self.selected_tile:
                self.selected_tile.selected = False

            self.selected_tile = self.current_tile
            self.selected_tile.selected = True

    def add_waypoint(self):
        if self.selected_tile:
            for unit in self.selected_tile.units:
                if issubclass(type(unit), Soldier) and hasattr(unit, 'waypoints') and isinstance(unit.waypoints, list) and self.current_tile and (self.current_tile.type == "PLAIN" or tile_all_climber(self.selected_tile)):
                    unit.waypoints.append((self.current_tile.x, self.current_tile.y))

    def reset_waypoint(self):
        if self.selected_tile:
            for unit in self.selected_tile.units:
                unit.waypoints = []

    def new_game(self, start_gold, name_1, name_2):
        # Configure Players
        self._player_1 = Player(name_1, 10, self.map_height // 2, 0, self)
        self._player_2 = Player(name_2, 10, self.map_height // 2, self.map_width-1, self)

        self._player_1.gold = start_gold
        self._player_2.gold = start_gold

        # Determine Starting Player
        # self._current_player = random.sample({self._player_1, self._player_2}, 1)[0]
        self._current_player = self._player_1
        self._starting_player = self._current_player
        # Generate Map
        for x in range(0, self.map_height):
            self._map.append([])
            for y in range(0, self.map_width):
                t = Tile(self, x, y)
                t.type = "PLAIN"
                self._map[x].append(t)
                if self._player_1.units[0].x == x and self._player_1.units[0].y == y:
                    t.add_castle(self._player_1.units[0])
                    self._player_1.add_castle_tile(t)
                elif self._player_2.units[0].x == x and self._player_2.units[0].y == y:
                    t.add_castle(self._player_2.units[0])
                    self._player_2.add_castle_tile(t)
        MapGeneration.generate_map(self)
        self._path_finder = AStar(self)

    def load_game(self):
        pass

    def save_game(self):
        pass

    def other_player(self):
        if self._current_player == self._player_1:
            return self._player_2
        else:
            return self._player_1

    def next_round(self):
        self._player_1.state = None
        self._player_2.state = None

        if self._current_player == self._player_1:
            self._current_player = self._player_2
        else:
            self._current_player = self._player_1
        if self._current_player == self._starting_player:
            self._player_1.gold = (self._player_1.gold + self._player_1.calculate_gold_bonus())
            self._player_2.gold = (self._player_2.gold + self._player_2.calculate_gold_bonus())
            self.reset_stats()
            self._start_simulation = True

        self._is_ended = not (self._player_1.get_castle_health() > 0 and self._player_2.get_castle_health())

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

    @property
    def starting_player(self):
        return self._starting_player

    @property
    def is_ended(self):
        return self._is_ended

    @property
    def winner(self):
        return self._winner

    @property
    def path_finder(self):
        return self._path_finder

    @property
    def start_simulation(self):
        return self._start_simulation

    @start_simulation.setter
    def start_simulation(self, value):
        self._start_simulation = value






