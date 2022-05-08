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
    return game

def test_next_round():
    game = setup_game()
    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 0, game)
    game._player_1 = player_1
    game._player_2 = player_2
    game._current_player = game._player_1
    game.next_round()
    assert game.current_player == game._player_2

def test_next_round_gold():
    game = setup_game()
    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 0, game)
    t = Tile(game, 1, 0)
    player_2._units.append(BasicSoldier(t, player_2, 0, 0))
    game._player_1 = player_1
    game._player_2 = player_2
    game._starting_player = game._player_1
    game._current_player = game._player_1
    game._player_2.gold = 1000
    game.next_round()
    game.next_round() # back to starting player
    
    assert game._player_2.gold == 1060

def test_next_round_is_ended():
    game = setup_game()
    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 0, game)
    game._player_2 = player_2
    player_1._units[0]._health = 0
    game._player_1 = player_1
    assert game._player_1.get_castle_health() == 0
    game.next_round()
    assert game.is_ended == True