from ast import AST
import ast
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
    game = setup_game()
    astar = AStar(game)
    game._map[0][5].type = "HILL"
    [availability, path] = astar.isPath(0, 0, 0, 10)

    # one obstacle in the way, normal unit
    astar.loadObstacles(False)
    assert astar.arr[0][5] == 1

    # one obstacle in the way, with special unit
    astar.loadObstacles(True)
    assert astar.arr[0][5] == 0

    # no obstacle
    game._map[0][5].type = "PLAIN"
    astar.loadObstacles(False)
    assert astar.arr[0][5] == 0

def test_is_path():
    game = setup_game()
    astar = AStar(game)
    [availability, path] = astar.isPath(0, 0, 0, 10)

    # empty test    
    arr = []
    for i in range(11):
        arr.append((0, i))

    assert availability
    
    assert path == arr

    # one obstacle, normal unit
    game = setup_game()
    astar = AStar(game)
    game._map[0][5].type = "HILL"
    [availability, path] = astar.isPath(0, 0, 0, 10)

    arr = []
    for i in range(5):
        arr.append((0, i))

    for i in range(4, 10):
        arr.append((1, i))

    arr.append((0,9))
    arr.append((0,10))

    assert availability
    
    assert path == arr

    # one obstacle, special unit
    game = setup_game()
    astar = AStar(game)
    game._map[0][5].type = "HILL"
    [availability, path] = astar.isPath(0, 0, 0, 10, True)

    arr = []
    for i in range(11):
        arr.append((0, i))


    assert availability
    
    assert path == arr

    # no available path, normal unit
    game = setup_game()
    astar = AStar(game)
    for i in range(14):
        game._map[i][5].type = "HILL"
    [availability, path] = astar.isPath(0, 0, 0, 10)


    assert not availability

    # no available path, special unit
    game = setup_game()
    astar = AStar(game)
    for i in range(14):
        game._map[i][5].type = "HILL"
    [availability, path] = astar.isPath(0, 0, 0, 10, True)


    assert availability