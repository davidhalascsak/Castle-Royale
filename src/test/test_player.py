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
    assert player_1.calculate_gold_bonus() == 10

def test_calculate_gold_bonus_multiple():
    game = Game()
    player_1 = Player("player_1", 150, 0, 0, game)
    player_1._gold = 1000
    t = Tile(Game(), 0, 0)
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    assert player_1.calculate_gold_bonus() == 30

def test_reset_stamina():
    game = Game()
    player_1 = Player("player_1", 150, 0, 0, game)
    t = Tile(Game(), 0, 0)
    player_1.add_unit(BasicSoldier(t, player_1, 0, 0))
    player_1._units[1].current_stamina = 0

    player_1.reset_stamina()

    assert player_1._units[1].current_stamina == player_1._units[1].stamina