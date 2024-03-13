from constants import UP, DOWN, LEFT, RIGHT
import ai.pacman_flee as flee

class PacmanAI():
    
    def __init__(self):
        self.pacman = None
        self.ghosts = None

    def get_movement_direction(self):
        if self.pacman is not None and self.ghosts is not None:
            return flee.get_movement_direction(self.pacman, self.ghosts)
        else:
            return UP
