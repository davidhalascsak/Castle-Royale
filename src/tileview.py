import pygame
import random
from src.castle import *
from src.soldier import *
from src.tower import *


def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect(), 1)
    surface.blit(shape_surf, rect)


class TileView:

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
        self._font = pygame.font.SysFont('Arial', 20)
        self._tile = None
        


    def draw(self, surface):

        surface.blit(self._image[self._tile.type], [self._y, self._x, self._width, self._height])
        if self._tile.type == "LAKE":
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
        if self._tile._is_castle:
            surface.blit(self.get_castle_image(), [self._y, self._x, self._width, self._height])

        if not self.game_ref.start_simulation:
            draw_rect_alpha(surface, pygame.Color(0, 0, 0, 30), pygame.Rect(self._y, self._x, self._width, self._height))

        # hover
        if self._tile._hover:
            surface.blit(self._hover_image, [self._y, self._x, self._width, self._height])

        # select
        if self._tile._selected:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self._y, self._x, self._width, self._height), 2)

        # waypoint
        if self._tile._waypoint:
            pygame.draw.rect(surface, (0, 255, 0), pygame.Rect(self._y, self._x, self._width, self._height), 2)

    def draw_buildings_and_soldiers(self, surface):
        # draw tower
        if len(self._tile._units) > 0 and isinstance(self._tile._units[0], Tower):
            surface.blit(self.get_tower_image(), [self._y, self._x, self._width, self._height])

        # draw soldier
        if (len(self._tile._units) > 0 and (isinstance(self._tile._units[0], Soldier))) or (len(self._tile._units) > 1 and self._tile._is_castle):
            surface.blit(self.get_soldier_image(), [self._y + 10, self._x + 10, self._width, self._height])

    def draw_context_menu_for_tiles(self, surface):
        # context menu for soldiers on a tile
        if self._tile._hover and ((len(self._tile._units) > 0 and issubclass(type(self._tile._units[0]), Soldier)) or
                            (self._tile._is_castle and len(self._tile._units) > 1 and issubclass(type(self._tile._units[1]), Soldier))):
            start = 0
            ind = 0
            length = len(self._tile._units)
            if self._tile._is_castle:
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
            for i in range(start, len(self._tile._units)):
                text = pygame.font.SysFont('Arial', 19).render("{0} - {1}/{2}".
                                                               format(type(self._tile._units[i]).__name__,
                                                                      self._tile._units[i].health,
                                                                      self._tile._units[i].max_health),
                                                               False, pygame.Color(0, 0, 0))
                surface.blit(text, (self._y + horizontal_alignment + 20, self._x + vertical_alignment - 2 + (ind * 18)))
                pygame.draw.circle(surface, self.get_owner_color(), (self._y + horizontal_alignment + 10, self._x + 9 + vertical_alignment + (ind * 18)), 5)
                ind += 1

            for u in self._tile._units:
                if hasattr(u, "destination") and u.destination:
                    pygame.draw.rect(surface, (255, 0, 0),
                                     pygame.Rect(u.destination.y * 48, u.destination.x * 48, self._width, self._height),
                                     2)
                if hasattr(u, "waypoints") and len(u.waypoints) > 0:
                    for point in u.waypoints:
                        pygame.draw.rect(surface, (255, 255, 0),
                                         pygame.Rect(point[1] * 48, point[0] * 48, self._width,
                                                     self._height),2)

        if self._tile._hover and (len(self._tile._units) > 0 and issubclass(type(self._tile._units[0]), Tower)):
            length = len(self._tile._units)
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
            if self._tile._units[0].is_in_ruins:
                text = pygame.font.SysFont('Arial', 19).render("{0} days to clean the site.".format(self._tile._units[0].clean_time), False, self.get_owner_color(0))
            else:
                text = pygame.font.SysFont('Arial', 19).render("{0} - {1}/{2}".
                                                               format(type(self._tile._units[0]).__name__,
                                                                      self._tile._units[0].health,
                                                                      self._tile._units[0].max_health),
                                                               False, pygame.Color(0, 0, 0))
            pygame.draw.circle(surface, self.get_owner_color(), (self._y + horizontal_alignment + 10, self._x + 8 + vertical_alignment), 5)
            surface.blit(text, (self._y + horizontal_alignment + 20, self._x + vertical_alignment - 2))


    def get_image(self):
        if self._tile._hover:
            return self._hover_image
        else:
            return self._image[self._tile.type]

    def get_owner_color(self, index=0):
        if self._tile._units[index].owner == self.game_ref.player_1:
            return 255, 0, 0
        else:
            return 0, 0, 255

    def get_castle_image(self):
        if self._tile._units[0].owner == self.game_ref.player_1:
            return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_castle.png"),
                                          (self._width, self._width))
        else:
            return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_castle.png"),
                                          (self._width, self._width))

    def get_tower_image(self):
        if self._tile._units[0].owner == self.game_ref.player_1:
            if self._tile._units[0].is_in_ruins:
                return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_tower_ruin.png"),
                                              (self._width, self._width))
            else:
                if isinstance(self._tile._units[0], BasicTower):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_basic_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._tile._units[0], Splash):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_splash_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._tile._units[0], Slow):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/red_slow_tower.png"),
                                                  (self._width, self._width))
        else:
            if self._tile._units[0].is_in_ruins:
                return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_tower_ruin.png"),
                                              (self._width, self._width))
            else:
                if isinstance(self._tile._units[0], BasicTower):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_basic_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._tile._units[0], Splash):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_splash_tower.png"),
                                                  (self._width, self._width))
                elif isinstance(self._tile._units[0], Slow):
                    return pygame.transform.scale(pygame.image.load("assets/tile_assets/blue_slow_tower.png"),
                                                  (self._width, self._width))

    def get_soldier_image(self):
        red = False
        blue = False

        for unit in self._tile._units:
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
    def tile(self):
        return self._tile

    @property
    def font(self):
        return self._font
