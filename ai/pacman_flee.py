import math

from constants import UP, DOWN, LEFT, RIGHT
from vector import Vector2
from ghosts import GhostGroup
from entity import Entity



def check_change_state():
    return False


def get_movement_direction(pacman: Entity, ghosts: GhostGroup):
    curr_dist = get_shortest_ghost_dist(pacman.position, ghosts)
    new_dir = pacman.direction
    new_dist = 0
    for dir in pacman.validDirections():
        dist = get_shortest_ghost_dist(pacman.position + pacman.directions[dir], ghosts)
        print(f"DIST FOR {pacman.directions[dir]} IS {dist}")
        if dist > new_dist:
            new_dist = dist
            new_dir = dir
    print(f"LONGEST DIST IS {pacman.directions[dir]}")
    return new_dir


def distance_between(pos: Vector2, ghost):
    vec: Vector2 = ghost.position - pos
    #print(str(ghost.position) + " : " + str(pos) + " = " + str(vec))
    return vec.magnitude()


def get_shortest_ghost_dist(pos: Vector2, ghosts: GhostGroup):
    ghost_dist = math.inf
    for ghost in ghosts:
        if distance_between(pos, ghost) < ghost_dist:
            ghost_dist = distance_between(pos, ghost)
    return ghost_dist

