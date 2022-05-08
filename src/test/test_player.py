from src.tile import Tile
from src.game import Game
from src.player import Player
from src.soldier import BasicSoldier

import pygame

pygame.init()


def test_calculate_gold_bonus_single():
    game = Game()
    player_1 = Player("player_1", 150, 0, 0, game)
    player_1._gold = 1000
    t = Tile(Game(), 0, 0)
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    assert player_1.calculate_gold_bonus() == 50 + 10

def test_calculate_gold_bonus_multiple():
    game = Game()
    player_1 = Player("player_1", 150, 0, 0, game)
    player_1._gold = 1000
    t = Tile(Game(), 0, 0)
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    assert player_1.calculate_gold_bonus() == 50 + 30

def test_reset_stamina():
    game = Game()

    player_1 = Player("player_1", 150, 0, 0, game)
    game._player_1 = player_1
    t = Tile(game, 0, 0)
    t.type = "PLAIN"
    t.add_castle(game._player_1.units[0])
    game._player_1.add_castle_tile(t)

    player_2 = Player("player_2", 150, 5, 5, game)
    game._player_2 = player_2
    t = Tile(game, 5, 5)
    t.type = "PLAIN"
    t.add_castle(game.player_2.units[0])
    game.player_2.add_castle_tile(t)


    t = Tile(Game(), 0, 0)
    player_1.add_unit(BasicSoldier(t, player_1, 0, 0))
    player_1._units[1].current_stamina = 0

    player_1.reset_stamina()

    assert player_1._units[1].current_stamina == player_1._units[1].stamina