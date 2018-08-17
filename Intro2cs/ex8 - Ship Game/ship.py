#######################################
# FILE : ex8.py
# WRITER : Ofir_Birka , ofir , *********
# EXERCISE : intro2cs ex8 2015-2016
# DESCRIPTION: Ship Game
#######################################
# Imports
import ship_helper
import copy

# Constants
BEGIN_BORDER = 0
FIRST_CELL = 1
SHIP_PACE = 1
Y = 1
X = 0


############################################################
# Helper class
############################################################


class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

    NOT_MOVING = 0

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

    def ret_opposite_direction(direct):
        '''
        Return the opposite direction in moving path
        '''
        return {
            Direction.UP : Direction.DOWN,
            Direction.DOWN : Direction.UP,
            Direction.RIGHT : Direction.LEFT,
            Direction.LEFT : Direction.RIGHT,
            Direction.NOT_MOVING : Direction.NOT_MOVING
        }[direct]


############################################################
# Class definition
############################################################


class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction to
    the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """

    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        self.__pos = pos
        self.__length = length
        self.__direct = direction
        # ship state - vertical or horizontal
        self.__state = Direction.HORIZONTAL
        if direction in Direction.VERTICAL:
            self.__state = Direction.VERTICAL
        self.__board_side = board_size
        self.__damaged_cells_list = []


    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string. The tuple's content should be (in
        the exact following order):
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """
        return str((self.coordinates(),
                    self.__damaged_cells_list,
                    ship_helper.direction_repr_str(Direction,
                                                   self.direction()),
                    self.__board_side))

    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement would
        take it outside of the board in which case the shp switches direction
        and sails one board unit in the new direction.
        the ship
        :return: A direction object representing the current movement direction.
        """
        if len(self.__damaged_cells_list) == 0:
            if self.__direct == Direction.UP:
                self.update_with_given_direction(Y, Direction.UP)
            elif self.__direct == Direction.DOWN:
                self.update_with_given_direction(Y, Direction.DOWN)
            elif self.__direct == Direction.RIGHT:
                self.update_with_given_direction(X, Direction.RIGHT)
            else:
                self.update_with_given_direction(X, Direction.LEFT)
        else:
            self.__direct = Direction.NOT_MOVING
        return self.__direct

    def update_with_given_direction(self, coord, direct):
        '''
        Help function for 'move'. Update the position of a ship
        :param coord: X or Y
        :param direction: (RIGHT, DOWN, LEFT, UP)
        '''
        coord_list = list(self.__pos)
        # Whether to check limit with end border of begin border
        if direct == Direction.LEFT or direct == Direction.UP:
                if coord_list[coord] <= BEGIN_BORDER:
                    coord_list[coord] = FIRST_CELL
                    self.__direct = \
                        Direction.ret_opposite_direction(direct)
                else:
                    coord_list[coord] -= SHIP_PACE
        else:
            if coord_list[coord]+self.__length < self.__board_side:
                coord_list[coord] += SHIP_PACE
            else:
                coord_list[coord] = int(self.__board_side) - 1 \
                                    - int(self.__length)
                self.__direct = Direction.ret_opposite_direction(direct)
        self.__pos = tuple(coord_list)

    def hit(self, pos):
        """
        Inform the ship that a bomb hit a specific coordinate. The ship updates
         its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
         in future turns. If all ship's body's coordinate are hit, the ship is
         terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
         otherwise.
        """
        if self.__contains__(pos) and not self.terminated() and \
                        pos not in self.__damaged_cells_list:
            # Hit
            self.__direct = Direction.NOT_MOVING
            self.__damaged_cells_list.append(pos)
            return True
        return False

    def terminated(self):
        """
        :return: True if all ship's coordinates were hit in previous turns, False
        otherwise.
        """
        if len(self.__damaged_cells_list) == self.__length:
            return True
        return False

    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the given
        (x, y) coordinates, False otherwise.
        """
        in_ship = False
        if pos in self.coordinates():
            in_ship = True
        return in_ship

    def coordinates(self):
        """
        Return ship's current positions on board.
        :return: A list of (x, y) tuples representing the ship's current
        position.
        """
        if self.__state == Direction.VERTICAL:
            return self.get_coordinates(self.__pos[Y], self.__pos[X], X)
        return self.get_coordinates(self.__pos[X], self.__pos[Y], Y)

    def get_coordinates(self, coord, value_permanent_coord, permanent_coord):
        coordinates_list = []
        for value in range(coord,
                           self.__length+coord):
            if permanent_coord == X:
                coordinates_list.append((value_permanent_coord, value))
            else:
                coordinates_list.append((value, value_permanent_coord))
        return coordinates_list

    def damaged_cells(self):
        """
        Return the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        return copy.deepcopy(self.__damaged_cells_list)

    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current
         sailing direction or NOT_MOVING if the ship is hit and not moving.
        """
        return copy.deepcopy(self.__direct)

    def cell_status(self, pos):
        """
        Return the state of the given coordinate (hit\not hit)
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None 
        """
        if not self.__contains__(pos):
            return None
        if pos in self.__damaged_cells_list:
            return True
        return False

