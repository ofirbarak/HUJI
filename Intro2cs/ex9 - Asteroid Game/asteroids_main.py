# FILE: asteroids_main.py
# WRITER: Netanel Faummy, Ofir Birka
# EXERCISE: intro2cs ex9 2015-2016
# DESCRIPTION:  Main game loop of the Asteroids game

############################################################
# Imports
############################################################
from screen import Screen
import sys
import ship
import asteroid
import torpedo
import copy
import random

############################################################
# CONSTANTS
############################################################

INITIAL_GAME_SCORE = 0
DEFAULT_ASTEROIDS_NUM = 5
TORPEDO_SHOT_LIMIT = 15
X = 0
Y = 1
POINTS_FOR_ASTEROID_SIZE_3 = 20
POINTS_FOR_ASTEROID_SIZE_2 = 50
POINTS_FOR_ASTEROID_SIZE_1 = 100
GAME_OVER = 1
GAME_WON = 2

############################################################
# GameRunner Class
############################################################


class GameRunner:
    def __init__(self, asteroids_amnt=3):
        self._screen = Screen()
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.score = INITIAL_GAME_SCORE
        self.torpedoes = []
        self.ship = ship.Ship(self.get_x_y_random_values())
        self.asteroids = []
        for i in range(asteroids_amnt):
            # Create a good asteroid
            asteroid_location = self.get_x_y_random_values()
            while asteroid_location == self.ship.get_position():
                asteroid_location = self.get_x_y_random_values()
            asteroid_velocity = self.get_velocity_x_y_random()
            new_asteroid = asteroid.Asteroid(asteroid_location[X],
                                             asteroid_location[Y],
                                             asteroid_velocity[X],
                                             asteroid_velocity[Y])
            self.asteroids.append(new_asteroid)
            self._screen.register_asteroid(new_asteroid,
                                           new_asteroid.get_size())

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        self.check_if_game_end()
        self.check_which_key_pressed()
        self.move_objects_on_turn()
        # Check hits in asteroids
        for asteroid in self.asteroids:
            # Check if ship was hit by an asteroid
            if asteroid.has_intersection(self.ship):
                self._screen.show_message("asteroid_hit_ship",
                                          "Ship was hit by an asteroid")
                self._screen.remove_life()
                if asteroid in self.asteroids:
                    self.asteroids.remove(asteroid)
                    self._screen.unregister_asteroid(asteroid)
                self.ship.dec_life()
            else:
                for torpedo in copy.deepcopy(self.torpedoes):
                    # Check if torpedo hit asteroid
                    if asteroid.has_intersection(torpedo):
                        self.add_points(asteroid.get_size())
                        if asteroid in self.asteroids:
                            self.asteroids.remove(asteroid)
                            self._screen.unregister_asteroid(asteroid)
                        new_sub_asteroids = \
                            asteroid.split_asteroid(torpedo.get_velocity())
                        self.asteroids.extend(new_sub_asteroids)
                        # register the new asteroids to screen
                        for sub_asteroid in new_sub_asteroids:
                            self._screen.register_asteroid(
                                sub_asteroid, sub_asteroid.get_size())
                            self.draw_object(sub_asteroid)
                        if torpedo in self.torpedoes:
                            self.torpedoes.remove(torpedo)
                            self._screen.unregister_torpedo(torpedo)

    def check_if_game_end(self):
        """
        Check if game end:
            1. All asteroids destroyed
            or 2. Were out of life
            or 3. 'q' was pressed
        """
        title = ''
        message = ''
        if self._screen.should_end() or \
                self.ship.is_dead() or \
                        len(self.asteroids) <= 0:
            title = 'GAMEOVER'
            message = 'Good luck next time:)'
            if len(self.asteroids) <= 0:
                title = 'Game Ended'
                message = 'You have won'
            self._screen.show_message(title, message)
            self._screen.end_game()
            sys.exit()

    def check_which_key_pressed(self):
        '''
        Check which key was pressed:
        right, left, up, fire key and response accordingly
        '''
        if self._screen.is_left_pressed():
            self.ship.set_heading(ship.LEFT_DIRECTION)
        elif self._screen.is_right_pressed():
            self.ship.set_heading(ship.RIGHT_DIRECTION)
        elif self._screen.is_up_pressed():
            self.ship.accelerate()
        # Check if fire key pressed
        if self._screen.is_space_pressed() and \
                                    len(self.torpedoes) < TORPEDO_SHOT_LIMIT:
            new_torpedo = self.ship.create_torpedo()
            self.torpedoes.append(new_torpedo)
            self._screen.register_torpedo(new_torpedo)

    def move_objects_on_turn(self):
        '''
        Move all objects(=ships, asteroids, torpedoes) in one turn
        '''
        # Move ship
        self.move_object(self.ship)
        # Move asteroids
        for asteroid in self.asteroids:
            self.move_object(asteroid)
        # move all torpedoes
        for torpedo in self.torpedoes:
            self.move_object(torpedo)

    def add_points(self, asteroid_size):
        """
        :param asteroid_size represent the size of the destroyed asteroid.
        Add points to user
        size 1 = 100 points
        size 2 = 50 points
        size 3 = 20 points
        """
        add_points = 0
        if asteroid_size == 3:
            add_points = POINTS_FOR_ASTEROID_SIZE_3
        elif asteroid_size == 2:
            add_points = POINTS_FOR_ASTEROID_SIZE_2
        else:
            add_points = POINTS_FOR_ASTEROID_SIZE_1
        self.score += add_points
        self._screen.set_score(self.score)

    def move_object(self, object):
        """
        Set new position to object
        :param object - Ship, Asteroid or Torpedo
        :return:
        """
        new_coord_x = self.get_new_coord(object, X)
        new_coord_y = self.get_new_coord(object, Y)
        object.set_position(new_coord_x, new_coord_y)
        self.draw_object(object)

    def draw_object(self, object):
        """
        This function will draw the object on screen
        """
        obj_position = object.get_position()
        if isinstance(object, ship.Ship):
            self._screen.draw_ship(obj_position[X], obj_position[Y],
                                            object.get_ship_heading_deg())
        elif isinstance(object, asteroid.Asteroid):
            self._screen.draw_asteroid(object, obj_position[X],
                                                            obj_position[Y])
        else:
            # Check if torpedo out of lives
            if object.dec_lives():
                self.torpedoes.remove(object)
                self._screen.unregister_torpedo(object)
            else:
                self._screen.draw_torpedo(object, obj_position[X],
                                          obj_position[Y],
                                          object.get_torpedo_heading_deg())

    def get_new_coord(self, object, axis):
        """
        Return the new coordinate in the given axis
        :param object:
        :param axis: X or Y
        :return:
        """
        delta_axis = self.get_delta_axis(axis)
        object_speed = object.get_velocity()
        object_position = object.get_position()
        axis_min_size = self.get_min_axis_size(axis)
        return (object_speed[axis] + object_position[axis] -
                axis_min_size) % delta_axis + axis_min_size

    def get_delta_axis(self, axis):
        """
        :param axis
        Return tuple (max_size<axis>, min_size<axis>)
        """
        return {X: (self.screen_max_x - self.screen_min_x),
                Y: (self.screen_max_y - self.screen_min_y)}[axis]

    def get_min_axis_size(self, axis):
        """
        :param axis
        Return the min axis size
        """
        return {X: self.screen_min_x,
                Y: self.screen_min_y}[axis]

    def get_x_y_random_values(self):
        return (random.randrange(Screen.SCREEN_MIN_X, Screen.SCREEN_MAX_X),
                random.randrange(Screen.SCREEN_MIN_Y, Screen.SCREEN_MAX_Y))

    def get_velocity_x_y_random(self):
        return (random.randrange(-3, 3),
                random.randrange(-3, 3))


def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
