import random, json, math

from ai.q_state import State

state = None
direction = 0
#{state : {actions: [values]}}
q_table = {}
history = []
scores = []
score = 0

## update state, then do lookup
def get_direction(globals, last_node, explore = False):
    global state, direction, q_table
    if last_node == None or q_table == {}:
        reset()
    update_q_table(globals)

    if state and last_node:
        update_state(globals, state, last_node)
    else:
        state = get_initial_state(globals)
    
    if len(globals.pacman.validDirections()) > 1:
        direction = choose_direction(globals, explore)
    
    return int(direction)

def reset():
    global history, q_table, score
    scores.append(score)
    print("Average Score: " + str(sum(scores)/len(scores)))
    if q_table != {}:
        save_q_table()
    history = []
    load_q_table() 
    for k in q_table.keys():
        for dir in q_table[k].keys():
            q_table[k][dir] = sorted(q_table[k][dir], reverse = True)[:40]
        

def choose_direction(globals, explore = False):
    global q_table, state
    if state.generate_hash() in q_table:
        available_directions = globals.pacman.validDirections()
        high_val = -math.inf
        best_dir = 0
        for dir in available_directions:
                if explore:
                    if not str(dir) in q_table[state.generate_hash()] or random.randint(0, 20) == 1:
                        best_dir = dir
                        break
                    elif len(q_table[state.generate_hash()][str(dir)]) < 20:
                        best_dir = dir
                        break
                if str(dir) in q_table[state.generate_hash()]:
                    point_values = sorted(q_table[state.generate_hash()][str(dir)], reverse = True)
                    avg_high_value = sum(point_values[:4])/(4 if len(point_values) > 4 else len(point_values))

                    if avg_high_value > high_val:
                        high_val = avg_high_value
                        best_dir = dir
        return str(best_dir)
    return str(random.choice(globals.pacman.validDirections()))


def load_q_table():
    global q_table
    with open("ai/trainingdata", "r") as file:
        data = file.read()
        try:
            q_table = json.loads(data)
        except:
            q_table = {}

def save_q_table():
    global q_table
    f = open("ai/trainingdata", "w")
    f.write(json.dumps(q_table))
    f.close()

def update_q_table(globals):
    global state, direction, q_table, history
    if state != None and direction != None:
        index = 0
        if state.generate_hash() in q_table:
            if direction in q_table[state.generate_hash()]:
                q_table[state.generate_hash()][direction].append(get_fitness(globals))
                index = len(q_table[state.generate_hash()][direction]) - 1
            else:
                q_table[state.generate_hash()][direction] = [get_fitness(globals)]
        else:
            q_table[state.generate_hash()] = {direction: [get_fitness(globals)]}
        history.append((state.generate_hash(), direction, index))


def update_state(globals, state : State, last_node):
    state.pacman_node = str(globals.pacman.node.position)
    state.ghost_nodes = [str(g.node.position) for g in globals.ghosts.ghosts]
    state.ghost_target_nodes = [str(g.target.position) for g in globals.ghosts.ghosts]
    state.traversed_ways.append(sorted([state.pacman_node, str(last_node.position)]))
    state.traversed_ways.sort()
    state.level = globals.level
    return state
    

def get_initial_state(globals):
    pacman_node = str(globals.pacman.node.position)
    ghost_nodes = [str(g.node.position) for g in globals.ghosts.ghosts]
    ghost_target_nodes = [str(g.target.position) for g in globals.ghosts.ghosts]
    pellet_edges = []
    return State(pacman_node, ghost_nodes, ghost_target_nodes, pellet_edges, globals.level)


prev_score = 0
def get_fitness(globals):
    global q_table, history, prev_score, score
    score = globals.score
    fitness = globals.score - prev_score
    prev_score = globals.score
    for i, item in enumerate(history):
        (q_table[item[0]])[item[1]][item[2]] += fitness / (len(history) - i)
    return fitness
