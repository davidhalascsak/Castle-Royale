import numpy as np


class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node, maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]
    return path


def search(maze, cost, start, end):
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    yet_to_visit_list = []
    visited_list = []

    yet_to_visit_list.append(start_node)

    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    move = [[-1, 0],  # go up
            [0, -1],  # go left
            [1, 0],  # go down
            [0, 1]]  # go right

    no_rows, no_columns = np.shape(maze)

    while len(yet_to_visit_list) > 0:

        outer_iterations += 1

        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        if outer_iterations > max_iterations:
            print("giving up on pathfinding too many iterations")
            return return_path(current_node, maze)

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node, maze)

        children = []

        for new_position in move:

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            child.g = current_node.g + cost

            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))

            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            yet_to_visit_list.append(child)


class AStar:
    def __init__(self, game):
        self.game = game
        self.arr = []

        for i in range(14):
            self.arr.append([])
            for j in range(26):
                self.arr[i].append(0)

        self.row = len(self.arr)
        self.col = len(self.arr[0])

    def isPath(self, x1, y1, x2, y2, special=False, update=True):
        if update:
            self.loadObstacles(special)
        path = search(self.arr, 1, [x1, y1], [x2, y2])
        if path is None:
            return False, []
        return True, path

    def loadObstacles(self, special):
        for row in self.game.map:
            for tile in row:
                if len(tile.units) > 0 and not tile.is_castle:
                    self.arr[tile.x][tile.y] = 1
                elif not special and tile.type != "PLAIN":
                    self.arr[tile.x][tile.y] = 1
                else:
                    self.arr[tile.x][tile.y] = 0
        # self.arr = []
        # for i in range(14):
        #     self.arr.append([])
        #     for j in range(26):
        #         self.arr[i].append(0)

    def set_obstacle(self, x, y, value):
        self.arr[x][y] = value
