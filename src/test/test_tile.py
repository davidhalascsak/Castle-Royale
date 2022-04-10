from src.tile import Tile
from src.game import Game
from src.player import Player
from src.tower import Tower
from src.soldier import Soldier
from src.astar import AStar

import pygame

pygame.init()

def setup_game():
    game = Game()
    return game

def test_add_castle():
    game = setup_game()
    t = Tile(game, 0, 0)
    c = Player("player_1", 150, 0, 0, game)._units[0]
    t.add_castle(c)

    assert c == t._units[0]
    assert t._is_castle


def test_build():
    game = setup_game()
    game._path_finder = AStar(game)
    t = Tile(game, 1, 0)
    player_1 = Player("player_1", 150, 0, 0, game)

    # 0 gold
    t.build(player_1, "BasicTower")
    assert len(t._units) == 0

    assert player_1.gold == 0

    player_1._gold = 1000
    

    t.build(player_1, "BasicTower")
    assert issubclass(type(t._units[0]), Tower)

    assert player_1.gold == 970

def test_train():
    game = setup_game()
    t = Tile(game, 1, 0)
    player_1 = Player("player_1", 150, 0, 0, game)

    # 0 gold
    t.train(player_1, "BasicSoldier")
    assert len(t._units) == 0

    assert player_1.gold == 0

    player_1._gold = 1000

    t.train(player_1, "BasicSoldier")
    assert issubclass(type(t._units[0]), Soldier)

    assert player_1.gold == 900

