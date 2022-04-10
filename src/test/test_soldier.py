from src.castle import Castle
from src.tile import Tile
from src.game import Game
from src.player import Player
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

def test_move():
    game = setup_game()
    player_1 = Player("player_1", 150, 0, 0, game)
    tile = Tile(game, 0, 0)
    soldier_1 = BasicSoldier(tile, player_1, 0, 0)
    player_1.units.append(soldier_1)
    tile._units.append(soldier_1)
    soldier_1._last_time = pygame.time.get_ticks() - soldier_1.get_speed() - 200
    soldier_1.current_stamina = 5
    
    astar = AStar(game)
    [availability, path] = astar.isPath(0, 0, 0, 10)
    soldier_1.path = path
    soldier_1.path.pop(0)
    soldier_1.destination = (0, 10)
    soldier_1.move()

    assert soldier_1._x == 0 and soldier_1._y == 1

def test_castle_dmg():
    game = setup_game()
    player_1 = Player("player_1", 150, 0, 0, game)
    tile = Tile(game, 0, 0)
    soldier_1 = BasicSoldier(tile, player_1, 0, 0)
    player_1.units.append(soldier_1)
    tile._units.append(soldier_1)
    soldier_1._last_time = pygame.time.get_ticks() - soldier_1.get_speed() - 200
    soldier_1.current_stamina = 5
    player_2 = Player("player_2", 150, 0, 10, game)
    player_2_castle = Castle(player_2, 100, 0, 10)
    tile_3 = Tile(game, 0, 10)
    tile_3.units.append(player_2_castle)
    tile_3._is_castle = True

    tile_2 = Tile(game, 0, 9)
    tile_2.units.append(soldier_1)
    soldier_1._last_time = pygame.time.get_ticks() - soldier_1.get_speed() - 1
    soldier_1.destination = tile_3
    soldier_1._tile = tile_2
    soldier_1.path = [(0, 10)]
    game._map[0][9] = tile_2
    game._map[0][10] = tile_3

    damage = soldier_1.damage

    soldier_1.move()

    assert player_2_castle._health == 100-damage

def test_take_damage():
    game = setup_game()
    player_1 = Player("player_1", 150, 0, 0, game)
    tile = Tile(game, 0, 0)
    soldier_1 = BasicSoldier(tile, player_1, 0, 0)
    player_1._units.append(soldier_1)
    tile.units.append(soldier_1)

    health = soldier_1.health

    soldier_1.take_damage(50)

    assert soldier_1.health == health-50

    

def test_take_damage_alive():
    game = setup_game()
    player_1 = Player("player_1", 150, 0, 0, game)
    tile = Tile(game, 0, 0)
    soldier_1 = BasicSoldier(tile, player_1, 0, 0)
    player_1._units.append(soldier_1)
    tile.units.append(soldier_1)
    soldier_1.take_damage(100)

    assert not soldier_1._alive

#TO-DO
def test_tank():
    pass

def test_suicide():
    pass