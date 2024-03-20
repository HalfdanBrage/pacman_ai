import math
from random import vonmisesvariate

from constants import UP, DOWN, LEFT, RIGHT
from vector import Vector2
from ghosts import GhostGroup, Ghost
from entity import Entity
from nodes import Node


def check_change_state():
    return False


def get_movement_direction(pacman: Entity, ghosts: GhostGroup):
    target_dir = get_desired_direction(pacman, ghosts, get_shortest_ghost_dist(pacman.position, ghosts) + 30)
    dir = get_closest_dir(pacman, target_dir, pacman.validDirections())
    for ghost in ghosts.ghosts:
        print(dijkstras(pacman, ghost))
    return dir
    # curr_dist = get_shortest_ghost_dist(pacman.position, ghosts)
    # new_dir = pacman.direction
    # new_dist = 0
    # for dir in pacman.validDirections():
    #    dist = get_shortest_ghost_dist(pacman.position + pacman.directions[dir], ghosts)
    #    if dist > new_dist:
    #        new_dist = dist
    #        new_dir = dir
    # return new_dir


def get_closest_dir(pacman: Entity, desired_dir, available_dirs):
    dist = math.inf
    new_dir = 0
    for _dir in available_dirs:
        dir = pacman.directions[_dir]
        dir_dist = (dir - desired_dir).magnitude()
        if dir_dist < dist:
            new_dir = _dir
            dist = dir_dist
        if len(available_dirs) > 1:
            pass
            # print(f"AVAILABLE: {dir}")
    if len(available_dirs) > 1:
        pass
        # print(f"BEST: {pacman.directions[new_dir]}")
    return new_dir

def distance_between(pos: Vector2, ghost):
    vec: Vector2 = ghost.position - pos
    return vec.magnitude()


def get_shortest_ghost_dist(pos: Vector2, ghosts: GhostGroup):
    ghost_dist = math.inf
    for ghost in ghosts: 
        if distance_between(pos, ghost) < ghost_dist:
            ghost_dist = distance_between(pos, ghost)
    return ghost_dist


def get_desired_direction(pacman: Entity, ghosts: GhostGroup, detection_range: int):
    pacman_pos = pacman.position
    impulse_vectors = []
    for ghost in ghosts:
        dist = distance_between(pacman_pos, ghost) 
        if dist < detection_range:
            impulse_vectors.append((pacman_pos - ghost.position).normalized() * 1 / (detection_range - dist))
    result = Vector2(0, 0)
    for vec in impulse_vectors:
        result += vec

    return result.normalized()


def explore(node, s):
    s.append(node)
    for v in node.neighbors.values():
        if v not in s and v != None:
            s = explore(v, s)
    return s

def dijkstras(pacman: Entity, ghost: Ghost):
    unvisited = explore(pacman.node, [])
    distances = {n : math.inf for n in unvisited}

    distances[pacman.node] = get_dist_to_node(pacman, pacman.node)
    distances[pacman.target] = get_dist_to_node(pacman, pacman.target)

    while distances[ghost.node] != math.inf and len(unvisited) > 0:
        next_node_i = 0
        for i in range(len(unvisited)):
            if distances[unvisited[i]] < distances[unvisited[next_node_i]]:
                next_node_i = i
        next_node = unvisited.pop(next_node_i)

    return distances

    seen_nodes = []
    visited_nodes = []
    reachable_nodes = []
    
    reachable_nodes.append(get_dijkstras_entry(pacman, pacman.node))
    reachable_nodes.append(get_dijkstras_entry(pacman, pacman.target))
    seen_nodes = [n for n, _ in reachable_nodes]

    next_node = reachable_nodes[0]
    while ghost.node != next_node[0]:
        for node in reachable_nodes:
            if node[1] < next_node[1]:
                next_node = node
        for k, v in next_node[0].neighbors.items():
            if v not in seen_nodes:
                node_entry = (v, )
            

def get_dist(n1: Node, n2: Node):
    return (n2.position - n1.position).magnitude()

def get_dijkstras_entry(entity: Entity, node : Node):
    return (node, get_dist_to_node(entity, node))

def get_dist_to_node(entity: Entity, node: Node):
    return (node.position - entity.position).magnitude()
