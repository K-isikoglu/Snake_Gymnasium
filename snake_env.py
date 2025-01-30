import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register

import snake_game
import numpy as np

register(
    id = 'snake-game-v0',
    entry_point = 'snake_env:SnakeEnv'
)

class SnakeGame(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 10}

    def __init__(self, render_mode = None):
        self.render_mode = render_mode

        self.my_snake = snake_game.SnakeGame()

        self.action_space = None
        self.observation_space = None

    def reset(self, seed = None, options = None):
        pass

    def step(self, action):
        pass

    def render(self):
        pass

    def close(self):
        pass