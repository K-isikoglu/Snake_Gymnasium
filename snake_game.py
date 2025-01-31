import pygame
import random
import sys
import numpy as np
from enum import Enum

from snake_game_renderer import Renderer

pygame.init()

WIDTH = 600
HEIGHT = 440
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - 40) // GRID_SIZE

class SnakeAction(Enum):
    LEFT=0
    RIGHT=1
    UP=2
    DOWN=3

class GameMode(Enum):
    PLAY=0
    TRAIN=1
    RENDER=2

class SnakeGame:
    def __init__(self, game_mode:GameMode):
        pygame.display.set_caption("Snake Game")

        self.game_mode = game_mode
        self.clock = pygame.time.Clock()
        self.fps = 10

        self.renderer = Renderer(WIDTH, HEIGHT, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT)

    def reset(self, np_random=None) -> np.ndarray:
        self.snake = [
                [GRID_WIDTH // 2, GRID_HEIGHT // 2],
                [GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2]
        ]
        self.food_pos = None
        self.np_random = np_random if np_random else np.random.default_rng()
        self.generate_food()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0

        return self.renderer.get_empty_grid_map()


    def start_game(self):
        self.reset()
        while True:
            if self.game_mode == GameMode.PLAY:
                self.handle_input()
            self.update_snake()
            self.check_collision()
            self.render()
            self.clock.tick(self.fps)

    def generate_food(self):
        while True:
            pos = [
                self.np_random.integers(0, GRID_WIDTH-1),
                self.np_random.integers(0, GRID_HEIGHT-1)
            ]
            if pos not in self.snake:
                self.food_pos = pos
                return

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.perform_action(SnakeAction.LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.perform_action(SnakeAction.RIGHT)
                elif event.key == pygame.K_UP:
                    self.perform_action(SnakeAction.UP)
                elif event.key == pygame.K_DOWN:
                    self.perform_action(SnakeAction.DOWN)

    def perform_action(self, snake_action:SnakeAction):
        if snake_action == SnakeAction.LEFT and self.direction[0] != 1:
            self.next_direction = (-1, 0)
        elif snake_action == SnakeAction.RIGHT and self.direction[0] != -1:
            self.next_direction = (1, 0)
        elif snake_action == SnakeAction.UP and self.direction[1] != 1:
            self.next_direction = (0, -1)
        elif snake_action == SnakeAction.DOWN and self.direction[1] != -1:
            self.next_direction = (0, 1)

    def update_snake(self):
        self.direction = self.next_direction
        new_head = [self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1]]
        self.snake.insert(0, new_head)
        
        if self.snake[0] == self.food_pos:
            self.score += 1
            self.generate_food()
        else:
            self.snake = self.snake[:-1]

    def check_collision(self):
        head = self.snake[0]
        is_game_over = False
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT or
            head in self.snake[1:]):
            is_game_over = True
        if self.game_mode == GameMode.TRAIN:
            return is_game_over
        elif is_game_over:
            self.game_over()
    
    def game_over(self):
        self.renderer.render_game_over(self.score)
        while True:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    pygame.quit()
                    sys.exit()

    def render(self):
        if self.game_mode != GameMode.TRAIN:
            self.renderer.render(self.snake, self.food_pos, self.score)
            
    def get_grid_map(self):
        return self.renderer.get_grid_map(self.snake, self.food_pos)

if __name__ == "__main__":
    game = SnakeGame(GameMode.PLAY)
    game.start_game()