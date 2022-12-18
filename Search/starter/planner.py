#Look for ### IMPLEMENT BELOW ### tags in this file. These tags indicate what has
#to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
# Search engines
from search import * 
# Warehouse specific classes
from warehouse import WarehouseState, Direction, warehouse_goal_state


def heur_displaced(state):
    '''A trivial example heuristic that is admissible''' # box not in storage
    '''INPUT: a warehouse state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    '''In this case, simply the number of displaced boxes.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage: # storage is a list of tuple
            count += 1
    return count


def nearest_storage(storages, box): # storage:(x, y) box:(x, y)
    s = list(storages)[0] # 1st is the closest storage
    min_distance = pow(pow(abs(s[0] - box[0]), 2) + pow(abs(s[1] - box[1]), 2), .5)
    for storage in list(storages)[1:]:
        cur_distance = pow(pow(abs(storage[0] - box[0]), 2) + pow(abs(storage[1] - box[1]), 2), .5)
        if cur_distance < min_distance:
            min_distance = cur_distance
            s = storage # update the closest storage
    return s


def heur_manhattan_distance(state):

    '''admissible heuristic: manhattan distance'''
    '''INPUT: a warehouse state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    
    #We want an admissible heuristic, which is an optimistic heuristic. 
    #It must always underestimate the cost to get from the current state to the goal.
    #The sum Manhattan distance of the boxes to their closest storage spaces is such a heuristic.  
    #When calculating distances, assume there are no obstacles on the grid and that several boxes can fit in one storage bin.
    #You should implement this heuristic function exactly, even if it is tempting to improve it.
    #Your function should return a numeric value; this is the estimate of the distance to the goal.
    
    ### IMPLEMENT BELOW ###
    if len(state.storage) == 0:
        return 0
    cum_distance = 0
    for box in state.boxes:
        if box not in state.storage:
            s = nearest_storage(state.storage, box)
            md = abs(box[0] - s[0]) + abs(box[1] - s[1]) # Manhattan distance
            cum_distance += md

    ### END OF IMPLEMENTATION ###
    return cum_distance

def fval_fn(sN, w):
    return sN.gval + sN.hval*w


def inf_cost_bound(x):
    return x, x, x


def weighted_astar(initial_state, heuristic, weight, timebound = 10):

    '''Provides an implementation of weighted a-star, as described in the PA2 handout'''
    '''INPUT: a warehouse state that represents the start state, the heursitic to be used,'''
    '''       weight for the A* search (w >= 1), and a timebound (number of seconds)'''
    '''OUTPUT: A WarehouseState (if a goal is found), else False'''
    
    ### IMPLEMENT BELOW ###
    end = os.times()[0] + timebound
    cost_bound = inf_cost_bound(float('inf'))
    searchEngine = SearchEngine('custom', 'full')
    # fval_fn
    wrap_fval_fn = (lambda sN: fval_fn(sN, weight))
    searchEngine.init_search(initial_state, warehouse_goal_state, heuristic, wrap_fval_fn)
    if os.times()[0] < end and weight >= 1:
        state, stats = searchEngine.search(end-os.times()[0], cost_bound)
        if state is False:
            return False
        return state
    return False

    ### END OF IMPLEMENTATION ###


def iterative_astar(initial_state, heuristic, weight, timebound = 10):

    '''Provides an implementation of iterative a-star, as described in the PA2 handout'''
    '''INPUT: a warehouse state that represents the start state, the heursitic to be used,'''
    '''       weight for the A* search (w >= 1), and a timebound (number of seconds)'''
    '''OUTPUT: A WarehouseState (if a goal is found), else False'''
    
    # HINT: Use os.times()[0] to obtain the clock time. Your code should finish within the timebound.'''

    ### IMPLEMENT BELOW ###
    end = os.times()[0] + timebound
    weight = 100
    goal = False
    searchEngine = SearchEngine('custom', 'full')
    while os.times()[0] < end and weight >= 1:
        wrap_fval_fn = (lambda sN: fval_fn(sN, weight))
        searchEngine.init_search(initial_state, warehouse_goal_state,
                                 heuristic, wrap_fval_fn)
        state, stats = searchEngine.search(end - os.times()[0], inf_cost_bound(float('inf')))
        if state is False:
            return False
        else:
            weight = weight * 0.2
            goal = state
    return goal



def robots_boxes_mh(state):
    cum_distance = 0

    for box in state.boxes:
        lst = []
        for robot in state.robots:
            md = abs(robot[0] - box[0]) + abs(robot[1] - box[1])  # Manhattan distance
            lst.append(md)
        cum_distance += min(lst)

    return cum_distance


def unmove_boxes(state, boxes):
    b = [] # return list do not forget
    for box in boxes:
        x = box[0]
        y = box[1]
        #coner
        if (x == 0 and y == 0) or (x == 0 and y == state.height-1) \
                or (x == state.width-1 and y == 0) \
                or (x == state.width-1 and y == state.height-1):
            b.append(box)
        #wall
        elif x == 0 or x == state.width-1:
            if ((x, y-1) in state.obstacles) or ((x, y+1) in state.obstacles):
                b.append(box)
        elif y == 0 or y == state.height-1:
            if ((x-1, y) in state.obstacles) or ((x+1, y) in state.obstacles):
                b.append(box)
        #abstacles
        elif (x-1, y) in state.obstacles and (x, y-1) in state.obstacles:
            b.append(box)
        elif (x-1, y) in state.obstacles and (x, y+1) in state.obstacles:
            b.append(box)
        elif (x+1, y) in state.obstacles and (x, y+1) in state.obstacles:
            b.append(box)
        elif (x+1, y) in state.obstacles and (x, y+1) in state.obstacles:
            b.append(box)
    return b


def unstored_box(state):
    count = 0
    unstored_box = []
    for box in state.boxes:
        if box not in state.storage:  # storage is a list of tuple
            unstored_box.append(box)
            count += 1
    if count != 0:
        return unstored_box
    return count


def unfiiled_storage(state):
    lst = []
    for s in state.storage:
        if s not in state.boxes:
            lst.append(s)
    return lst

def heur_alternate(state):

    '''a better warehouse heuristic'''
    '''INPUT: a warehouse state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''        
  
    #Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    #Your function should return a numeric value for the estimate of the distance to the goal.

    ### IMPLEMENT BELOW ###
    boxes = unstored_box(state)
    if boxes == 0:
        return boxes
    if unmove_boxes(state, boxes) != []:
        return float('inf')
    if len(state.storage) == 0:
        return float('inf')

    cum_distance = 0
    for box in boxes:
        s = nearest_storage(unfiiled_storage(state), box)
        md = abs(box[0] - s[0]) + abs(box[1] - s[1])  # Manhattan distance
        cum_distance += md

    return cum_distance + robots_boxes_mh(state) - 1






