from gym_snake.envs.snake import Snake
from gym_snake.envs.snake import Grid
import numpy as np


class Controller:
    """
    This class combines the Snake, Food, and Grid classes to handle the game logic.
    """

    def __init__(
        self,
        grid_size=[30, 30],
        unit_size=10,
        unit_gap=1,
        snake_size=3,
        n_snakes=1,
        n_foods=1,
        random_init=True,
    ):
        assert n_snakes < grid_size[0] // 3
        assert n_snakes < 25
        assert snake_size < grid_size[1] // 2
        assert unit_gap >= 0 and unit_gap < unit_size

        self.snakes_remaining = n_snakes
        self.grid = Grid(grid_size, unit_size, unit_gap)

        self.dead_snake = False

        # Randomize starting coord
        start_coord = [5, 4]
        color = self.grid.HEAD_COLOR
        self.snake = Snake(start_coord, snake_size, color)
        self.grid.draw_snake(self.snake)

        # Draw food
        for i in range(n_foods):
            self.grid.new_food()

    def move_snake(self, direction):
        """
        Moves the specified snake according to the game's rules dependent on the direction.
        Does not draw head and does not check for reward scenarios. See move_result for these
        functionalities.
        """

        snake = self.snake
        if snake is None:
            return

        # Cover old head position with body
        self.grid.cover(snake.head, self.grid.BODY_COLOR)
        # Erase tail without popping so as to redraw if food eaten
        self.grid.erase(snake.body[-1])
        # Find and set next head position conditioned on direction
        snake.action(direction)

    def move_result(self):
        """
        Checks for food and death collisions after moving snake. Draws head of snake if
        no death scenarios.
        """

        snake = self.snake
        if snake is None:
            return 0

        # Check for death of snake
        if self.grid.check_death(snake.head):
            self.dead_snake = True
            self.grid.cover(
                snake.head, snake.head_color
            )  # Avoid miscount of grid.open_space
            reward = -1
        # Check for reward
        elif self.grid.food_space(snake.head):
            self.grid.draw(snake.body[-1], self.grid.BODY_COLOR)  # Redraw tail
            self.grid.cover(
                snake.head, snake.head_color
            )  # Avoid miscount of grid.open_space
            reward = 1
            self.grid.new_food()
        else:
            reward = 0
            empty_coord = snake.body.pop()
            self.grid.draw(snake.head, snake.head_color)

        # self.grid.connect(snake.body[-1], snake.head, self.grid.BODY_COLOR)

        return reward

    def step(self, directions):
        """
        Takes an action for each snake in the specified direction and collects their rewards
        and dones.

        directions - tuple, list, or ndarray of directions corresponding to each snake.
        """

        # Ensure no more play until reset
        if self.snakes_remaining < 1 or self.grid.open_space < 1:
            if type(directions) == type(int()) or len(directions) == 1:
                return (
                    self.grid.grid.copy(),
                    0,
                    True,
                    {"snakes_remaining": self.snakes_remaining},
                )
            else:
                return (
                    self.grid.grid.copy(),
                    [0] * len(directions),
                    True,
                    {"snakes_remaining": self.snakes_remaining},
                )

        rewards = []

        direction = directions

        self.move_snake(direction)
        rewards.append(self.move_result())
        done = self.dead_snake or self.grid.open_space < 1

        if len(rewards) == 1:
            return (
                self.grid.grid.copy(),
                rewards[0],
                done,
                {"snakes_remaining": self.snakes_remaining},
            )
        else:
            return (
                self.grid.grid.copy(),
                rewards,
                done,
                {"snakes_remaining": self.snakes_remaining},
            )
