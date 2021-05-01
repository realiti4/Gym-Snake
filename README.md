# gym-snake

This fork is heavly optimized (up to x10 faster than original repo) for multi-env training. Only supports 1 snake and
some drawing features are removed.

#### Install:

    pip install git+https://github.com/realiti4/Gym-Snake.git@master --upgrade


## Description
gym-snake is a multi-agent implementation of the classic game [snake](https://www.youtube.com/watch?v=wDbTP0B94AM) that is made as an OpenAI gym environment.

## Dependencies
- pip
- gym
- numpy
- matplotlib

## Installation
1. Clone this repository
2. Navigate to the cloned repository
3. Run command `$ pip install -e ./`

## Rendering
If you are experiencing trouble using the `render()` function while using jupyter notebook, insert:

    %matplotlib notebook

before calling `render()`.

## Using gym-snake
After installation, you can use gym-snake by making one of two gym environments.

#### SnakeEnv
Use `gym.make('snake-v0')` to make a new snake environment with the following default options (see Game Details to understand what each variable does):

    grid_size = [15,15]
    unit_size = 10
    unit_gap = 1
    snake_size = 3
    n_snakes = 1
    n_foods = 1

## Game Details
You're probably familiar with the game of snake. This is an OpenAI gym implementation of the game with multi snake and multi food options.

#### Rewards
A +1 reward is returned when a snake eats a food.

A -1 reward is returned when snake dies.

A -1 reward is returned when snake gets stuck for 1000 steps.

#### Game Options

- _grid_size_ - An x,y coordinate denoting the number of units on the snake grid (width, height).
- _unit_size_ - Number of numpy pixels within a single grid unit.
- _unit_gap_ - Number of pixels separating each unit of the grid. Space between the units can be useful to understand the direction of the snake's body.
- _snake_size_ - Number of body units for each snake at start of game
- _n_snakes_ - Number of individual snakes on grid
- _n_foods_ - Number of food units (the stuff that makes the snakes grow) on the grid at any given time.
- _random_init_ - If set to false, the food units initialize to the same location at each reset.

Each of these options are member variables of the environment and will come into effect after the environment is reset. For example, if you wanted to use 5 food tokens in the regular version, you can be set the number of food tokens using the following code:

    env = gym.snake('snake-v0')
    env.n_foods = 5
    observation = env.reset()

This will create a vanilla snake environment with 5 food tokens on the map.

#### General Info
The snake environment has three main interacting classes to construct the environment. The three are a Snake class, a Grid class, and a Controller class. Each holds information about the environment, and each can be accessed through the gym environment.

    import gym
    import gym_snake

    # Construct Environment
    env = gym.make('snake-v0')
    observation = env.reset() # Constructs an instance of the game

    # Controller
    game_controller = env.controller

    # Grid
    grid_object = game_controller.grid
    grid_pixels = grid_object.grid

    # Snake(s)
    snakes_array = game_controller.snakes
    snake_object1 = snakes_array[0]

