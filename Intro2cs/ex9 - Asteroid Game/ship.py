# FILE: ship.py
# WRITER: Netanel Faummy, Ofir Birka
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION:  Ship class of Asteroids game

############################################################
# Imports
############################################################

import math
from screen import Screen
import torpedo
import random

############################################################
# CONSTANTS
############################################################

CONVERT_DEG_TO_RAD = math.pi / 180
RIGHT_DIRECTION = 6             # Representing the right direction as integer
LEFT_DIRECTION = 4              # Representing the left direction as integer
HEADING_DEGREE_CHANGE_LEFT = 7  # Representing the degrees change for heading
HEADING_DEGREE_CHANGE_RIGHT = -7# Representing the degrees change for heading
SHIP_RADIUS = 1                 # Ship radius.
SHIP_INITIAL_LIVES = 3          # Ship initial lives.
TORPEDO_ACCELERATOR_FACTOR = 2

############################################################
# Ship Class
############################################################


class Ship:
    """
    Class representing a space-ship in out asteroid game.
    """

    def __init__(self, random_pos):
        """
        A constructor for a Ship object.
        :return: Ship object
        """
        self.pos_x, self.pos_y = random_pos
        # Set ship velocity to 0.
        self.velocity_x = 0
        self.velocity_y = 0
        # Set ship heading direction to 0 degrees, paralleled to x axis.
        self.heading = 0
        # Set ship lives to 3 by default.
        self.lives = SHIP_INITIAL_LIVES

    def get_position(self):
        """
        This function returns the position of ship on both axis as tuple.
        """
        return self.pos_x, self.pos_y

    def get_velocity(self):
        """
        This function returns the velocity of ship on both axis as tuple.
        """
        return self.velocity_x, self.velocity_y

    def get_ship_heading_rad(self):
        """
        This function returns the ship's heading direction in radians.
        """
        return self.heading * CONVERT_DEG_TO_RAD

    def get_ship_heading_deg(self):
        """
        This function will return the ship heading direction in degrees.
        """
        return self.heading

    def get_radius(self):
        """
        This function returns the constant radius of the ship.
        """
        return SHIP_RADIUS

    def set_position(self, pos_x, pos_y):
        """
        This function will set new position to the ship.
        :param pos_x - the new x coordinate for ship.
        :param pos_y - the new y coordinate for ship
        """
        self.pos_x = pos_x
        self.pos_y = pos_y

    def set_heading(self, pressed_key):
        """
        This function will set the ship heading direction according to the
        key was pressed.
        :param pressed_key: can be Right / Left keys
        (given by is_right/left_pressed functions designed by course's staff)
        """
        if pressed_key == RIGHT_DIRECTION:
            self.heading += HEADING_DEGREE_CHANGE_RIGHT
        elif pressed_key == LEFT_DIRECTION:
            self.heading += HEADING_DEGREE_CHANGE_LEFT

    def accelerate(self):
        """
        This function will accelerate the ship speed by the given formula.
        """
        current_heading_in_radian = self.get_ship_heading_rad()
        self.velocity_x += math.cos(current_heading_in_radian)
        self.velocity_y += math.sin(current_heading_in_radian)

    def dec_life(self):
        """
        This function will decrease ship's lives by 1.
        """
        self.lives -= 1

    def is_dead(self):
        """
        Return True - if ship is out of lives
        otherwise return False.
        """
        if self.lives <= 0:
            return True
        return False

    def create_torpedo(self):
        """
        This function will create a torpedo using the Torpedo
        class constructor
        """
        # Setting torpedo velocity on both axis by given formula.
        torpedo_velocity_x = self.velocity_x + TORPEDO_ACCELERATOR_FACTOR \
                                    * math.cos(self.get_ship_heading_rad())
        torpedo_velocity_y = self.velocity_y + TORPEDO_ACCELERATOR_FACTOR \
                                    * math.sin(self.get_ship_heading_rad())
        # Creating a new torpedo object with current ship position
        #  and heading
        # direction, with new velocity.
        return torpedo.Torpedo(self.pos_x, self.pos_y, torpedo_velocity_x,
                                            torpedo_velocity_y, self.heading)
