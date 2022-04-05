from src.tile import Tile
from src.game import Game
from src.player import Player
from src.tower import Tower
from src.soldier import BasicSoldier
from src.astar import AStar

import pygame

pygame.init()

def setup_game():
    game = Game()
    game._map = []
    height = 14
    width = 26
    for x in range(0, height):
            game._map.append([])
            for y in range(0, width):
                t = Tile(game, x, y)
                t.type = "PLAIN"
                game._map[x].append(t)
    return game
#TO-DO
def test_load_obstacles():
    pass

def test_is_path():
    pass
