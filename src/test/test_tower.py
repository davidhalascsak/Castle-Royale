from src.tile import Tile
from src.game import Game
from src.player import Player
from src.tower import Splash
from src.tower import BasicTower
from src.soldier import BasicSoldier
from src.soldier import Tank
from src.soldier import Climber

import pygame

pygame.init()

def setup_game():
    game = Game()
    return game

def test_demolish():
    game = setup_game()
    t = Tile(game, 0, 0)
    player_1 = Player("player_1", 150, 0, 0, game)
    tower = BasicTower(t, player_1, 1, 0)
    tower._is_in_ruins = True
    tower._clean_time = 1
    player_1.add_unit(tower)
    t.units.append(tower)
    tower.demolish()
    
    assert tower._clean_time == 1

def test_basic_tower_dmg():
    game = setup_game()
    tower_tile = Tile(game, 1, 1)
    soldier_tile = Tile(game, 2, 1)
    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 25, game)
    soldier = BasicSoldier(soldier_tile, player_2, 2, 1)
    tower = BasicTower(tower_tile, player_1, 1, 1)
    tower._last_time = pygame.time.get_ticks() - tower.get_speed() - 1

    # Damage check
    player_2._units.append(soldier)
    health = soldier.health

    tower.shoot(player_2._units)

    assert soldier.health == health-tower.damage

def test_basic_tower_death():
    game = setup_game()
    tower_tile = Tile(game, 1, 1)
    soldier_tile = Tile(game, 2, 1)
    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 25, game)
    soldier = BasicSoldier(soldier_tile, player_2, 2, 1)
    tower = BasicTower(tower_tile, player_1, 1, 1)
    tower._last_time = pygame.time.get_ticks() - tower.get_speed() - 1
    player_2._units.append(soldier)

    soldier._alive = False
    player_2._units.remove(soldier)

    tower.shoot(player_2._units)

    assert tower._locked_unit is None

def test_basic_tower_rng():
    game = setup_game()
    tower_tile = Tile(game, 1, 1)
    soldier_tile = Tile(game, 2, 1)
    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 25, game)
    soldier = BasicSoldier(soldier_tile, player_2, 2, 1)
    tower = BasicTower(tower_tile, player_1, 1, 1)
    tower._last_time = pygame.time.get_ticks() - tower.get_speed() - 1
    player_2._units.append(soldier)

    [soldier.x, soldier.y] = (10,10)

    tower.shoot(player_2._units)

    assert tower._locked_unit == None


def test_splash():
    game = setup_game()

    tower_tile = Tile(game, 1, 1)
    soldier_1_tile = Tile(game, 2, 1)
    soldier_2_tile = Tile(game, 1, 2)
    soldier_3_tile = Tile(game, 2, 2)

    player_1 = Player("player_1", 150, 0, 0, game)
    player_2 = Player("player_2", 150, 0, 25, game)

    soldier_1 = BasicSoldier(soldier_1_tile, player_2, 2, 1)
    soldier_2 = Tank(soldier_2_tile, player_2, 1, 2)
    soldier_3 = Climber(soldier_3_tile, player_2, 2, 2)

    player_2._units.append(soldier_1)
    player_2._units.append(soldier_2)
    player_2._units.append(soldier_3)

    tower = Splash(tower_tile, player_1, 1, 1)
    tower._last_time = pygame.time.get_ticks() - tower.get_speed() - 1

    soldier_1_health = soldier_1.health
    soldier_2_health = soldier_2.health
    soldier_3_health = soldier_3.health

    tower.shoot(player_2._units)

    assert soldier_1.health == soldier_1_health-tower.damage
    assert soldier_2.health == soldier_2_health-tower.damage
    assert soldier_3.health == soldier_3_health-tower.damage

    #TO-DO
def test_upgrade():
    pass