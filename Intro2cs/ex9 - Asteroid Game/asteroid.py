# FILE: asteroid.py
# WRITER: Netanel Faummy, Ofir Birka
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION:  Asteroid class of Asteroids game

############################################################
# Imports
############################################################

import math
import random
from screen import Screen

############################################################
# CONSTANTS
############################################################

COEFFICIENT_RADIUS_FACTOR = 10  # Factor of given formula
NORMALIZE_RADIUS_FACTOR = 5     # Factor of given formula
X = 0
Y = 1
REVERT_DIRECTION = -1
ASTEROID_DECREASE_SIZE = -1

############################################################
# Asteroid Class
############################################################


class Asteroid:
    """
    Class representing a asteroid object in our Asteroids game.
    """

    def __init__(self, pos_x, pos_y, velocity_x, velocity_y, size = 3):
        """
        A constructor for a asteroid object.
        :param pos_x: position of the asteroid on x-axis.
        :param pos_y: position of the asteroid on y-axis.
        :param velocity_x: velocity of the asteroid on x-axis.
        :param velocity_y: velocity of the asteroid on y-axis.
        :param size: size of the asteroid 1 - 3 (int).
        :return: Asteroid object.
        """
        # Set location of the asteroid.
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Set asteroid's velocity.
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        # Set asteroid's size.
        self.size = size

    def get_position(self):
        """
        This function returns asteroid's position on both axis as tuple.
        """
        return self.pos_x, self.pos_y

    def get_velocity(self):
        """
        This function returns the asteroid's velocity on both axis as tuple.
        """
        return self.velocity_x, self.velocity_y

    def get_size(self):
        """
        This function returns the asteroid's size.
        """
        return self.size

    def get_radius(self):
        """
        This function returns the radius of asteroid. (Given formula)
        """
        return COEFFICIENT_RADIUS_FACTOR * self.size - \
               NORMALIZE_RADIUS_FACTOR

    def set_position(self, pos_x, pos_y):
        """
        This function will set new position to the asteroid.
        :param pos_x - new position coordinate on x axis.
        :param pos_y - new position coordinate on y axis.
        """
        self.pos_x = pos_x
        self.pos_y = pos_y

    def has_intersection(self, other_obj):
        """
        This function will check if the asteroid object have any intersection
        with other object which can be torpedo / ship.
        Return True for intersection and False otherwise.
        :param other_obj - represent object of Torpedo or Ship.
        """
        # Checking if asteroid intersected ship / torpedo object.
        if type(other_obj) != Asteroid:
            # Getting other object position / radius data.
            other_obj_x, other_obj_y = other_obj.get_position()
            other_obj_radius = other_obj.get_radius()
            asteroid_radius = self.get_radius()
            # Calculating the distance between asteroid and other object.
            distance = math.sqrt(math.pow(other_obj_x - self.pos_x, 2) +
                                 math.pow(other_obj_y - self.pos_y, 2))
            # If distance is less then objects radius sum - intersection!
            if distance <= asteroid_radius + other_obj_radius:
                return True
            else:
                return False
        else:
            return False

    def split_asteroid(self, torpedo_speed):
        """
        Split asteroids if asteroid size > 1
        :return: list of divided asteroids
        """
        divided_asteroids = []   # Temp list for the two new asteroids.
        # Checking the hit asteroid size
        if self.size <= 1:
            return divided_asteroids
        # Getting the hit asteroid velocity data.
        velocity_x, velocity_y = self.get_velocity()
        # Calculating denominator of distance formula.
        denominator = math.sqrt(velocity_x**2 + velocity_y**2)
        # Dealing with non-moving asteroid. Avoiding division by zero.
        # Setting new asteroids velocities by given formula
        if denominator == 0:
            new_speed_x = torpedo_speed[X]
            new_speed_y = torpedo_speed[Y]
        else:
            new_speed_x = (torpedo_speed[X] + velocity_x) / denominator
            new_speed_y = (torpedo_speed[Y] + velocity_y) / denominator
        # Creating 2 new asteroids and returning list of two of them.
        divided_asteroids.append(Asteroid(self.pos_x, self.pos_y, new_speed_x,
                                         new_speed_y,
                                         self.size + ASTEROID_DECREASE_SIZE))
        divided_asteroids.append(Asteroid(self.pos_x, self.pos_y,
                                         REVERT_DIRECTION * new_speed_x,
                                         REVERT_DIRECTION * new_speed_y,
                                         self.size + ASTEROID_DECREASE_SIZE))
        return divided_asteroids
