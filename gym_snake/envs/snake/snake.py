from queue import deque
import numpy as np

class Snake():

    """
    The Snake class holds all pertinent information regarding the Snake's movement and boday.
    The position of the snake is tracked using a queue that stores the positions of the body.

    Note:
    A potentially more space efficient implementation could track directional changes rather
    than tracking each location of the snake's body.
    """

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    def __init__(self, head_coord_start, length=3, color=np.array([255,0,0], np.uint8)):
        """
        head_coord_start - tuple, list, or ndarray denoting the starting coordinates for the snake's head
        length - starting number of units in snake's body
        """

        # Select a random direction
        self.direction_dict = [self.UP, self.RIGHT, self.DOWN, self.LEFT]
        self.direction = np.random.randint(4)
        
        self.direction = self.DOWN
        self.head = np.asarray(head_coord_start).astype(np.int)
        self.head_color = color
        self.body = deque()
        # self.body.append(self.head)
        for i in range(1, length):
            body_cord = self.head - np.asarray([0, i], dtype=np.int)
            self.body.append(body_cord)

        # for i in range(length-1, 0, -1):
        #     self.body.append(self.head - np.asarray([0, i]).astype(np.int))
        
        # # Create body depending on direction
        # if self.direction == self.UP:
        #     pass
        # elif self.direction == self.RIGHT:
        #     pass
        # elif self.direction == self.DOWN:
        #     self.body.append(self.head - np.asarray([0, i]).astype(np.int))
        # elif self.direction == self.LEFT:
        #     pass
        # else:
        #     raise Exception('Direction is out of bounds')

    def step(self, coord, direction):
        """
        Takes a step in the specified direction from the specified coordinate.

        coord - list, tuple, or numpy array
        direction - integer from 1-4 inclusive.
            0: up
            1: right
            2: down
            3: left
        """

        if direction == self.UP:
            return np.asarray([coord[0], coord[1] - 1]).astype(np.int)
        elif direction == self.RIGHT:
            return np.asarray([coord[0] + 1, coord[1]]).astype(np.int)
        elif direction == self.DOWN:
            return np.asarray([coord[0], coord[1] + 1]).astype(np.int)
        else:
            return np.asarray([coord[0] - 1, coord[1]]).astype(np.int)

    def action(self, direction):
        """
        This method sets a new head coordinate and appends the old head
        into the body queue. The Controller class handles popping the
        last piece of the body if no food is eaten on this step.

        The direction can be any integer value, but will be collapsed
        to 0, 1, 2, or 3 corresponding to up, right, down, left respectively.

        direction - integer from 0-3 inclusive.
            0: up
            1: right
            2: down
            3: left
        """

        # Ensure direction is either 0, 1, 2, or 3
        direction = int(direction)
        assert direction in self.direction_dict, 'Invalid action'

        if np.abs(self.direction - direction) != 2:
            self.direction = direction

        self.body.appendleft(self.head)
        self.head = self.step(self.head, self.direction)

        return self.head
