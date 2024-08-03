import pygame
from pygame import Vector2
from random import randrange
import config

pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
screen_width, screen_height = pygame.display.get_surface().get_size()
config.SCREEN_SIZE = screen_width
config.GRID_CELL_SIZE = screen_width // 80
config.SNAKE_PART_SIZE = config.GRID_CELL_SIZE
config.FOOD_SIZE = config.GRID_CELL_SIZE
config.SNAKE_MOVE_LENGTH = config.GRID_CELL_SIZE

running = True
begin = True
bait = True
time = None
snake_rect = None
snake_length = None
snake_parts = None
snake_direction = None
food_rect = None

while running:
    if begin:
        begin = False
        time = 0
        snake_rect = pygame.Rect([randrange(0, screen_width, config.GRID_CELL_SIZE),
                                  randrange(0, screen_height, config.GRID_CELL_SIZE),
                                  config.SNAKE_PART_SIZE,
                                  config.SNAKE_PART_SIZE])
        snake_length = 1
        snake_parts = []
        snake_direction = Vector2(0, 0)

    if bait:
        bait = False
        food_rect = pygame.Rect([randrange(0, screen_width, config.GRID_CELL_SIZE),
                                 randrange(0, screen_height, config.GRID_CELL_SIZE),
                                 config.FOOD_SIZE,
                                 config.FOOD_SIZE])

    for event in pygame.event.get():
        if (event.type == pygame.QUIT or
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not snake_direction[1] > 0:
                snake_direction = Vector2(0, -config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_DOWN and not snake_direction[1] < 0:
                snake_direction = Vector2(0, config.SNAKE_MOVE_LENGTH)
            if event.key == pygame.K_LEFT and not snake_direction[0] > 0:
                snake_direction = Vector2(-config.SNAKE_MOVE_LENGTH, 0)
            if event.key == pygame.K_RIGHT and not snake_direction[0] < 0:
                snake_direction = Vector2(config.SNAKE_MOVE_LENGTH, 0)

    time_now = pygame.time.get_ticks()
    screen.fill((173, 216, 230))

    for i in range(0, screen_width, config.GRID_CELL_SIZE):
        pygame.draw.line(screen, config.GRID_COLOR, (i, 0), (i, screen_height))
        pygame.draw.line(screen, config.GRID_COLOR, (0, i), (screen_width, i))

    if time_now - time > config.DELAY:
        time = time_now
        snake_rect.move_ip(snake_direction)
        snake_parts.append(snake_rect.copy())
        snake_parts = snake_parts[-snake_length:]

    pygame.draw.rect(screen, config.SNAKE_FOOD_COLOR, food_rect, 0, 10)

    for snake_part in snake_parts:
        pygame.draw.rect(screen, (0, 0, 0), snake_part, 6, 4)  # Black rectangle
        center_x = snake_part.centerx
        center_y = snake_part.centery
        circle_radius = config.GRID_CELL_SIZE // 4
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), circle_radius)

    if (snake_rect.left < 0 or snake_rect.right > screen_width or
            snake_rect.top < 0 or snake_rect.bottom > screen_height or
            len(snake_parts) != len(set(snake_part.center for snake_part in snake_parts))):
        begin = True

    if snake_rect.center == food_rect.center:
        snake_length += 1
        bait = True

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
