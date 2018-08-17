'''
if len(self.damaged_cells) != ZERO:
            return Direction.NOT_MOVING
        # Otherwise - ship not damaged
        if self.direction in Direction.VERTICAL:
            if self.direction == Direction.UP:
                if self.pos[X] - ONE < ZERO:
                    self.pox[X] = ONE
                    self.direction = Direction.DOWN
                else:
                    self.pos[X] -= ONE
            elif self.direction == Direction.DOWN:
                if self.pos[X]+self.length < self.board_side:
                    self.pos[X] += ONE
                else:
                    self.pos[X] = self.board_side - ONE
                    self.direction = Direction.UP
        else:
            if self.direction == Direction.RIGHT:
                if self.pos[Y]+self.length
            else: #self.direction == Direction.LEFT:
'''
class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    UP = 1
    DOWN = -1
    LEFT = 2
    RIGHT = -2

    NOT_MOVING = 0

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

    def ret_oppositon_direction(direct):
        return {
            Direction.UP : Direction.DOWN,
            Direction.DOWN : Direction.UP,
            Direction.RIGHT : Direction.LEFT,
            Direction.LEFT : Direction.RIGHT
        }[direct]

x = [None]*3
x[2]='b'
for i in x:
    if i != None:
        print(x)
a  = 1
b = (a)
print(type(b))