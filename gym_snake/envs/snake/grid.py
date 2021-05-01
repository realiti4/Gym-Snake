import numpy as np

class Grid():

    """
    This class contains all data related to the grid in which the game is contained.
    The information is stored as a numpy array of pixels.
    The grid is treated as a cartesian [x,y] plane in which [0,0] is located at
    the upper left most pixel and [max_x, max_y] is located at the lower right most pixel.

    Note that it is assumed spaces that can kill a snake have a non-zero value as their 0 channel.
    It is also assumed that HEAD_COLOR has a 255 value as its 0 channel.
    """

    # BODY_COLOR = np.array([1,0,0], dtype=np.uint8)
    # HEAD_COLOR = np.array([255, 0, 0], dtype=np.uint8)
    # FOOD_COLOR = np.array([0,0,255], dtype=np.uint8)
    # SPACE_COLOR = np.array([240,240,240], dtype=np.uint8)

    # BODY_COLOR = np.array([255, 255, 255], dtype=np.uint8)
    # HEAD_COLOR = np.array([128, 0, 0], dtype=np.uint8)
    # FOOD_COLOR = np.array([0, 255, 0], dtype=np.uint8)
    # SPACE_COLOR = np.array([0, 0, 0], dtype=np.uint8)

    BODY_COLOR = np.array([64, 64, 64], dtype=np.uint8)
    HEAD_COLOR = np.array([128, 128, 128], dtype=np.uint8)
    FOOD_COLOR = np.array([255, 255, 255], dtype=np.uint8)
    SPACE_COLOR = np.array([0, 0, 0], dtype=np.uint8)

    def __init__(self, grid_size=[30, 30], unit_size=10, unit_gap=1):
        """
        grid_size - tuple, list, or ndarray specifying number of atomic units in
                    both the x and y direction
        unit_size - integer denoting the atomic size of grid units in pixels
        """

        self.unit_size = int(unit_size)
        self.unit_gap = unit_gap
        self.grid_size = np.asarray(grid_size, dtype=np.int) # size in terms of units
        height = self.grid_size[1] * self.unit_size
        width = self.grid_size[0] * self.unit_size
        channels = 3
        self.grid = np.zeros((height, width, channels), dtype=np.uint8)
        self.grid[:, :, :] = self.SPACE_COLOR
        self.open_space = grid_size[0] * grid_size[1]

        self.x_size = np.arange(grid_size[0])
        self.y_size = np.arange(grid_size[1])

    def check_death(self, head_coord):
        """
        Checks the grid to see if argued head_coord has collided with a death space (i.e. snake or wall)

        head_coord - x,y integer coordinates as a tuple, list, or ndarray
        """
        return self.off_grid(head_coord) or self.snake_space(head_coord)

    def color_of(self, coord):
        """
        Returns the color of the specified coordinate
        coord - x,y integer coordinates as a tuple, list, or ndarray
        """

        return self.grid[int(coord[1] * self.unit_size), int(coord[0] * self.unit_size), :]

    def cover(self, coord, color):
        """
        Colors a single space on the grid. Use erase if creating an empty space on the grid.
        This function is used like draw but without affecting the open_space count.

        coord - x,y integer coordinates as a tuple, list, or ndarray
        color - [R,G,B] values as a tuple, list, or ndarray
        """

        if self.off_grid(coord):
            return False
        x = int(coord[0] * self.unit_size)
        end_x = x + self.unit_size - self.unit_gap
        y = int(coord[1]*self.unit_size)
        end_y = y + self.unit_size - self.unit_gap
        self.grid[y:end_y, x:end_x, :] = np.asarray(color, dtype=np.uint8)
        return True

    def draw(self, coord, color):
        """
        Colors a single space on the grid. Use erase if creating an empty space on the grid.
        Affects the open_space count.

        coord - x,y integer coordinates as a tuple, list, or ndarray
        color - [R,G,B] values as a tuple, list, or ndarray
        """

        if self.cover(coord, color):
            self.open_space -= 1
            return True
        else:
            return False

    def draw_snake(self, snake):
        """
        Draws a snake with the given head color.

        snake - Snake object
        head_color - [R,G,B] values as a tuple, list, or ndarray
        """

        self.draw(snake.head, snake.head_color)
        prev_coord = None
        for i in range(len(snake.body)):
            self.draw(snake.body[i], self.BODY_COLOR)

    def erase(self, coord):
        """
        Colors the entire coordinate with SPACE_COLOR to erase potential
        connection lines.

        coord - (x,y) as tuple, list, or ndarray
        """
        if self.off_grid(coord):
            return False
        self.open_space += 1
        x = int(coord[0]*self.unit_size)
        end_x = x + self.unit_size
        y = int(coord[1] * self.unit_size)
        end_y = y + self.unit_size
        self.grid[y:end_y, x:end_x, :] = self.SPACE_COLOR
        return True

    def erase_snake_body(self, snake):
        """
        Removes the argued snake's body and head from the grid.

        snake - Snake object
        """

        for i in range(len(snake.body)):
            self.erase(snake.body.popleft())

    def food_space(self, coord):
        """
        Checks if argued coord is snake food

        coord - x,y integer coordinates as a tuple, list, or ndarray
        """
        return np.array_equal(coord, self.food_cord)
        # return np.array_equal(self.color_of(coord), self.FOOD_COLOR)

    def new_food(self, snake):
        """
        Draws a food on a random, open unit of the grid.
        Returns true if space left. Otherwise returns false.
        """

        if self.open_space < 1:
            return False

        # # Check performance
        # body = np.asarray(snake_body)
        # unique_x, unique_y = np.unique(body[:, 0]), np.unique(body[:, 1])

        # x = np.random.choice(np.setdiff1d(self.x_size, unique_x))
        # y = np.random.choice(np.setdiff1d(self.y_size, unique_y))
        # coord = (x, y)
        # self.draw(coord, self.FOOD_COLOR)
        # self.food_cord = np.asarray(coord)
        # return True

        # Old one
        coord_not_found = True
        while coord_not_found:
            coord = (np.random.randint(0, self.grid_size[0]), np.random.randint(0, self.grid_size[1]))
            if np.array_equal(self.color_of(coord), self.SPACE_COLOR):
                coord_not_found = False
        self.draw(coord, self.FOOD_COLOR)
        self.food_cord = np.asarray(coord)
        return True

    def off_grid(self, coord):
        """
        Checks if argued coord is off of the grid

        coord - x,y integer coordinates as a tuple, list, or ndarray
        """

        return coord[0]<0 or coord[0]>=self.grid_size[0] or coord[1]<0 or coord[1]>=self.grid_size[1]

    def snake_space(self, coord):
        """
        Checks if argued coord is occupied by a snake
        coord - x,y integer coordinates as a tuple, list, or ndarray
        """

        color = self.color_of(coord)
        return np.array_equal(color, self.BODY_COLOR)
