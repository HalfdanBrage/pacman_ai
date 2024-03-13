import math

from constants import UP, DOWN, LEFT, RIGHT
from vector import Vector2
from ghosts import GhostGroup
from entity import Entity



def check_change_state():
    return False


def get_movement_direction(pacman: Entity, ghosts: GhostGroup):
    target_dir = get_desired_direction(pacman, ghosts, get_shortest_ghost_dist(pacman.position, ghosts) + 30)
    dir = get_closest_dir(pacman, target_dir, pacman.validDirections())
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
            print(f"AVAILABLE: {dir}")
    if len(available_dirs) > 1:
        print(f"BEST: {pacman.directions[new_dir]}")
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
