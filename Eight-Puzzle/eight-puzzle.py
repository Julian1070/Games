# This is code that solves the 8-puzzle (and larger puzzles at slower speed). I compare different heuristic functions.

# Import Libraries
from queue import PriorityQueue


# Define Input Test Function
'''
This function makes sure the input is correct. if a) the input dimension 'n' does not match the state or b) the state
itself doesn't match the m-lists with m-values each criteria or c) the state doesn't include each value from 0 to m^2-1
exactly once, then the function returns error code -1. to test whether the state is solvable, i count the number of
inversions (i.e. add the number of values that follow and are greater than each value). if this number is odd, then the
state is not solvable and the function returns error code -2. i found this trick on the internet:
https://math.stackexchange.com/questions/293527/how-to-check-if-a-8-puzzle-is-solvable
'''


def test_input(m, input):
    flat_list = [item for sublist in input for item in sublist if item != 0]  # i exclude 0 from the inversion count
    inversions = 0
    for pos, i in enumerate(flat_list):
        inversions += sum([j < i for j in flat_list[pos:]])
    if not (set([len(input)]) == set([len(x) for x in input]) and m == len(input) and
            sorted([item for sublist in input for item in sublist]) == list(range(0, len(input) ** 2))):
        return [0, 0, -1]
    elif not (inversions % 2 == 0):
        return [0, 0, -2]
    else:
        return False


# Define Heuristic Functions

# counts the number of tiles that aren't in the right position
def Misplc(current_state):
    flat_list = [item for sublist in current_state for item in sublist]
    return len([k for k,x in enumerate(flat_list) if x != k])

# adds together the manhattan distance of each tile
def ManHat(current_state):
    flat_list = [item for sublist in current_state for item in sublist]
    n = len(current_state)
    # i create the a list of coordinates to use for the manhattan distance
    co = [[] for i in range(n**2)]
    for i in range(n):
        for j in range(n):
            co[n*i+j].append(j)
            co[n*i+j].append(i)
    # calculates the sum of the distances for each tile
    dist = sum([abs(co[x][0]-co[k][0])+abs(co[x][1]-co[k][1]) for k,x in enumerate(flat_list)])
    return dist

# doubles the total manhattan distance
def ManHat2(current_state):
    return 2 * ManHat(current_state)

# squares the total manhattan distance
def ManHat3(current_state):
    return ManHat(current_state)**2

# list with the heuristic functions
heuristics = [Misplc, ManHat, ManHat2, ManHat3]


# Class and Conversion (list<->tuple) Functions

# converts the lists in list format to a tuple to be compatible with dict (all alternatives i found required extra
# libraries and it was too late to ask whether i can use them. also, it would have taken me too long to figure out
# probably. anyways, i realize that this may not be the most efficient way of dealing with the dict issue...)
def convert(n_lists):
    return tuple([item for sublist in n_lists for item in sublist])

# converts the tuple back to lists in list (which i need later on)
def unconvert(a_tuple):
    return [list(a_tuple[x:x+int(len(a_tuple)**(0.5))]) for x in range(0, len(a_tuple), int(len(a_tuple)**(0.5)))]

# defines the class
class PuzzleNode:
    def __init__(self, state, fval, gval, parent=None):
        self.state = convert(state) # here i use the tuple
        self.fval = fval # heuristic value + steps taken
        self.gval = gval # steps taken
        self.parent = parent
        self.pruned = False # true if state has been reached more efficiently

    # the following two are blackboxes to me -- i took this from the code from class 3.1 (i'd really appreciate a brief
    # comment regarding where in the code these two functions are used. or maybe i can ask in office hours!?)
    def __lt__(self, other):
        return self.fval < other.fval

    def __str__(self):
        return str(self.state)

# Define Solving Puzzle Function

# the solvePuzzle function. i called the last variable "print_it" because "print" (as proposed) messes with my code.
def solvePuzzle(n, state, heuristic, print_it=False):
    check = test_input(n, state) # tests input and returns error if applicable
    if check:
        return check
    # the following code is very similar to the code from class 3.1. i'll comment where i adapted things and where i
    # think i need to show my understanding. the priority queue, goal test, pruning, etc. is the same
    start = state
    goal = tuple(range(0,len(state)**2)) # i use a tuple because self.state is also a tuple
    start_node = PuzzleNode(state, heuristic(state), 0)
    cost_db = {convert(start):start_node}
    frontier = PriorityQueue()
    frontier.put(start_node)
    moves = [[1,0], [0,1], [-1,0], [0,-1]]
    #expansion_counter = 0 # i included this for fun, but since i'm not using it i'm commenting it out
    max_frontier = 0 # keeps track of the biggest frontier
    while not frontier.empty():
        # chosing the node with the smalles f value (combination of step cost and heuristic cost) to expand
        cur_node = frontier.get()
        # skip if node has been pruned (i.e. when state has been reached more efficiently)
        if cur_node.pruned:
            continue
        # goal test to stop when goal is reached
        if cur_node.state == goal:
            break
        # here i'm finding the coordinates for 0 because that's the tile to be moved (conceptually)
        for row_number, row in enumerate(unconvert(cur_node.state)):
            if 0 in row:
                zero = (row_number, row.index(0))
        # going through all the moves
        for m in moves:
            # this is the coordinate of the tile that is switched with 0, given move m
            other = [x + y for x, y in zip(zero, m)]
            # ensuring that the move is legal (i.e. other tile's coordinates are within boundaries)
            if all([0<=z<n for z in other]):
                # tentatively increasing gval based on step cost
                gval = cur_node.gval + 1
                next_state = list(unconvert(cur_node.state))
                # switching tile 0 with the other tile
                next_state[zero[0]][zero[1]], next_state[other[0]][other[1]] = next_state[other[0]][other[1]], \
                                                                               next_state[zero[0]][zero[1]]

                # checks (and prunes if applicable) if state has occured before
                tup_next_state = convert(next_state)
                if tup_next_state in cost_db:
                    # this tests which path is more efficient...
                    if cost_db[tup_next_state].gval > gval:
                        # ...and prunes if less efficient
                        cost_db[tup_next_state].pruned = True
                    else:
                        continue

                # calculates the heuristic cost based on heuristic function used
                hval = heuristic(next_state)
                next_node = PuzzleNode(next_state,gval+hval,gval,cur_node)
                frontier.put(next_node)
                cost_db[convert(next_state)] = next_node
                # updating the maximum frontier size if applicable
                if frontier.qsize() > max_frontier:
                    max_frontier = frontier.qsize()
        # expansion_counter = expansion_counter + 1 # i included this for fun, but since i'm not using it i'm commenting
        # it out

    # reconstrucs optimal path found (not necessarily global optimum due to heuristic)
    optimal_path = [unconvert(cur_node.state)] # optimal path starts with current node because it is the most efficient
    # path to the goal state that was found based on heuristic cost and step cost
    # walking up the path using the parent-child node connection
    while cur_node.parent:
        optimal_path.append(unconvert((cur_node.parent).state))
        cur_node = cur_node.parent
    optimal_path = optimal_path[::-1]

    if print_it:
        print("Number of moves: %d\n"% len(optimal_path))
        print("Maximum frontier size: %d\n"% max_frontier)
        print("Optimal Path to Goal:", optimal_path)
    else:
        return [len(optimal_path), max_frontier, 0]


# Comparing Heuristics Function

def compHeur():
    results = [["State", "Heuristic", "Length of Path", "Maximum Frontier Size", "Error Code"]]
    states = [[[5,7,6],[2,4,3],[8,1,0]], [[7,0,8],[4,6,1],[5,3,2]], [[2,3,7],[1,8,0],[6,5,4]]] # the states you gave us
    # for each state...
    for state_count, state in enumerate(states):
        # ...and each heuristic...
        for heu_count, heuristic in enumerate(heuristics):
            # ...solve the puzzle
            results.append(["State %d, Heuristic %d"%(state_count+1,heu_count+1)] + solvePuzzle(3, state, heuristic))
    for result in results:
        print(result)

compHeur()
