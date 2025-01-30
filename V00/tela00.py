import pygame

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Alimente o gatinho")

# Imagem de fundo
fundo = pygame.image.load("V00/fundo.webp")

# Imagem gatinho
gatinhoBocaFechada = pygame.image.load("V00/bocaFechada.png")
gatinhoBocaFechada = pygame.transform.scale(gatinhoBocaFechada, (100, 100))

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Fecha a janela
            rodando = False

    # Atualiza a tela
    # tela.fill((255, 255, 255))  # Define o fundo preto

    tela.blit(fundo,(0,0))
    tela.blit(gatinhoBocaFechada, (300, 400))  
    

    #Atualiza a tela
    pygame.display.flip()

# Finaliza o Pygame
pygame.quit()
