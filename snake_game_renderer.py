import pygame
import numpy as np
from enum import Enum

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
HEAD_COLOR = (0, 255, 0)

class GridMap(Enum):
    EMPTY=0
    HEAD=1
    BODY=2
    FOOD=3

class Renderer:
    font = pygame.font.SysFont(None, 35)

    def __init__(self, width, height, grid_size, grid_width, grid_height):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.grid_width = grid_width
        self.grid_height = grid_height

        self.grid_map = np.zeros((grid_width, grid_height))
        self.screen = pygame.display.set_mode((width, height))

    def get_grid_map(self, snake, food_pos) -> np.ndarray:
        self.grid_map = np.zeros((self.grid_width, self.grid_height))
        for i, segment in enumerate(snake):
            if i == 0:
                self.grid_map[tuple(segment)] = GridMap.HEAD.value
            else:
                self.grid_map[tuple(segment)] = GridMap.BODY.value
        self.grid_map[tuple(food_pos)] = GridMap.FOOD.value
        return self.grid_map

    def render(self, snake, food_pos, score) -> np.ndarray:
        self.grid_map = np.zeros((self.grid_width, self.grid_height))
        self._render_game_background()
        self._render_snake(snake)
        self._render_food(food_pos)
        self._render_score(score)
        pygame.display.update()
        return self.grid_map

    def _render_game_background(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, 40))
        for x in range(0, self.width, self.grid_size):
            pygame.draw.line(self.screen, WHITE, (x, 40), (x, self.height))
        for y in range(40, self.height, self.grid_size):
            pygame.draw.line(self.screen, WHITE, (0, y), (self.width, y))

    def _render_snake(self, snake):
        for i, segment in enumerate(snake):
            if i == 0:
                color = HEAD_COLOR
                self.grid_map[tuple(segment)] = GridMap.HEAD.value
            else:
                color = GREEN
                self.grid_map[tuple(segment)] = GridMap.BODY.value
            x_pos = segment[0] * self.grid_size
            y_pos = segment[1] * self.grid_size + 40
            pygame.draw.rect(self.screen, color, (x_pos, y_pos, self.grid_size-1, self.grid_size-1))

    def _render_food(self, food_pos):
        self.grid_map[tuple(food_pos)] = GridMap.FOOD.value
        food_x = food_pos[0] * self.grid_size
        food_y = food_pos[1] * self.grid_size + 40
        pygame.draw.rect(self.screen, RED, (food_x, food_y, self.grid_size-1, self.grid_size-1))

    def _render_score(self, score):
        self.screen.blit(Renderer.font.render(f'Score: {score}', True, WHITE), (10, 5))

    def render_game_over(self, score):
        self.screen.fill(BLACK)
        texts = [
            Renderer.font.render(f'Game Over! Score: {score}', True, WHITE),
            Renderer.font.render('Press any key to quit', True, WHITE)
        ]
        for i, text in enumerate(texts):
            self.screen.blit(text, (self.width//2 - text.get_width()//2, self.height//2 - 30 + i*40))
        pygame.display.update()