from zoneinfo import available_timezones
from src.tile import Tile
import random

class MapGeneration:

    obstacle_type1 = [[0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,1,1,1,1,0,0,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,1,1,1,1,1,1,1,1,0],
                    [0,1,1,1,1,1,1,1,1,0],
                    [0,1,1,1,1,1,1,1,1,0],
                    [0,1,1,1,1,1,1,1,1,0],
                    [0,0,1,1,1,1,1,1,0,0],
                    [0,0,0,1,1,1,1,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0]]

    obstacle_type2 = [[0,0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,1,1,1,1,0],
                    [0,0,0,0,0,0,0,1,1,1,1,0],
                    [0,0,0,0,0,1,1,1,1,1,1,0],
                    [0,0,0,0,0,1,1,1,1,1,1,0],
                    [0,0,0,1,1,1,1,1,1,0,0,0],
                    [0,0,0,1,1,1,1,1,1,0,0,0],
                    [0,1,1,1,1,1,1,0,0,0,0,0],
                    [0,1,1,1,1,1,1,0,0,0,0,0],
                    [0,1,1,1,1,0,0,0,0,0,0,0],
                    [0,1,1,1,1,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0,0]]

    obstacle_type3 = [[0,0,0,0,0,0,0,0,0,0,0],
                    [0,0,0,0,1,1,1,1,1,1,0],
                    [0,0,0,0,1,1,1,1,1,1,0],
                    [0,0,0,0,1,1,1,1,1,1,0],
                    [0,0,0,0,1,1,1,1,1,1,0],
                    [0,0,0,1,1,1,1,1,0,0,0],
                    [0,1,1,1,1,1,1,0,0,0,0],
                    [0,1,1,1,1,1,1,0,0,0,0],
                    [0,1,1,1,1,1,1,0,0,0,0],
                    [0,1,1,1,1,1,1,0,0,0,0],
                    [0,0,0,0,0,0,0,0,0,0,0]]

    def check_placement_availability(game, obs_matrix, x, y):
        width = len(obs_matrix[0])
        height = len(obs_matrix)

        if(x < 0 or y < 0 or x+width >= game.map_width or y+height >= game.map_height):
            return False

        availability_matrix = MapGeneration.available_tiles(game)
        for i in range(y, y+height+1):
            for j in range(x, x+width+1):
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

    def place_obstacle(obs_matrix):
        pass

    def setup_availability_matrix(availability_matrix, x, y, width, height):
        left_x = max(min(x-2, width-1), 0) 
        right_x = max(min(x+2, width-1), 0) 
        top_y = max(min(y-2,  height-1), 0) 
        bottom_y = max(min(y+2,  height-1), 0) 
        for i in range(top_y, bottom_y+1):
            for j in range(left_x, right_x+1):
                availability_matrix[i][j] = 1
            

    def available_tiles(game):
        availability_matrix = [[0 for i in range(0, game.map_width)] for j in range(0, game.map_height)]
        for i in range(0, game.map_width):
            for j in range(0, game.map_height):
                if(game._map[i][j]._is_castle):
                    MapGeneration.setup_availability_matrix(availability_matrix, i, j, game.map_width, game.map_height)
                elif(game._map[i][j].type != "PLAIN"):
                    availability_matrix[i][j] = 1
        return availability_matrix
        
    def generate_map(game):
        return game._map