class State:

    def __init__(self, pacman_node, ghost_nodes, ghost_target_nodes, traversed_ways) -> None:
        self.pacman_node = pacman_node
        self.ghost_nodes = ghost_nodes
        self.ghost_target_nodes = ghost_target_nodes
        self.traversed_ways = traversed_ways

    def to_json(self):
        return {
            "pacman_node": self.pacman_node,
            "ghost_nodes": self.ghost_nodes,
            "ghost_target_nodes": self.ghost_target_nodes,
            "traversed_ways": self.traversed_ways
        }

