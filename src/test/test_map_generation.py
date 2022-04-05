from src.tile import Tile
from src.game import Game
from src.mapgeneration import MapGeneration

import pygame

pygame.init()

good_result = [[1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
               
obs_matrix = [[0,0,0,0,0,0,0,0],
              [0,0,0,1,1,0,0,0],
              [0,0,1,1,1,1,0,0],
              [0,1,1,1,1,1,1,0],
              [0,0,1,1,1,1,0,0],
              [0,0,0,1,1,0,0,0],
              [0,0,0,0,0,0,0,0]]
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

def test_availability_matrix():
    availability_matrix = [[0 for i in range(0, 26)] for j in range(0, 14)]
    

    MapGeneration.setup_availability_matrix(availability_matrix, 0, 0, 26, 14)
    assert (availability_matrix == good_result)

def test_place_obstacle():
    game = setup_game()
    



    MapGeneration.place_obstacle(game, obs_matrix, 0, 0, "HILL") 
    assert (game._map[1][3].type == "HILL")
    assert (game._map[3][1].type == "HILL")
    
def test_check_placement_availability():
    game = setup_game()

    assert MapGeneration.check_placement_availability(game, obs_matrix, 0, 0)
    assert not MapGeneration.check_placement_availability(game, obs_matrix, 13, 25)

def test_available_tiles():
    game = setup_game()
    game._map[0][0]._is_castle = True

    assert MapGeneration.available_tiles(game) == good_result