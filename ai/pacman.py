from constants import UP, DOWN, LEFT, RIGHT
import ai.pacman_flee as flee

class PacmanAI():
    
    def __init__(self):
        self.pacman = None
        self.ghosts = None
        self.globals = None

    def get_movement_direction(self):
        if self.globals is not None:
            print(type(self.globals.pacman.node.id))
            return flee.get_movement_direction(self.globals.pacman, self.globals.ghosts)
        else:
            print("FAILING")
            return UP
