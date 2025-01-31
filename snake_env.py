import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register

from snake_game import SnakeAction, GameMode, SnakeGame
import numpy as np

register(
    id = 'snake-game-v0',
    entry_point = 'snake_env:SnakeEnv'
)

class SnakeGame(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 10}

    def __init__(self, render_mode = None):
        self.render_mode = render_mode

        self.my_snake = SnakeGame(GameMode.RENDER)

        self.action_space = spaces.Discrete(len(SnakeAction))

        self.observation_space = spaces.Box(
            low=0,
            high=np.array([])
        )

    def reset(self, seed = None, options = None):
        pass

    def step(self, action):
        pass

    def render(self):
        pass

    def close(self):
        pass