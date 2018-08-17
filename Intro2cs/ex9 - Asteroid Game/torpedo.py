# FILE: torpedo.py
# WRITER: Netanel Faummy, Ofir Birka
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION:  Torpedo class of Asteroids game

############################################################
# CONSTANTS
############################################################

TORPEDO_RADIUS = 4


class Torpedo:

    def __init__(self, pos_x, pos_y, velocity_x, velocity_y,
                 heading, lives=200):
        """
        A constructor for a Torpedo object.
        :param pos_x: position of the torpedo on x-axis.
        :param pos_y: position of the torpedo on y-axis.
        :param velocity_x: velocity of the torpedo on x-axis.
        :param velocity_y: velocity of the torpedo on y-axis.
        :param heading: heading direction to the torpedo.
        """
        # Set location of the asteroid.
        self.pos_x = pos_x
        self.pos_y = pos_y
        # Set velocity of the torpedo.
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        # Set torpedo heading direction in degrees.
        self.heading = heading
        self.radius = TORPEDO_RADIUS
        # Set torpedo lives
        self.lives = lives

    def get_velocity(self):
        """
        This function returns the velocity of torpedo on both axis as tuple.
        """
        return self.velocity_x, self.velocity_y

    def get_position(self):
        """
        This function returns the position of torpedo on both axis as tuple.
        """
        return self.pos_x, self.pos_y

    def set_position(self, pos_x, pos_y):
        """
        This function will set new position to the torpedo.
        :param pos_x - the new x coordinate for torpedo.
        :param pos_y - the new y coordinate for torpedo
        """
        self.pos_x = pos_x
        self.pos_y = pos_y

    def get_torpedo_heading_deg(self):
        """
        This function will return the torpedo heading direction in degrees.
        """
        return self.heading

    def get_radius(self):
        """
        This function returns the torpedo radius.
        """
        return self.radius

    def dec_lives(self):
        """
        Return True- torpedo should disappear, False- otherwise
        :return:
        """
        self.lives -= 1
        if self.lives <= 0:
            return True
        return False
