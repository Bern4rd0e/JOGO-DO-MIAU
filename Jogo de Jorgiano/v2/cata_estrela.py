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


display = game_init(640, 480)

imagem_fundo = pygame.image.load("Space.png")
nave = pygame.image.load("Nave.bmp")
nave.set_colorkey((255, 0, 255))
naverect = nave.get_rect()
naverect.y = 240
naverect.x = 320


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
        naverect.x -= 5
        if naverect.left < 0:
            naverect.left = 0
    if keys[pygame.K_RIGHT]:
        naverect.x += 5
        if naverect.right > 640:
            naverect.right = 640
    if keys[pygame.K_DOWN]:
        naverect.y += 5
        if naverect.bottom > 480:
            naverect.bottom = 480
    if keys[pygame.K_UP]:
        naverect.y -= 5
        if naverect.top < 0:
            naverect.top = 0

    display.blit(imagem_fundo, (0, 0))
    draw_stars(stars, stars_rect, display)
    display.blit(nave, naverect)
    pygame.display.flip()
    time.sleep(0.015)
