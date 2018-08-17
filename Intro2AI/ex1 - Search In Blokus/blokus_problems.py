from board import Board
from search import SearchProblem, ucs
import util
import math
from search import SearchFringe


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)



#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.targets = [(0,0), (board_w-1, 0), (board_w-1, board_h-1), (0, board_h -1)]

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        pieces = state.state
        if pieces[0][0] == pieces[0][self.board.board_w-1]:
            if pieces[0][self.board.board_w-1] == pieces[self.board.board_h-1][self.board.board_w-1]:
                if pieces[self.board.board_h-1][self.board.board_w-1] == pieces[self.board.board_h-1][0]:
                    if pieces[self.board.board_h-1][0] != -1:
                        return True
        return False


    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles())
                for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        sum_of_actions = 0
        piece_list = self.board.piece_list
        for action in actions:
            id = action.piece_index
            piece = piece_list.get_piece(id)
            sum_of_actions += piece.get_num_tiles()
        return sum_of_actions


def is_valid_tile(point, board):
    if point[0] == 0:
        if point[1] == len(board[0]) - 1:
            if board[point[0]][point[1]-1] == -1 and board[point[0]+1][point[1]] == -1 and board[point[0]+1][point[1] -1] != -1:
                return True
            return False
        else:
            if board[point[0]][point[1]-1] == -1 and board[point[0]][point[1]+1] == -1 and board[point[0]+1][point[1]] == -1 and (board[point[0]+1][point[1]-1] != -1 \
                or board[point[0]+1][point[1] +1] != -1):
                return True
            return False

    if point[0] == len(board) - 1:
        if point[1] == len(board[0]) - 1:
            if board[point[0]][point[1]-1] == -1 and board[point[0]-1][point[1]] == -1 and board[point[0]-1][point[1]-1] != -1:
                return True
            return False
        if point[1] == 0:
            if board[point[0] -1][point[1]] == -1 and board[point[0]][point[1]+1] == -1 and board[point[0]-1][point[1] +1] != -1:
                return True
            return False
        else:
            if board[point[0]][point[1]-1] == -1 and board[point[0]][point[1]+1] == -1 and board[point[0]-1][point[1]] == -1 and (board[point[0]-1][point[1]-1] != -1 or board[point[0]-1][point[1]+1] != -1):
                return True
            return False

    if point[1] == 0:
        if board[point[0]+1][point[1]] == -1 and board[point[0]][point[1]+1]==-1 and board[point[0]-1][point[1]]==-1 and (board[point[0]-1][point[1]+1] != -1 or board[point[0]+1][point[1]+1] != -1):
            return True
        return False

    if point[1] == len(board[0]) - 1:
        if board[point[0] - 1][point[1]] == -1 and board[point[0]+1][point[1]] == -1 and board[
            point[0]][point[1] - 1] == -1 and (board[point[0]+1][point[1]-1] != -1 or board[point[0]-1][point[1]-1] != -1):
            return True
        return False

    if board[point[0] - 1][point[1]] == -1 and board[point[0]][point[1] - 1] == -1 and board[
        point[0]][point[1] + 1] == -1 and board[point[0]+1][point[1]] == -1:
        if board[point[0]-1][point[1]-1] != -1 or board[point[0]+1][point[1]-1] != -1 or board[point[0]-1][point[1]+1] != -1 or board[point[0]+1][point[1]+1] != -1:
            return True
    return False

def distance_to_all_targets(point,board, targets):
    penalty = 0
    for target in targets:
        if board[target[0]][target[1]] == -1:
           penalty += util.manhattanDistance(target, point) - 1
    if penalty == 0:
        return 0
    return penalty + 1



def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    targets = problem.targets
    num_tiles = state[0].state
    penalty = 1000
    for i in range(len(num_tiles)):
        for j in range(len(num_tiles[0])):
            if is_valid_tile((i, j), num_tiles):
                new_penalty = distance_to_all_targets((i,j),num_tiles, targets)
                if new_penalty < penalty:
                    penalty = new_penalty
    return penalty







class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        pieces = state.state
        for target in self.targets:
            if pieces[target[0]][target[1]] == -1:
                return False
        return True


    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        sum_of_actions = 0
        piece_list = self.board.piece_list
        for action in actions:
            id = action.piece_index
            piece = piece_list.get_piece(id)
            sum_of_actions += piece.get_num_tiles()
        return sum_of_actions


def blokus_cover_heuristic(state, problem):
    targets = problem.targets
    num_tiles = state[0].state
    penalty = 100000
    for i in range(len(num_tiles)):
        for j in range(len(num_tiles[0])):
            if is_valid_tile((i, j), num_tiles):
                new_penalty = distance_to_all_targets((i, j), num_tiles, targets)
                if new_penalty < penalty:
                    penalty = new_penalty
    return penalty

def check_path(current):
    actions = []
    while current.parent:
        actions.insert(0, current.action)
        current = current.parent
    return actions

class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board


    def get_closest_target(self, nearest_target, reached_all_targets):
        min_target = 1000
        min_index = 0
        for i in range(0, len(self.targets)):
            if util.manhattanDistance(self.targets[i],nearest_target)< min_target and reached_all_targets[i] == False:
                min_target = util.manhattanDistance(self.targets[i],nearest_target)
                min_index = i
        return min_index



    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        actions = []
        backtrace = []
        reached_all_targets = [False] * len(self.targets)
        nearest_target = self.starting_point
        index = self.get_closest_target(nearest_target, reached_all_targets)
        problem = BlokusCoverProblem(self.board.board_w, self.board.board_h, self.board.piece_list,
                                     self.starting_point, [self.targets[index]])
        current_state = problem.get_start_state()
        while not all(reached_all_targets):
            index = self.get_closest_target(nearest_target, reached_all_targets)
            reached_all_targets[index] = True
            nearest_target = self.targets[index]
            problem = BlokusCoverProblem(self.board.board_w, self.board.board_h, self.board.piece_list,
                                         self.starting_point, [nearest_target])
            closed = set()
            fringe = util.PriorityQueue()
            fringe.push(SearchFringe(current_state, '', None, 0), 0)
            while fringe:
                current = fringe.pop()
                if problem.is_goal_state(current.state):
                    actions = check_path(current)
                    break
                if current.state not in closed:
                    closed.add(current.state)
                    for i in problem.get_successors(current.state):
                        node = SearchFringe(i[0], i[1], current, i[2] + current.cost_so_far)
                        fringe.push(node, node.cost_so_far + blokus_cover_heuristic(i,problem))
            for action in actions:
                current_state = current_state.do_move(0, action)
            backtrace += actions
            self.expanded += problem.expanded
        return backtrace




class MiniContestSearch :
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board


    def solve(self):
        util.raiseNotDefined()


