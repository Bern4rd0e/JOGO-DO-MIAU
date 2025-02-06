import pygame

import random
import sys
import time

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Alimente o gatinho")

# Imagem de fundo
fundo = pygame.image.load("./V01/fundo.webp")

# Imagem gatinho
gatinhoBocaFechada = pygame.image.load("./V01/bocaFechada.png")
gatinhoBocaFechada = pygame.transform.scale(gatinhoBocaFechada, (100, 100))
petisco = pygame.image.load("./V01/petisco.png")
petisco = pygame.transform.scale(petisco, (80, 80))

# Posição inicial da imagem petisco
x = random.randint(0, largura - petisco.get_width())  # Posição aleatória dentro da tela
y = 0 # Inicia no início da tela

# Velocidada da queda 
velocidade = 5

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Fecha a janela
            rodando = False

    

    # Define o fundo branco
    # tela.fill((255, 255, 255)) 

    # Atualiza a posição da imagem (fazendo-a cair)
    y += velocidade 

    # Se a imagem atingir o fundo da tela, ela volta para o topo
    if y > altura:  
        y -80 # Reinicia acima da tela
        x = random.randint(0, largura - petisco.get_width())  # Gera uma nova posição aleatória para x



    tela.blit(fundo,(0,0))
    tela.blit(gatinhoBocaFechada, (300, 400))  
    tela.blit(petisco, (x,y))
    

    #Atualiza a tela
    pygame.display.flip()

    # Controla a velocidade da animação
    pygame.time.delay(30)

# Finaliza o Pygame
pygame.quit()
