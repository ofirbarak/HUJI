#######################################
# FILE : ex8.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex8 2015-2016
# DESCRIPTION: Ship Game
#######################################
# Constants
X = 0
Y = 1
TURNS = 4
MIN_NUMBER_TURNES = 1
INITIALIZE_VALUE = 0

############################################################
# Imports
############################################################
import game_helper as gh
import copy

############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board
        :param ships: A list of ships that participate in the game.
        """
        self.__board_size = board_size
        self.__bombs = {}       # All coordinates (x,y) bombs
        self.__hits = []        # All coordinates (x,y) hits
        self.__hit_ships = []   # List of ship that was hit
        self.__ships = ships    # List of all ship that was not terminated
        self.__coord_ships_not_hit = [] # List of coordinates of ships that
                                            # were not hit

    def __play_one_round(self):
        """
        Te function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits and
             terminated ships)
        """
        target = gh.get_target(self.__board_size)
        # Put the bomb on board
        self.__bombs[target] = TURNS
        current_hits_list = []
        number_of_terminated_in_current_turn = INITIALIZE_VALUE
        number_of_hit_ships_in_current_turn = INITIALIZE_VALUE
        # 1. Move the ships if it was not hit
        # 2. Each ship that moved, check if a bomb (including the new target)
        #       hit in ship in the new location
        # 3. For all not moved ships check if the new target hits
        for ship in self.__ships:
            # Step 1:
            if ship not in self.__hit_ships:
                ship.move()
                # Step 2:
                previous_damaged_cells = tuple(ship.damaged_cells())
                for bomb in self.__bombs:
                    ship.hit(bomb)
                if len(ship.damaged_cells()) != len(previous_damaged_cells):
                    self.__hit_ships.append(ship)
                    for cell in ship.damaged_cells():
                        self.__hits.append(cell)
                        number_of_hit_ships_in_current_turn += 1
                        current_hits_list.append(cell)
            # Step 3:
            else:
                if ship.hit(target):
                    current_hits_list.append(target)
                    self.__hits.append(target)
                    number_of_hit_ships_in_current_turn += 1
        # Decrease bombs turns
        ezer_dict_bombs = copy.deepcopy(self.__bombs)
        for index_bomb in ezer_dict_bombs:
            self.__bombs[index_bomb] -= 1
            if  self.__bombs[index_bomb] < MIN_NUMBER_TURNES or \
                            index_bomb in current_hits_list:
                del self.__bombs[index_bomb]
        # Print board
        print(gh.board_to_string(self.__board_size, current_hits_list, self.__bombs,
                           self.__hits, self.get_coordinates_from_ship_list()))
        # Check if ship terminated
        for ship in self.__ships:
            if ship.terminated():
                number_of_terminated_in_current_turn += 1
                self.__hit_ships.remove(ship)
                self.__ships.remove(ship)
                for cell in ship.coordinates():
                    self.__hits.remove(cell)
        # Report
        gh.report_turn(number_of_hit_ships_in_current_turn,
                       number_of_terminated_in_current_turn)

    def __repr__(self):
        """
        Return a string representation of the board's game
        :return: A tuple converted to string. The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        ships_repr = []
        for ship in self.__ships:
            ships_repr.append(eval(ship.__repr__()))
        return str((self.__board_size, self.__bombs, ships_repr))

    def get_coordinates_from_ship_list(self):
        list_coordinates = []
        for ship in self.__ships:
            list_coordinates.extend(ship.coordinates())
        return list_coordinates

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        completion.
        :return: None
        """
        gh.report_legend()
        print(gh.board_to_string(self.__board_size, [],
                                 self.__bombs,
                                 self.__hits,
                                 self.get_coordinates_from_ship_list()))
        while len(self.__ships) > 0:
            self.__play_one_round()
        gh.report_gameover()


############################################################
# An example usage of the game
############################################################
if __name__=="__main__":
    game = Game(4, gh.initialize_ship_list(3, 2))
    game.play()
