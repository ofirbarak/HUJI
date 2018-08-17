"""
In search.py, you will implement generic search algorithms
"""
from collections import deque
import util


class SearchFringe:
    def __init__(self, state, action, parent, cost_so_far):
        self.state = state
        self.action = action
        self.parent = parent
        self.cost_so_far = cost_so_far

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()



def depth_first_search(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """

    closed = set()
    fringe = util.Stack()
    fringe.push(SearchFringe(problem.get_start_state(), '', None, 0))
    while fringe:
        current = fringe.pop()
        if problem.is_goal_state(current.state):
            return check_path(current)
        if current.state not in closed:
            closed.add(current.state)
            for i in problem.get_successors(current.state):
                node = SearchFringe(i[0], i[1], current,0)
                fringe.push(node)


def check_path(current):
    actions = []
    while current.parent:
        actions.insert(0, current.action)
        current = current.parent
    return actions

def breadth_first_search(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    closed = set()
    fringe = deque([SearchFringe(problem.get_start_state(), '', None,0)])
    while fringe:
        current = fringe.popleft()
        if problem.is_goal_state(current.state):
            return check_path(current)
        if current.state not in closed:
            closed.add(current.state)
            for i in problem.get_successors(current.state):
                node = SearchFringe(i[0], i[1], current, 0)
                fringe.append(node)



def uniform_cost_search(problem):
    """
    Search the node of least total cost first.
    """
    closed = set()
    fringe = util.PriorityQueue()
    fringe.push(SearchFringe(problem.get_start_state(), '', None, 0), 0)
    while fringe:
        current = fringe.pop()
        if problem.is_goal_state(current.state):
            return check_path(current)
        if current.state not in closed:
            closed.add(current.state)
            for i in problem.get_successors(current.state):
                node = SearchFringe(i[0], i[1], current, i[2] + current.cost_so_far)
                fringe.push(node, node.cost_so_far)



def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    closed = set()
    fringe = util.PriorityQueue()
    fringe.push(SearchFringe(problem.get_start_state(), '', None, 0), 0)
    while fringe:
        current = fringe.pop()
        if problem.is_goal_state(current.state):
            return check_path(current)
        if current.state not in closed:
            closed.add(current.state)
            for i in problem.get_successors(current.state):
                node = SearchFringe(i[0], i[1], current, i[2]+current.cost_so_far)
                fringe.push(node, node.cost_so_far + heuristic(i, problem))



# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
