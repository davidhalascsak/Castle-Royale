from src.tile import Tile
from src.game import Game
from src.player import Player
from src.soldier import BasicSoldier

import pygame

pygame.init()

def test_calculate_gold_bonus():
    player_1 = Player("player_1", 150, 0, 0)
    player_1._gold = 1000
    t = Tile(Game(), 0, 0)
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    assert player_1.calculate_gold_bonus() == 10

    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    player_1._units.append(BasicSoldier(t, player_1, 0, 0))
    assert player_1.calculate_gold_bonus() == 30