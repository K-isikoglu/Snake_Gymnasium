import gymnasium as gym
from gymnasium import spaces
from gymnasium.envs.registration import register

import pygame

import snake_game
from snake_game import SnakeAction, GameMode, SnakeGame
import numpy as np

register(
    id = 'snake-game-v0',
    entry_point = 'snake_env:SnakeEnv'
)

REWARD_FOR_COLLIDING = -200
REWARD_FOR_EATING = 20
REWARD_FOR_MOVING = -1

class SnakeEnv(gym.Env):
    metadata = {'render_modes': ['human'], 'render_fps': 10}

    def __init__(self, render_mode = None):
        self.render_mode = render_mode

        self.my_snake = SnakeGame(GameMode.RENDER)

        self.action_space = spaces.Discrete(len(SnakeAction))

        self.observation_space = spaces.Box(
            low=0,
            high=3,
            shape=(snake_game.GRID_WIDTH, snake_game.GRID_HEIGHT),
            dtype=np.uint8
        )

    def reset(self, seed=None, options=None):
        super().reset()
        obs = self.my_snake.reset()
        info = {}

        return obs, info

    def step(self, action):
        reward = 0
        terminated = False

        self.my_snake.perform_action(SnakeAction(action))
        if self._did_snake_eat():
            reward += REWARD_FOR_EATING
        if self.my_snake.check_collision():
            reward += REWARD_FOR_COLLIDING
            terminated = True
        obs = self.render()

        info = {}

        return obs, reward, terminated, False, info

    def _did_snake_eat(self):
        last_score = self.my_snake.score
        self.my_snake.update_snake()
        return self.my_snake.score > last_score

    def render(self):
        self.my_snake.render()

    def close(self):
        pass

if __name__ == "__main__":
    env = gym.make('snake-game-v0', render_mode='human')

    obs = env.reset()[0]

    clock = pygame.time.Clock()

    for i in range(1000):
        rand_action = env.action_space.sample()
        obs, reward, terminated, _, _ = env.step(rand_action)
        clock.tick(10)