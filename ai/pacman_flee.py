import math
import pygame
import random
from random import vonmisesvariate

from constants import UP, DOWN, LEFT, RIGHT
from vector import Vector2
from ghosts import GhostGroup, Ghost
from entity import Entity
from nodes import Node

# Dir prios generated at every turn, such that it doesnt flicker in one spot when multiple directions can be chosen
dir_prios = {1: 0, -1: 0, 2: 1, -2: 0}

def randomize_dir_prios():
    global dir_prios
    dir_prios = {k: random.random() for k in dir_prios.keys()}

def check_change_state():
    return False

# Main method for retrieving the direction pacman should move in
def get_movement_direction(pacman: Entity, ghosts: GhostGroup):
    dir_weights = get_dijkstras_direction_weights(pacman, ghosts)
    dir = get_safest_dir(pacman, dir_weights)
    pygame.draw.circle(pygame.display.get_surface(), (0, 255, 0), pacman.node.position.asTuple(), 10)
    pygame.draw.circle(pygame.display.get_surface(), (255, 0, 0), pacman.target.position.asTuple(), 10)
    pygame.display.update()
    return dir

# Chose a direction based on weights, tiebreakers decided by dir_prio
def get_safest_dir(pacman: Entity, dir_weights):
    global dir_prios
    dir = 0
    weight = math.inf
    prio = 0
    for _dir in get_valid_directions(pacman):
        _weight = 0
        _dir_vec = pacman.directions[_dir]
        for k, v in dir_weights.items():
            if k == _dir_vec:
                _weight += v
        if _weight < weight:
            dir = _dir
            weight = _weight
            prio = dir_prios[dir]
        elif _weight == weight and prio < dir_prios[_dir]:
            dir = _dir
            weight = _weight
            prio = dir_prios[dir]
    return dir

# Returns all directions pacman can move in AT ANY ONE POINT IN TIME
# This is used instead of the inbuild get_valid_directions, which only updates on intersections
def get_valid_directions(pacman: Entity):
    if pacman.target != pacman.node:
        if pacman.target.position.y == pacman.node.position.y:
            return [2, -2]
        else:
            return [1, -1]
    randomize_dir_prios()
    return pacman.validDirections()


# This method returns the last direction of the path from the ghost to pacman, and the weight, calculated based on the length of the path
def get_dijkstras_direction_weights(pacman: Entity, ghosts: GhostGroup):
    dirs = {}
    for ghost in ghosts.ghosts:
        dist, pos = dijkstras(pacman, ghost)
        if dist != None:
            dir = (pos - pacman.position).normalized()
            if dir in dirs.keys():
                dirs[dir] = dirs[dir] + weight_dist(dist)
            else:
                dirs[dir] = weight_dist(dist)
    dirs = {k: v for k, v in dirs.items() if v > 1000}
    return dirs

# Method for converting distance into weight
def weight_dist(dist):
    raw_dist = math.inf if dist == 0 else (1 + 1000.0/dist)
    return min(raw_dist**4, 2**31)

# Helper method used to initialize an empty array of all nodes
def explore(node, s):
    s.append(node)
    for v in node.neighbors.values():
        if v not in s and v != None:
            s = explore(v, s)
    return s

# Our dijkstras implementation, which returns distance, and the last node in the path of the ghost before it reaches pacman
# This method is designed to be called per ghost
def dijkstras(pacman: Entity, ghost: Ghost):
    # If the ghost is on the same edge as pacman, ignore dijkstras and do calculation based on euclidean distance
    if (pacman.target == ghost.target or pacman.target == ghost.node) and (pacman.node == ghost.target or pacman.node == ghost.node):
        dist = (ghost.position - pacman.position).magnitude()
        pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), pacman.position.asTuple(), ghost.position.asTuple(), round(weight_dist(dist) / 100))
        return (dist, ghost.position)

    unvisited = explore(pacman.node, [])
    distances = {n : math.inf for n in unvisited}
    from_nodes = {}
    
    # if pacman is at an intersection, add all neighboring nodes to the graph
    if pacman.position == pacman.target.position:
        for node in pacman.target.neighbors.values():
            if node != None:
                distances[node] = get_dist_to_node(pacman, node)
                from_nodes[node] = None
    else: # if pacman isnt at an intersection, only add pacmans target node and last node
        distances[pacman.node] = get_dist_to_node(pacman, pacman.node)
        from_nodes[pacman.node] = None
        distances[pacman.target] = get_dist_to_node(pacman, pacman.target)
        from_nodes[pacman.target] = None

    # The main dijkstras loop, which keeps checking the node with the shortest distance, and explores it untill it reaches the ghost
    while distances[ghost.node] == math.inf and len(unvisited) > 0:
        next_node_i = 0
        for i in range(len(unvisited)):
            if distances[unvisited[i]] < distances[unvisited[next_node_i]]:
                next_node_i = i
        current = unvisited.pop(next_node_i)

        for node in current.neighbors.values():
            if node in unvisited:
                _dist = distances[current] + get_dist(current, node)
                if _dist < distances[node]:
                    distances[node] = _dist
                    from_nodes[node] = current
    
    # run through the path from the ghost to pacman, to find the last node in the path
    t_node = ghost.node
    while from_nodes[t_node] != None:
        t_node = from_nodes[t_node]
        if from_nodes[t_node] != None:
            pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), t_node.position.asTuple(), from_nodes[t_node].position.asTuple(), round(weight_dist(distances[ghost.node]) / 100))
    pygame.draw.line(pygame.display.get_surface(), (255, 0, 0), pacman.position.asTuple(), t_node.position.asTuple(), round(weight_dist(distances[ghost.node]) / 100))

    # return None, None if the ghost isnt following the shortest path (eg. ignore the ghost if it isn't chasing the player)
    if from_nodes[ghost.node] != None:
        if (from_nodes[ghost.node].position - ghost.node.position).normalized() == pacman.directions[ghost.direction]:
            return (distances[ghost.node], t_node.position)
    return None, None

# get distance between two nodes
def get_dist(n1: Node, n2: Node):
    return (n2.position - n1.position).magnitude()

# get distance between entity and node
def get_dist_to_node(entity: Entity, node: Node):
    return (node.position - entity.position).magnitude()
