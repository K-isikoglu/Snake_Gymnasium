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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont(None, 35)
clock = pygame.time.Clock()

def init_game():
    snake = [
            [GRID_WIDTH // 2, GRID_HEIGHT // 2],
            [GRID_WIDTH // 2 - 1, GRID_HEIGHT // 2]
    ]
    return {
        'snake': snake,
        'food': generate_food(snake),
        'direction': (1, 0),
        'next_dir': (1, 0),
        'score': 0,
        'fps': 10
    }

def generate_food(snake):
    while True:
        pos = [random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)]
        if pos not in snake:
            return pos

def handle_input(current_dir):
    new_dir = current_dir
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and current_dir[0] != 1:
                new_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT and current_dir[0] != -1:
                new_dir = (1, 0)
            elif event.key == pygame.K_UP and current_dir[1] != 1:
                new_dir = (0, -1)
            elif event.key == pygame.K_DOWN and current_dir[1] != -1:
                new_dir = (0, 1)
    return new_dir

def update_snake(snake, direction, food):
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]
    snake.insert(0, new_head)
    
    if snake[0] == food:
        food = generate_food(snake)
        return snake, food, True
    return snake[:-1], food, False

def check_collision(snake):
    head = snake[0]
    if (head[0] < 0 or head[0] >= GRID_WIDTH or 
        head[1] < 0 or head[1] >= GRID_HEIGHT):
        return True
    return head in snake[1:]

def draw_game(snake, food, score):
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, 40))
    
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (x, 40), (x, HEIGHT))
    for y in range(40, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, WHITE, (0, y), (WIDTH, y))
    
    for i, segment in enumerate(snake):
        color = HEAD_COLOR if i == 0 else GREEN
        y_pos = segment[1] * GRID_SIZE + 40
        pygame.draw.rect(screen, color, (segment[0]*GRID_SIZE, y_pos, GRID_SIZE-1, GRID_SIZE-1))
    
    food_y = food[1] * GRID_SIZE + 40
    pygame.draw.rect(screen, RED, (food[0]*GRID_SIZE, food_y, GRID_SIZE-1, GRID_SIZE-1))
    
    screen.blit(font.render(f'Score: {score}', True, WHITE), (10, 5))
    pygame.display.update()

def game_over(score):
    screen.fill(BLACK)
    texts = [
        font.render(f'Game Over! Score: {score}', True, WHITE),
        font.render('Press any key to quit', True, WHITE)
    ]
    for i, text in enumerate(texts):
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - 30 + i*40))
    pygame.display.update()
    
    while True:
        for event in pygame.event.get():
            if event.type in (pygame.QUIT, pygame.KEYDOWN):
                pygame.quit()
                sys.exit()

game_state = init_game()

while True:
    game_state['direction'] = handle_input(game_state['direction'])
    game_state['snake'], game_state['food'], ate_food = update_snake(
        game_state['snake'], game_state['direction'], game_state['food']
    )
    
    if ate_food:
        game_state['score'] += 1
    
    if check_collision(game_state['snake']):
        game_over(game_state['score'])
    
    draw_game(game_state['snake'], game_state['food'], game_state['score'])
    clock.tick(game_state['fps'])