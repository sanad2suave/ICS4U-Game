import pygame
import os
import random

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Shooter!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

class Number:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

def draw_window(red, yellow, red_numbers, yellow_numbers):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for number in red_numbers:
        pygame.draw.rect(WIN, RED, (number.x, number.y, 10, 10))

    for number in yellow_numbers:
        pygame.draw.rect(WIN, YELLOW, (number.x, number.y, 10, 10))

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:  # DOWN
        red.y += VEL

def handle_numbers(yellow_numbers, red_numbers, yellow, red):
    for number in yellow_numbers:
        number.x += BULLET_VEL
        if red.colliderect((number.x, number.y, 10, 10)):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_numbers.remove(number)
        elif number.x > WIDTH:
            yellow_numbers.remove(number)

    for number in red_numbers:
        number.x -= BULLET_VEL
        if yellow.colliderect((number.x, number.y, 10, 10)):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_numbers.remove(number)
        elif number.x < 0:
            red_numbers.remove(number)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_numbers = []
    yellow_numbers = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_numbers) < MAX_BULLETS:
                    number = Number(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 5, random.randint(1, 9))
                    yellow_numbers.append(number)

                if event.key == pygame.K_RCTRL and len(red_numbers) < MAX_BULLETS:
                    number = Number(red.x, red.y + red.height // 2 - 5, random.randint(1, 9))
                    red_numbers.append(number)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        draw_window(red, yellow, red_numbers, yellow_numbers)

        handle_numbers(yellow_numbers, red_numbers, yellow, red)

    pygame.quit()

if __name__ == "__main__":
    main()
