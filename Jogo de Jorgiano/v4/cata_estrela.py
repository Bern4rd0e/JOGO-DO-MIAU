import math
import random
import sys
import time

import pygame


def game_init(w, h):
    pygame.init()
    size = w, h
    display = pygame.display.set_mode(size)
    pygame.display.set_caption("Cata Estrela")
    return display


def create_star(stars, stars_rect):
    star = pygame.image.load("Estrela.png")
    star_rect = star.get_rect()
    star_rect.x = random.randrange(640)
    star_rect.y = random.randrange(480)
    color = random.randrange(200), random.randrange(200), random.randrange(200)
    star.fill(color, special_flags=pygame.BLEND_SUB)
    stars.append(star)
    stars_rect.append(star_rect)


def draw_ship(ship, ship_rect, display, ship_angle):
    center = ship_rect.center
    ship_copy = ship.copy()
    ship_copy = pygame.transform.rotate(ship_copy, ship_angle + 90)
    ship_copy_rect = ship_copy.get_rect()
    ship_copy_rect.center = center
    display.blit(ship_copy, ship_copy_rect)


def draw_stars(stars, stars_rect, display):
    for i in range(0, len(stars)):
        display.blit(stars[i], stars_rect[i])


def capture_stars(stars, stars_rect, ship_rect):
    new_stars = []
    new_stars_rect = []
    for i in range(0, len(stars)):
        x = stars_rect[i].x
        y = stars_rect[i].y
        crop = pygame.Rect((x, y), (25, 25))
        if not (ship_rect.colliderect(crop)):
            new_stars.append(stars[i])
            new_stars_rect.append(stars_rect[i])

    return new_stars, new_stars_rect


def move_player(keys, ship_rect, ang, speed_x, speed_y):
    if keys[pygame.K_LEFT]:
        ang += 5
    if keys[pygame.K_RIGHT]:
        ang -= 5
    if keys[pygame.K_UP]:
        speed_x += -(math.cos(math.radians(ang)))
        speed_y += math.sin(math.radians(ang))
    speed_x = speed_x * 0.95
    speed_y = speed_y * 0.95
    new_x = round(((ship_rect.center[0]) + speed_x) % display.get_rect().width)
    new_y = round(((ship_rect.center[1]) + speed_y) % display.get_rect().height)
    ship_rect.center = (new_x, new_y)
    return ang, speed_x, speed_y


display = game_init(640, 480)

background_img = pygame.image.load("Space.png")
ship = pygame.image.load("Nave.bmp")
ship.set_colorkey((255, 0, 255))
shiprect = ship.get_rect()
shiprect.y = 240
shiprect.x = 320
ang_nave = 270
vel_x = 0.0
vel_y = 0.0

stars = []
stars_rect = []
for i in range(0, 20):
    create_star(stars, stars_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    ang_nave, vel_x, vel_y = move_player(
        keys, shiprect, ang_nave, vel_x, vel_y
    )  # noqa: E501

    stars, stars_rect = capture_stars(stars, stars_rect, shiprect)
    if len(stars) < 20:
        if random.randrange(100) > 10:
            create_star(stars, stars_rect)

    display.blit(background_img, (0, 0))
    draw_stars(stars, stars_rect, display)
    draw_ship(ship, shiprect, display, ang_nave)
    pygame.display.flip()
    time.sleep(0.015)
