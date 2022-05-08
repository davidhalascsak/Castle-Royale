import pygame
import random
from src.castle import *
from src.soldier import *
from src.tower import *


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), 1)
    surface.blit(shape_surf, rect)


class Tile:

    def __init__(self, game, pos_x, pos_y):
        self.game_ref = game
        self.x = pos_x
        self.y = pos_y
        self._x = pos_x * 48
        self._y = pos_y * 48
        self._width = 48
        self._height = 48
        self._image = {
            None: (255, 255, 255),
            "PLAIN": pygame.transform.scale(pygame.image.load("assets/tile_assets/grass.png"),
                                            (self._width, self._width)),
            "LAKE": pygame.transform.scale(pygame.image.load("assets/tile_assets/swamp.png"),
                                           (self._width, self._width)),
            "HILL": pygame.transform.scale(pygame.image.load("assets/tile_assets/hill.png"), (self._width, self._width))
        }

        self._blender_image = pygame.transform.scale(pygame.image.load("assets/tile_assets/blender_swamp.png"),
                                                     (self._width, self._width))
        self._hover_image = pygame.transform.scale(pygame.image.load("assets/tile_assets/hover.png"),
                                                   (self._width, self._width))
        self._hover = False
        self._is_castle = False
        self._has_building = False
        self._units = []
        self._font = pygame.font.SysFont('Arial', 20)
        self.type = None
        self._selected = None
        self._waypoint = None

    def add_castle(self, castle):
        self._units.append(castle)
        self._is_castle = True
        self._has_building = True

    def build(self, player, type):
        if len(self._units) == 0 and self.type == "PLAIN":
            unit_price = eval(type).price
            if (player.gold - unit_price) >= 0:
                self.game_ref.path_finder.loadObstacles(False, None)
                self.game_ref.path_finder.set_obstacle(self.x, self.y, 1)
                if self.game_ref.path_finder.isPath(7, 0, 7, 25, False)[0]:
                    player.gold = (player.gold - unit_price)
                    unit = eval(type)(self, player, self.x, self.y)
                    player.add_unit(unit)
                    self._units.append(unit)
                    self._has_building = True
                else:
                    self.game_ref.path_finder.set_obstacle(self.x, self.y, 0)

    def upgrade_tower(self):
        unit = None
        for u in self._units:
            if issubclass(type(u), Tower):
                unit = u

        unit.upgrade()

    def demolish_tower(self):
        unit = None
        for u in self._units:
            if issubclass(type(u), Tower):
                unit = u
        self.game_ref.path_finder.set_obstacle(self.x, self.y, 0)
        unit.demolish()

    def remove_tower_ruin(self):
        if self._units[0].owner == self.game_ref._current_player:
            unit = None
            for u in self._units:
                if issubclass(type(u), Tower):
                    unit = u

            unit.remove_ruins()

    def train(self, player, soldier):
        count = 0
        for unit in self._units:
            if issubclass(type(unit), Soldier):
                count += 1

        if count < 5:
            unit_price = eval(soldier).price
            if (player.gold - unit_price) >= 0:
                if soldier != "Suicide":
                    player.gold = (player.gold - unit_price)
                    unit = eval(soldier)(self, player, self.x, self.y)
                    player.add_unit(unit)
                    self._units.append(unit)
                    unit.destination = player.game.not_active_player().castle_tile
                else:
                    if self.game_ref.player_1 == player:
                        if self.game_ref.player_2.has_tower():
                            player.gold = (player.gold - unit_price)
                            unit = eval(soldier)(self, player, self.x, self.y)
                            player.add_unit(unit)
                            self._units.append(unit)
                            unit.destination = self.game_ref.player_2.closest_tower(player.castle_tile)
                    elif self.game_ref.player_2 == player:
                        if self.game_ref.player_1.has_tower():
                            player.gold = (player.gold - unit_price)
                            unit = eval(soldier)(self, player, self.x, self.y)
                            player.add_unit(unit)
                            self._units.append(unit)
                            unit.destination = self.game_ref.player_1.closest_tower(player.castle_tile)

                # player.to_simulate.append(unit)
                # print("asd")

    def draw(self, surface):

        surface.blit(self._image[self.type], [self._y, self._x, self._width, self._height])
        if self.type == "LAKE":
            # up
            if self.x - 1 >= 0 and self.game_ref._map[self.x - 1][self.y].type != "LAKE":
                surface.blit(self._blender_image, [self._y, self._x, self._width, self._height])
            # down
            if self.x + 1 < self.game_ref.map_height and self.game_ref._map[self.x + 1][self.y].type != "LAKE":
                surface.blit(pygame.transform.rotate(self._blender_image, 180),
                             [self._y, self._x, self._width, self._height])
            # left
            if self.y >= 0 and self.game_ref._map[self.x][self.y - 1].type != "LAKE":
                surface.blit(pygame.transform.rotate(self._blender_image, 90),
                             [self._y, self._x, self._width, self._height])
            # right
            if self.y + 1 < self.game_ref.map_width and self.game_ref._map[self.x][self.y + 1].type != "LAKE":
                surface.blit(pygame.transform.rotate(self._blender_image, 270),
                             [self._y, self._x, self._width, self._height])
        # castle
        if self._is_castle:
            surface.blit(self.get_castle_image(), [self._y, self._x, self._width, self._height])

        if not self.game_ref.start_simulation:
            draw_rect_alpha(surface, pygame.Color(0, 0, 0, 30), pygame.Rect(self._y, self._x, self._width, self._height))

        # hover
        if self._hover:
            surface.blit(self._hover_image, [self._y, self._x, self._width, self._height])

        # select
        if self._selected:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self._y, self._x, self._width, self._height), 2)

        # waypoint
        if self._waypoint:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self._y, self._x, self._width, self._height), 2)
        # pygame.display.flip()

        # pygame.draw.rect(surface, pygame.Color(0, 0, 0, 50), pygame.Rect(self._y, self._x, self._width, self._height), 1)

    def draw_buildings_and_soldiers(self, surface):
        # draw tower
        if len(self._units) > 0 and isinstance(self._units[0], Tower):
            surface.blit(self.get_tower_image(), [self._y, self._x, self._width, self._height])

        # draw soldier
        if len(self._units) > 0 and (isinstance(self._units[0], Soldier)):
            surface.blit(self.get_soldier_image(), [self._y + 10, self._x + 10, self._width, self._height])
        elif len(self._units) > 1 and self._is_castle:
            surface.blit(self.get_soldier_image(), [self._y + 10, self._x + 10, self._width, self._height])

        # barrack draw

    def draw_context_menu_for_tiles(self, surface):
        # context menu for soldiers on a tile
        if self._hover and ((len(self._units) > 0 and issubclass(type(self._units[0]), Soldier)) or
                            (self._is_castle and len(self._units) > 1 and issubclass(type(self._units[1]), Soldier))):
            start = 0
            ind = 0
            length = len(self._units)
            if self._is_castle:
                start = 1
                length -= 1
            if self._y > 600:
                horizontal_alignment = -172
            else:
                horizontal_alignment = 0
            if self._x > 330:
                vertical_alignment = - length * 18
            else:
                vertical_alignment = 48
            pygame.draw.rect(surface, pygame.Color(255, 255, 255),
                             pygame.Rect(self._y + horizontal_alignment, self._x + vertical_alignment, 220,
                                         length * 18))
            for i in range(start, len(self._units)):
                text = pygame.font.SysFont('Arial', 19).render("{0} - {1}/{2}".
                                                               format(type(self._units[i]).__name__,
                                                                      self._units[i].health,
                                                                      self._units[i].max_health),
                                                               False, pygame.Color(0, 0, 0))
                surface.blit(text, (self._y + horizontal_alignment + 20, self._x + vertical_alignment - 2 + (ind * 18)))
                pygame.draw.circle(surface, self.get_owner_color(), (self._y + horizontal_alignment + 10, self._x + 9 + vertical_alignment + (ind * 18)), 5)
                ind += 1

            for u in self.units:
                if hasattr(u, "destination") and u.destination:
                    pygame.draw.rect(surface, (255, 0, 0),
                                     pygame.Rect(u.destination.y * 48, u.destination.x * 48, self._width, self._height),
                                     2)
                if hasattr(u, "waypoints") and len(u.waypoints) > 0:
                    for point in u.waypoints:
                        pygame.draw.rect(surface, (255, 255, 0),
                                         pygame.Rect(point[1] * 48, point[0] * 48, self._width,
                                                     self._height),2)

        if self._hover and (len(self._units) > 0 and issubclass(type(self._units[0]), Tower)):
            length = len(self._units)
            if self._y > 600:
                horizontal_alignment = -182
            else:
                horizontal_alignment = 0
            if self._x > 330:
                vertical_alignment = - length * 18
            else:
                vertical_alignment = 48
            pygame.draw.rect(surface, pygame.Color(255, 255, 255),
                             pygame.Rect(self._y + horizontal_alignment, self._x + vertical_alignment, 230,
                                         length * 18))
            if self._units[0].is_in_ruins:
                text = pygame.font.SysFont('Arial', 19).render("{0} days to clean the site.".format(self._units[0].clean_time), False, self.get_owner_color(0))
            else:
                text = pygame.font.SysFont('Arial', 19).render("{0} - {1}/{2}".
                                                               format(type(self._units[0]).__name__,
                                                                      self._units[0].health,
                                                                      self._units[0].max_health),
                                                               False, pygame.Color(0, 0, 0))
            pygame.draw.circle(surface, self.get_owner_color(), (self._y + horizontal_alignment + 10, self._x + 8 + vertical_alignment), 5)
            surface.blit(text, (self._y + horizontal_alignment + 20, self._x + vertical_alignment - 2))

    def is_over(self, pos):
        if self._y < pos[0] < self._y + self._width:
            if self._x < pos[1] < self._x + self._height:
                self._hover = True
                return True
        self._hover = False

    def get_image(self):
        if self._hover:
            return self._hover_image
        else:
            return self._image[self.type]

    def get_owner_color(self, index=0):
        if self._units[index].owner == self.game_ref.player_1:
            return 255, 0, 0
        else:
            return 0, 0, 255

    def get_castle_image(self):
        if self._units[0].owner == self.game_ref.player_1:
            return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_castle.png"),
                                          (self._width, self._width))
        else:
            return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_castle.png"),
                                          (self._width, self._width))

    def get_tower_image(self):
        if self._units[0].owner == self.game_ref.player_1:
            if self._units[0].is_in_ruins:
                return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_tower_ruin.png"),
                                              (self._width, self._width))
            else:
                if isinstance(self._units[0], BasicTower):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_basic_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._units[0], Splash):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_splash_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._units[0], Slow):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_slow_tower.png"),
                                                  (self._width, self._width))
        else:
            if self._units[0].is_in_ruins:
                return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_tower_ruin.png"),
                                              (self._width, self._width))
            else:
                if isinstance(self._units[0], BasicTower):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_basic_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._units[0], Splash):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_splash_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._units[0], Slow):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_slow_tower.png"),
                                                  (self._width, self._width))

    def get_soldier_image(self):
        red = False
        blue = False

        for unit in self._units:
            if unit.owner == self.game_ref.player_1:
                red = True
            else:
                blue = True
        if red and blue:
            return pygame.transform.scale(pygame.image.load("assets/tile_assets/mixed_knight.png"),
                                          (self._width / 1.5, self._width / 1.5))
        elif red:
            return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_knight.png"),
                                          (self._width / 1.5, self._width / 1.5))
        else:
            return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_knight.png"),
                                          (self._width / 1.5, self._width / 1.5))

    @property
    def units(self):
        return self._units

    @property
    def font(self):
        return self._font

    @property
    def is_castle(self):
        return self._is_castle

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, value):
        self._selected = value

    @property
    def waypoint(self):
        return self._waypoint

    @waypoint.setter
    def waypoint(self, value):
        self._waypoint = value

    @property
    def has_building(self):
        return self._has_building

    @has_building.setter
    def has_building(self, new_value):
        self._has_building = new_value
