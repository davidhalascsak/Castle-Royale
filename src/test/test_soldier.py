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

    player_2 = Player("player_2", 150, 0, 1, game)
    game._player_2 = player_2
    t = Tile(game, 0, 1)
    t.type = "PLAIN"
    t.add_castle(game.player_2.units[0])
    game.player_2.add_castle_tile(t)

    soldier_1 = BasicSoldier(tile, player_1, 0, 0)
    player_1.add_unit(soldier_1)
    tile._units.append(soldier_1)
    soldier_1._last_time = pygame.time.get_ticks() - soldier_1.get_speed() - 200
    soldier_1.current_stamina = 5
    
    game._path_finder = AStar(game)
    [availability, path] = game.path_finder.isPath(0, 0, 0, 10, True)
    soldier_1.path = path
    soldier_1.path.pop(0)
    soldier_1.destination  = player_2.castle_tile
    soldier_1.move()

    assert soldier_1._x == 0 and soldier_1._y == 1

def test_castle_dmg():
    game = setup_game()
    game._path_finder = AStar(game)

    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 10, game)

    game._player_1 = player_1
    game._player_2 = player_2

    player_2_tile = game._map[0][10]
    player_2_tile.units.append(game._player_2.units[0])
    player_2_tile.add_castle(player_2_tile.units[0])
    game._player_2.add_castle_tile(player_2_tile)

    tile_2 = game._map[0][9]

    soldier_1 = BasicSoldier(tile_2, player_1, 0, 9)
    player_1.add_unit(soldier_1)
    soldier_1.current_stamina = 5
    soldier_1._last_time = pygame.time.get_ticks() - soldier_1.get_speed() - 1

    tile_2.units.append(soldier_1)
    
    soldier_1.destination = player_2_tile
    soldier_1._tile = tile_2

    damage = soldier_1.damage

    soldier_1.move()

    assert game._player_2.get_castle_health() == 150-damage

def test_take_damage():
    game = setup_game()
    game._path_finder = AStar(game)

    player_1 = Player("player_1", 150, 0, 0, game)
    game._player_1 = player_1

    player_1_tile = game._map[0][10]
    player_1_tile.units.append(game._player_1.units[0])
    player_1_tile.add_castle(player_1_tile.units[0])
    game._player_1.add_castle_tile(player_1_tile)

    tile = game._map[0][0]
    soldier_1 = BasicSoldier(tile, player_1, 0, 0)
    player_1.add_unit(soldier_1)
    tile.units.append(soldier_1)

    health = soldier_1.health

    soldier_1.take_damage(50)

    assert soldier_1.health == health-50

    

def test_take_damage_alive():
    game = setup_game()
    game._path_finder = AStar(game)

    player_1 = Player("player_1", 150, 0, 0, game)
    game._player_1 = player_1

    player_1_tile = game._map[0][10]
    player_1_tile.units.append(game._player_1.units[0])
    player_1_tile.add_castle(player_1_tile.units[0])
    game._player_1.add_castle_tile(player_1_tile)

    player_2 = Player("player_2", 150, 1, 1, game)
    game._player_2 = player_2

    tile = game._map[0][0]
    soldier_1 = BasicSoldier(tile, player_1, 0, 0)
    player_1.add_unit(soldier_1)
    tile.units.append(soldier_1)
    
    soldier_1.take_damage(100)

    assert not soldier_1._alive

#TO-DO
def test_tank():
    pass

def test_suicide():
    pass