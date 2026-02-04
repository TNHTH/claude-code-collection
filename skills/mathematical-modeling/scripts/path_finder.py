"""
Path Finder Module
Implements A* Search Algorithm for grid-based path planning.
Category: Optimization
"""

import heapq
import math

class Node:
    def __init__(self, x, y, parent=None):
        self.x = x
        self.y = y
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic cost from current node to end
        self.f = 0  # Total cost (g + h)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash((self.x, self.y))

def heuristic(node_a, node_b):
    # Manhattan distance for grid with 4-way movement
    # Euclidean distance for 8-way (but let's stick to Manhattan for simplicity if 4-way)
    return abs(node_a.x - node_b.x) + abs(node_a.y - node_b.y)

def find_path(grid, start_pos, end_pos, allow_diagonal=False):
    """
    Finds a path from start to end on a grid using A* algorithm.

    Args:
        grid (list[list[int]]): 2D grid where 0 is walkable and 1 is obstacle.
        start_pos (tuple): (x, y) start coordinates.
        end_pos (tuple): (x, y) end coordinates.
        allow_diagonal (bool): Whether to allow diagonal movement.

    Returns:
        dict: {
            "path": list[tuple], # [(x1,y1), (x2,y2), ...]
            "steps": int,
            "cost": float
        }
    """
    rows = len(grid)
    cols = len(grid[0])

    start_node = Node(start_pos[0], start_pos[1])
    end_node = Node(end_pos[0], end_pos[1])

    open_list = []
    closed_set = set()

    heapq.heappush(open_list, start_node)

    # Check if start or end are obstacles
    if grid[start_pos[0]][start_pos[1]] == 1:
        return {"error": "Start position is an obstacle"}
    if grid[end_pos[0]][end_pos[1]] == 1:
        return {"error": "End position is an obstacle"}

    while open_list:
        current_node = heapq.heappop(open_list)
        closed_set.add((current_node.x, current_node.y))

        # Found the destination
        if current_node == end_node:
            path = []
            current = current_node
            while current:
                path.append((current.x, current.y))
                current = current.parent
            return {
                "path": path[::-1], # Return reversed path
                "steps": len(path) - 1,
                "cost": current_node.g
            }

        # Generate children
        children = []

        # Adjacent squares (0, -1), (0, 1), (-1, 0), (1, 0)
        movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        if allow_diagonal:
             movements.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])

        for new_position in movements:
            node_position = (current_node.x + new_position[0], current_node.y + new_position[1])

            # Check within range
            if node_position[0] > (rows - 1) or node_position[0] < 0 or \
               node_position[1] > (cols - 1) or node_position[1] < 0:
                continue

            # Check walkable terrain
            if grid[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(node_position[0], node_position[1], current_node)
            children.append(new_node)

        for child in children:
            if (child.x, child.y) in closed_set:
                continue

            # Calculate cost
            move_cost = 1 # Simple cost
            if allow_diagonal and (abs(child.x - current_node.x) + abs(child.y - current_node.y) == 2):
                move_cost = 1.414 # sqrt(2)

            child.g = current_node.g + move_cost
            child.h = heuristic(child, end_node)
            child.f = child.g + child.h

            # Check if child is already in open list with lower g
            # This is O(N) scan, can be optimized but fine for simple skill
            if any(open_node for open_node in open_list if child == open_node and child.g > open_node.g):
                continue

            heapq.heappush(open_list, child)

    return {"error": "No path found"}

if __name__ == "__main__":
    # Test
    grid_map = [
        [0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1],
        [0, 0, 0, 0, 0],
        [0, 1, 1, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start = (0, 0)
    end = (4, 4)
    print(find_path(grid_map, start, end))
