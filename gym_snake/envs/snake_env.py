import numpy as np
import gymnasium as gym
from gymnasium import error, spaces
from gym_snake.envs.snake import Controller
from typing import Optional

try:
    import matplotlib.pyplot as plt
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (HINT: see matplotlib documentation for installation https://matplotlib.org/faq/installing_faq.html#installation".format(e))

class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, grid_size=[10, 10], unit_size=10, unit_gap=1, snake_size=3, n_snakes=1, n_foods=1, random_init=True):
        self.grid_size = grid_size
        self.unit_size = unit_size
        self.unit_gap = unit_gap
        self.snake_size = snake_size
        self.n_snakes = n_snakes
        self.n_foods = n_foods
        self.food_cord = None
        self.viewer = None
        self.random_init = random_init

        self.action_space = spaces.Discrete(4)

        controller = Controller(
            self.grid_size, self.unit_size, self.unit_gap,
            self.snake_size, self.n_snakes, self.n_foods,
            random_init=self.random_init)
        grid = controller.grid
        self.observation_space = spaces.Box(
            low=np.min(grid.COLORS),
            high=np.max(grid.COLORS),
            dtype=np.uint8
        )

        # Terminate or punish stuck agents
        self.count = 0
        self.end_episode = 1000

        self.enable_episode_limit = True

        # # Spaces
        # self.observation_space = spaces.Box(0, 255, [grid_size[0]*unit_size, grid_size[1]*unit_size, 3])

    def step(self, action):
        self.last_obs, rewards, done, info = self.controller.step(action)
        
        # Max length control - terminate after not seeing a reward after n steps
        if self.enable_episode_limit:
            if rewards == 0:
                self.count += 1
            else:
                self.count = 0
            if self.count >= self.end_episode:
                rewards = 0
                done = True

        truncated = False
            
        return self.last_obs, rewards, done, truncated, info

    def reset(self, seed: Optional[int] = None, options: Optional[dict] = None):
        self.controller = Controller(self.grid_size, self.unit_size, self.unit_gap, self.snake_size, self.n_snakes, self.n_foods, random_init=self.random_init)
        self.last_obs = self.controller.grid.grid.copy()
        self.count = 0

        info = {}

        return self.last_obs, info

    def render(self, mode='human', close=False, frame_speed=.1):
        if self.viewer is None:
            self.fig = plt.figure()
            self.viewer = self.fig.add_subplot(111)
            plt.ion()
            self.fig.show()
        
        self.viewer.clear()
        self.viewer.imshow(self.last_obs)
        plt.pause(frame_speed)
        
        self.fig.canvas.draw()

    def seed(self, x):
        pass
