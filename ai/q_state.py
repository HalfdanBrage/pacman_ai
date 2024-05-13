import mmh3

class State:

    def __init__(self, pacman_node, ghost_nodes, ghost_target_nodes, traversed_ways, level) -> None:
        self.pacman_node = pacman_node
        self.ghost_nodes = ghost_nodes
        self.ghost_target_nodes = ghost_target_nodes
        self.traversed_ways = traversed_ways
        self.level = level

    def to_json(self):
        return {
            "pacman_node": self.pacman_node,
            "ghost_nodes": self.ghost_nodes,
            "ghost_target_nodes": self.ghost_target_nodes,
            "traversed_ways": self.traversed_ways,
            "level": self.level
    }

    def generate_hash(self):
        return str(mmh3.hash(str(self.to_json())))

