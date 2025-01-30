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


display = game_init(640, 480)

imagem_fundo = pygame.image.load("Space.png")
ship = pygame.image.load("Nave.bmp")
ship.set_colorkey((255, 0, 255))
shiprect = ship.get_rect()
shiprect.y = 240
shiprect.x = 320


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
    if keys[pygame.K_LEFT]:
        shiprect.x -= 5
        if shiprect.left < 0:
            shiprect.left = 0
    if keys[pygame.K_RIGHT]:
        shiprect.x += 5
        if shiprect.right > 640:
            shiprect.right = 640
    if keys[pygame.K_DOWN]:
        shiprect.y += 5
        if shiprect.bottom > 480:
            shiprect.bottom = 480
    if keys[pygame.K_UP]:
        shiprect.y -= 5
        if shiprect.top < 0:
            shiprect.top = 0
            # Draw stars
    stars, stars_rect = capture_stars(stars, stars_rect, shiprect)
    if len(stars) < 20:
        if random.randrange(100) > 10:
            create_star(stars, stars_rect)

    display.blit(imagem_fundo, (0, 0))
    draw_stars(stars, stars_rect, display)
    display.blit(ship, shiprect)
    pygame.display.flip()
    time.sleep(0.015)
