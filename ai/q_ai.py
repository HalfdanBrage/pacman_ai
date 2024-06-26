import random, json, math, multiprocessing, datetime

from ai.q_state import State

state = None
direction = 0
q_table = {} # The lookup table for our q learning bot. Maps from state hash to fitness values
history = [] # The history of the states in the current run. Used for effecting previous states based on the current one
max_score = 0 # Max score seen this run
max_level = 0 # Max level seen this run
score = 0 # Score for the current run

## Main method for the q learning ai. Simply returns the direction pacman should move in based on the current game state
def get_direction(globals, last_node, explore = False):
    global state, direction, q_table
    if last_node == None or q_table == {}:
        reset(globals)
    update_q_table(globals)

    if state and last_node:
        update_state(globals, state, last_node)
    else:
        state = get_initial_state(globals)
    
    if len(globals.pacman.validDirections()) > 1:
        direction = choose_direction(globals, explore)
    
    return int(direction)

run_count = 0
# Method that prepares everything for the next run
def reset(globals):
    global history, q_table, score, run_count, max_score, max_level
    run_count += 1
    if score > max_score:
        max_score = score
    print(str(run_count) + " games, max score: " + str(max_score) + ", max level: " + str(max_level))
    if q_table != {}:
        if run_count % 1000 == 0:
            minimize_q_table(q_table)
        if run_count % 50 == 0:
            t = multiprocessing.Process(target = save_q_table, args=(q_table, ))
            t.start()
    else:
        load_q_table()     
        minimize_q_table(q_table)
    history = []

# Method which scraps the worst values from the q_table
def minimize_q_table(q_table):
    for k in q_table.keys():
        for dir in q_table[k].keys():
            q_table[k][dir] = sorted(q_table[k][dir], reverse = True)[:40]

# Method which actually chooses a direction
def choose_direction(globals, explore = False):
    global q_table, state
    if state.generate_hash() in q_table:
        available_directions = globals.pacman.validDirections()
        high_val = -math.inf
        best_dir = 0
        for dir in available_directions:
                if explore:
                    if not str(dir) in q_table[state.generate_hash()] or random.randint(0, 512) == 1:
                        best_dir = dir
                        break
                    elif len(q_table[state.generate_hash()][str(dir)]) < 1:
                        best_dir = dir
                        break
                if str(dir) in q_table[state.generate_hash()]:
                    point_values = sorted(q_table[state.generate_hash()][str(dir)], reverse = True)
                    # avg_high_value = sum(point_values[:4])/(4 if len(point_values) > 4 else len(point_values))
                    avg_high_value = max(point_values) * (random.uniform(0.6, 1.4) if explore else 1)

                    if avg_high_value > high_val:
                        high_val = avg_high_value
                        best_dir = dir
        return str(best_dir)
    #print("NEW")
    return str(random.choice(globals.pacman.validDirections()))

def load_q_table():
    global q_table
    with open(("ai/trainingdata-backup-" + str(datetime.datetime.now())).replace(":", "-"), "w") as backup:
        with open("ai/trainingdata", "r") as file:
            data = file.read()
            backup.write(data)
            try:
                q_table = json.loads(data)
            except:
                q_table = {}

def save_q_table(q_table):
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
    global isDead
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


prev_level = 1
prev_lives = 0
prev_score = 0
# Fitness calculation method. This is based on points scored. Additionally it punishes when pacman dies, punishes when pacman moves along an edge without scoring, and rewards for clearing a level.
def get_fitness(globals):
    global q_table, history, prev_score, score, prev_lives, prev_level, max_level
    score = globals.score
    fitness = globals.score - prev_score
    prev_score = globals.score
    if globals.level > max_level:
        max_level = globals.level

    if prev_level < globals.level:
        print("Completed level!!!")
        fitness += 800
    prev_level = globals.level

    if globals.lives < prev_lives:
        fitness -= 400
    prev_lives = globals.lives

    if fitness == 0:
        fitness = -20

    for i, item in enumerate(history):
        (q_table[item[0]])[item[1]][item[2]] += fitness / (len(history) - i)
    return fitness
