from q_state import State


def get_initial_state(globals):
    pacman_node = str(globals.pacman.node)
    ghost_nodes = [str(g.node) for g in globals.ghosts.ghosts]
    ghost_target_nodes = [str(g.target) for g in globals.ghosts.ghosts]
    pellet_edges = get_full_pellet_edges(globals.pacman.node)
    return State(pacman_node, ghost_nodes, ghost_target_nodes, pellet_edges)


def get_full_pellet_edges(node, edges = {}):
    for _, v in node.neighbors:
        if str(v) not in edges.keys():
            edges[str(v)] = True
            get_full_pellet_edges(globals, edges)
