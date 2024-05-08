from constants import UP, DOWN, LEFT, RIGHT
import ai.pacman_flee as flee
from vector import Vector2
from ai import q_ai

class PacmanAI():
    
    def __init__(self):
        self.pacman = None
        self.ghosts = None
        self.globals = None
        self.direction = RIGHT
        self.mode = "q_explore"
        self.last_node = None

    def get_movement_direction(self):
        if self.mode == "standard":
            if self.globals.pacman.node == self.globals.pacman.target:
                q_ai.get_direction(self.globals, self.last_node)
                self.last_node = self.globals.pacman.node
            self.direction = flee.get_movement_direction(self.globals.pacman, self.globals.ghosts)
        if self.mode == "q":
            if self.globals.pacman.node == self.globals.pacman.target and self.globals.pacman.node != self.last_node:
                self.direction = q_ai.get_direction(self.globals, self.last_node)
                self.last_node = self.globals.pacman.node
        if self.mode == "q_explore":
            if self.globals.pacman.node == self.globals.pacman.target and self.globals.pacman.node != self.last_node:
                self.direction = q_ai.get_direction(self.globals, self.last_node, True)
                self.last_node = self.globals.pacman.node
        return self.direction
