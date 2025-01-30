import sys
import time

import pygame

pygame.init()

width, height = 640, 480
size = width, height
tela = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Cata estrela")

imagem_fundo = pygame.image.load("Space.png")
nave = pygame.image.load("Nave.bmp")
nave.set_colorkey((255, 0, 255))
naverect = nave.get_rect()
naverect.y = 240
naverect.x = 320

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

    tela.blit(imagem_fundo, (0, 0))
    tela.blit(nave, naverect)
    pygame.display.flip()
    time.sleep(0.015)
