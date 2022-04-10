from src.tile import Tile
from src.game import Game
from src.player import Player
from src.tower import Tower
from src.tower import BasicTower
from src.soldier import BasicSoldier

import pygame

pygame.init()

def setup_game():
    game = Game()

def test_attack():
    pass

def test_demolish():
    game = setup_game()
    t = Tile(game, 0, 0)
    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 25, game)
    tower = BasicTower(t, player_1, 1, 0)
    tower._is_in_ruins = True
    tower._clean_time = 1
    tower.demolish()
    assert tower._clean_time == 0

def test_basic_tower():
    '''game = setup_game()
    tower_tile = Tile(game, 1, 0)
    soldier_tile = Tile(game, 1, 1)
    player_1 = Player("player_1", 150, 0, 0)
    player_2 = Player("player_2", 150, 0, 25)
    soldier = BasicSoldier(soldier_tile, player_2, 1, 1)
    tower = BasicTower(tower_tile, player_1, 1, 0)
    tower.attack(player_2._units)
    assert soldier._alive == False'''
    pass

def test_splash():
    pass

def test_slow():
    pass