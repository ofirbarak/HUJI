import numpy as np
import abc
import util
from game_state import GameState
import game_state as gs
from game import Agent, Action
import math




class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)

        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score
        open_squares = len(successor_game_state.get_empty_tiles())
        score += 2*(open_squares - len(current_game_state.get_empty_tiles()))
        for i in range(0,len(board)):
            for j in range(0,len(board[0])):
                if i == 0 and j == 0:
                    if board[0][0] == board[1][0] > 0 or board[0][0] == board[0][1] > 0:
                        score += board[0][0]
                    continue
                if i == 0 and j == len(board[0]) - 1:
                    if board[0][len(board[0])-1] == board[1][len(board[0])-1] > 0 or board[0][len(board[0])-1] == \
                            board[0][len(board[0]) - 2] > 0:
                        score += board[0][len(board[0])-1]
                    continue
                if i == 0:
                    if board[0][j]==board[0][j-1] > 0 or board[0][j] == board[0][j+1]>0 or board[1][j] == board[0][j] >0:
                        score += board[0][j]
                    continue
                if i == len(board) - 1 and j == 0:
                    if board[i][j] == board[i-1][j] > 0 or board[i][j] == board[i][j+1] >0:
                        score += board[i][j]
                    continue
                if i == len(board) - 1 and j == len(board[0]) - 1:
                    if board[i][j] == board[i-1][j]>0 or board[i][j] == board[i][j-1] > 0:
                        score += board[i][j]
                    continue
                if i == len(board) - 1:
                    if board[i][j] == board[i][j - 1] > 0 or board[i][j] == board[i][j + 1] > 0 or board[i][j] == \
                            board[i-1][j] > 0:
                        score += board[i][j]
                    continue
                if j == 0:
                    if board[i][j] == board[i+1][j] > 0 or board[i][j] == board[i-1][j] >0 or board[i][j] == board[i][j+1]>0:
                        score+= board[i][j]
                    continue
                if j == len(board[0])-1:
                    if board[i][j] == board[i+1][j] > 0 or board[i][j] == board[i-1][j] >0 or board[i][j] == board[i][j-1]>0:
                        score+= board[i][j]
                    continue
                if board[i][j] == board[i + 1][j] > 0 or board[i][j] == board[i - 1][j] > 0 or board[i][j] == board[i][j - 1] > 0 or \
                        board[i][j] == board[i][j+1]:
                    score+=board[i][j]
        return score


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):

    def minimax(self, game_state, depth, player_turn):
        if depth >= 2*self.depth:
            return self.evaluation_function(game_state), Action.STOP
        else:
            if player_turn % 2 == 0:
                maximizer = float("-inf")
                maximizer_action = Action.STOP
                successors = []
                if not game_state.get_legal_actions(0):
                    return self.evaluation_function(game_state), maximizer_action
                for action in game_state.get_legal_actions(0):
                    successors.append(game_state.generate_successor(0, action))
                for i in range(len(successors)):
                    new_value = self.minimax(successors[i], depth + 1, 1)[0]
                    if maximizer < new_value:
                        maximizer = new_value
                        maximizer_action = game_state.get_legal_actions(0)[i]
                return maximizer, maximizer_action
            if player_turn % 2 == 1:
                minimizer = float("+inf")
                minimizer_action = Action.STOP
                successors = []
                if not game_state.get_legal_actions(1):
                    return self.evaluation_function(game_state), minimizer_action
                for action in game_state.get_legal_actions(1):
                    successors.append(game_state.generate_successor(1, action))
                for i in range(len(successors)):
                    new_value = self.minimax(successors[i], depth + 1, 0)[0]
                    if minimizer > new_value:
                        minimizer = new_value
                        minimizer_action = game_state.get_legal_actions(1)[i]
                return minimizer, minimizer_action


    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        action = self.minimax(game_state, 0, 0)[1]
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def alphabeta(self, game_state, depth, player_turn, alpha, beta):
        if depth >= 2*self.depth:
            return self.evaluation_function(game_state), Action.STOP
        else:
            if player_turn % 2 == 0:
                maximizer = float("-inf")
                maximizer_action = Action.STOP
                successors = []
                if not game_state.get_legal_actions(0):
                    return self.evaluation_function(game_state), maximizer_action
                for action in game_state.get_legal_actions(0):
                    successors.append(game_state.generate_successor(0, action))
                for i in range(len(successors)):
                    new_value = self.alphabeta(successors[i], depth + 1, 1, alpha, beta)[0]
                    if maximizer < new_value:
                        maximizer = new_value
                        maximizer_action = game_state.get_legal_actions(0)[i]
                    if new_value >= beta:
                        return new_value, maximizer_action
                    alpha = alpha if alpha > new_value else new_value
                return maximizer, maximizer_action
            if player_turn % 2 == 1:
                minimizer = float("+inf")
                minimizer_action = Action.STOP
                successors = []
                if not game_state.get_legal_actions(1):
                    return self.evaluation_function(game_state), minimizer_action
                for action in game_state.get_legal_actions(1):
                    successors.append(game_state.generate_successor(1, action))
                for i in range(len(successors)):
                    new_value = self.alphabeta(successors[i], depth + 1, 0, alpha, beta)[0]
                    if minimizer > new_value:
                        minimizer = new_value
                        minimizer_action = game_state.get_legal_actions(1)[i]
                    if new_value <= alpha:
                        return new_value, minimizer, action
                    beta = beta if beta < new_value else new_value
                return minimizer, minimizer_action


    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """*** YOUR CODE HERE ***"""
        action = self.alphabeta(game_state, 0,0, float("-inf"), float("+inf"))[1]
        return action


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """
    def expecti_max(self, game_state, depth, player_turn):
        if depth >= 2*self.depth:
            return self.evaluation_function(game_state), Action.STOP
        else:
            if player_turn % 2 == 0:
                maximizer = float("-inf")
                maximizer_action = Action.STOP
                successors = []
                if not game_state.get_legal_actions(0):
                    return self.evaluation_function(game_state), maximizer_action
                for action in game_state.get_legal_actions(0):
                    successors.append(game_state.generate_successor(0, action))
                for i in range(len(successors)):
                    new_value = self.expecti_max(successors[i], depth + 1, 1)[0]
                    if maximizer < new_value:
                        maximizer = new_value
                        maximizer_action = game_state.get_legal_actions(0)[i]
                return maximizer, maximizer_action
            if player_turn % 2 == 1:
                expectation = 0
                expectation_answer = Action.STOP
                sons_value = []
                successors = []
                if not game_state.get_legal_actions(1):
                    return self.evaluation_function(game_state), expectation_answer
                for action in game_state.get_legal_actions(1):
                    successors.append(game_state.generate_successor(1, action))
                for i in range(len(successors)):
                    new_value = self.expecti_max(successors[i], depth + 1, 0)[0]
                    sons_value.append(new_value)
                for value in sons_value:
                    expectation += 1/len(sons_value) * value
                return expectation, expectation_answer
    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """*** YOUR CODE HERE ***"""

        action = self.expecti_max(game_state, 0, 0)[1]
        return action


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    board = current_game_state.board
    max_tile = current_game_state.max_tile
    score = current_game_state.score
    open_squares_score = len(current_game_state.get_empty_tiles())
    board_x = board.shape[0]
    board_y = board.shape[1]
    big_board1 = np.ones((board_x + 2, board_y + 2))
    big_board1[1:1 + board_x, 1:1 + board_y] = board

    weight_matrix = [15,14,13,12,
                     8,9,10,11,
                     7,6,5,4,
                     0,1,2,3]

    thershold = 50
    if (board[0,2] - board[0,3]) < -thershold or \
            (board[0,1] - board[0,2]) < -thershold or \
            (board[0,0] - board[0,1]) < -thershold:
        #(board[1, 1] - board[1, 0]) >= thershold or (board[1,2] - board[1,1]) >= thershold or (board[1,3] - board[1,2]) >= thershold:
        weight_matrix = [15,14,13,12,
                         13,12,10,11,
                         7,6,5,4,
                         0,1,2,3]

    weight_matrix = np.array(weight_matrix).reshape(board.shape)

    score *= np.sum((4**weight_matrix)*board)

    return score


# Abbreviation
better = better_evaluation_function
