from zoneinfo import available_timezones
from src.tile import Tile
import random

class MapGeneration:

    obstacle_type1 = [[0,0,0,0,0,0,0,0],
                      [0,0,0,1,1,0,0,0],
                      [0,0,1,1,1,1,0,0],
                      [0,1,1,1,1,1,1,0],
                      [0,0,1,1,1,1,0,0],
                      [0,0,0,1,1,0,0,0],
                      [0,0,0,0,0,0,0,0]]

    obstacle_type2 = [[0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,1,1,1,0],
                      [0,0,0,1,1,1,1,1,0],
                      [0,0,1,1,1,1,1,0,0],
                      [0,1,1,1,1,0,0,0,0],
                      [0,1,1,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0]]

    obstacle_type3 = [[0,0,0,0,0,0,0,0,0],
                      [0,1,1,1,1,1,0,0,0],
                      [0,0,1,1,1,1,1,0,0],
                      [0,0,0,1,1,1,1,1,0],
                      [0,0,0,0,0,0,0,0,0]]

    def check_placement_availability(game, obs_matrix, x, y):
        width = len(obs_matrix[0])
        height = len(obs_matrix)

        if(x < 0 or y < 0 or y+width >= game.map_width or x+height >= game.map_height):
            return False

        availability_matrix = MapGeneration.available_tiles(game)
        for i in range(x, x+height+1):
            for j in range(y, y+width+1):
                if(availability_matrix[i][j] == 1):
                    return False
        return True

    def choose_obstacles():
        random_number = random.randrange(3)
        if(random_number == 0):
            return MapGeneration.obstacle_type1
        elif(random_number == 1):
            return MapGeneration.obstacle_type2
        elif(random_number == 2):
            return MapGeneration.obstacle_type3
        return []

    def place_obstacle(game, obs_matrix, x, y, type):
        obs_width = len(obs_matrix[0])
        obs_height = len(obs_matrix)
        for i in range(x, obs_height+x):
            for j in range(y, obs_width+y):
                if(obs_matrix[i-x][j-y] == 1):
                    t = Tile(game, i, j)
                    t.type = type
                    game._map[i][j] = t

    def setup_availability_matrix(availability_matrix, x, y, width, height):
        top_x = max(min(x-2, height-1), 0) 
        bottom_x = max(min(x+2, height-1), 0) 
        left_y = max(min(y-2,  width-1), 0) 
        right_y = max(min(y+2,  width-1), 0) 
        for i in range(top_x, bottom_x+1):
            for j in range(left_y, right_y+1):
                availability_matrix[i][j] = 1
            

    def available_tiles(game):
        availability_matrix = [[0 for i in range(0, game.map_width)] for j in range(0, game.map_height)]
        for i in range(0, game.map_height):
            for j in range(0, game.map_width):
                if(game._map[i][j]._is_castle):
                    MapGeneration.setup_availability_matrix(availability_matrix, i, j, game.map_width, game.map_height)
                elif(game._map[i][j].type != "PLAIN"):
                    availability_matrix[i][j] = 1
        return availability_matrix
        
    def generate_map(game):
        hill = MapGeneration.choose_obstacles()
        lake = MapGeneration.choose_obstacles()
        free_tiles = []
        for i in range(0, game.map_height):
            for j in range(0, game.map_width):
                if(MapGeneration.check_placement_availability(game, hill, i, j)):
                    free_tiles.append((i,j))
        if(len(free_tiles) > 0):
            free_tuple = free_tiles[random.randrange(len(free_tiles))]
            MapGeneration.place_obstacle(game, hill, free_tuple[0], free_tuple[1], "HILL")
        
        free_tiles = []
        for i in range(0, game.map_height):
            for j in range(0, game.map_width):
                if(MapGeneration.check_placement_availability(game, hill, i, j)):
                    free_tiles.append((i,j))
        if(len(free_tiles) > 0):
            free_tuple = free_tiles[random.randrange(len(free_tiles))]
            MapGeneration.place_obstacle(game, lake, free_tuple[0], free_tuple[1], "LAKE")