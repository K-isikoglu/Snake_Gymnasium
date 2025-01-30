import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 440
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - 40) // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 180, 0)
HEAD_COLOR = (0, 255, 0)

class SnakeGame:
    font = pygame.font.SysFont(None, 35)

    def __init__(self):
        pygame.display.set_caption("Snake Game")

        self.snake = [
                [GRID_WIDTH // 2, GRID_HEIGHT // 2],
                [GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2]
        ]
        self.food_pos = None
        self.generate_food()
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.fps = 10

    def start_game(self):
        while True:
            self.handle_input()
            self.update_snake()
            self.check_collision()
            self.draw_game()
            self.clock.tick(self.fps)

    def generate_food(self):
        while True:
            pos = [random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)]
            if pos not in self.snake:
                self.food_pos = pos
                return

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction[0] != 1:
                    self.next_direction = (-1, 0)
                elif event.key == pygame.K_RIGHT and self.direction[0] != -1:
                    self.next_direction = (1, 0)
                elif event.key == pygame.K_UP and self.direction[1] != 1:
                    self.next_direction = (0, -1)
                elif event.key == pygame.K_DOWN and self.direction[1] != -1:
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
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT or
            head in self.snake[1:]):
            self.game_over()

    def draw_game(self):
        self.screen.fill(BLACK)
        pygame.draw.rect(self.screen, BLACK, (0, 0, WIDTH, 40))
        
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (x, 40), (x, HEIGHT))
        for y in range(40, HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, WHITE, (0, y), (WIDTH, y))
        
        for i, segment in enumerate(self.snake):
            color = HEAD_COLOR if i == 0 else GREEN
            y_pos = segment[1] * GRID_SIZE + 40
            pygame.draw.rect(self.screen, color, (segment[0]*GRID_SIZE, y_pos, GRID_SIZE-1, GRID_SIZE-1))
        
        food_x = self.food_pos[0] * GRID_SIZE
        food_y = self.food_pos[1] * GRID_SIZE + 40
        pygame.draw.rect(self.screen, RED, (food_x, food_y, GRID_SIZE-1, GRID_SIZE-1))
        
        self.screen.blit(SnakeGame.font.render(f'Score: {self.score}', True, WHITE), (10, 5))
        pygame.display.update()

    def game_over(self):
        self.screen.fill(BLACK)
        texts = [
            SnakeGame.font.render(f'Game Over! Score: {self.score}', True, WHITE),
            SnakeGame.font.render('Press any key to quit', True, WHITE)
        ]
        for i, text in enumerate(texts):
            self.screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 30 + i*40))
        pygame.display.update()
        
        while True:
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    game = SnakeGame()
    game.start_game()