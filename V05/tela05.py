import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Alimente o gatinho")

# Imagem de fundo
fundo = pygame.image.load("fundo.webp")

# Imagem gatinho
gatinhoBocaFechada = pygame.image.load("bocaFechada.png")
gatinhoBocaFechada = pygame.transform.scale(gatinhoBocaFechada, (100, 100))
gatinhoBocaAberta = pygame.image.load("bocaAberta.png")
gatinhoBocaAberta = pygame.transform.scale(gatinhoBocaAberta, (100, 100))
petisco = pygame.image.load("petisco.png")
petisco = pygame.transform.scale(petisco, (80, 80))

# Posição inicial da imagem petisco
velocidade_max = 5  # Velocidade máxima de queda
contador = 0

# Lista de petiscos
petiscos = []
boca = "fechada"

# Gera 5 petiscos com posições e velocidades aleatórias
for _ in range(5):
    petiscos.append({
        "x": random.randint(0, largura - petisco.get_width()),  # Posição aleatória no eixo X
        "y": random.randint(-100, -10),  # Inicia um pouco acima da tela
        "velocidade": random.randint(3, velocidade_max),  # Velocidade aleatória
        "direcao_x": random.choice([-1, 1]) * random.randint(1, 3)  # Direção aleatória no eixo X
    })

# Posição do gatinho
gatinho_rect = pygame.Rect(300, 450, gatinhoBocaFechada.get_width(), gatinhoBocaFechada.get_height())  # Cria um retângulo para o gatinho
gatinho_velocidade = 5  # Velocidade do gatinho

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Fecha a janela
            rodando = False

    # Detecta o pressionamento das teclas para mover o gatinho
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:  # Move para a esquerda
        gatinho_rect.x -= gatinho_velocidade
    if teclas[pygame.K_RIGHT]:  # Move para a direita
        gatinho_rect.x += gatinho_velocidade

    # Garante que o gatinho não saia da tela
    if gatinho_rect.x < 0:
        gatinho_rect.x = 0
    elif gatinho_rect.x > largura - gatinho_rect.width:
        gatinho_rect.x = largura - gatinho_rect.width

    # Atualiza a posição de cada petisco
    for petisco_obj in petiscos:
        petisco_obj['y'] += petisco_obj['velocidade']  # Atualiza a posição Y
        petisco_obj['x'] += petisco_obj['direcao_x']  # Atualiza a posição X (movendo para a esquerda ou direita)

        # Cria um retângulo para o petisco
        petisco_rect = pygame.Rect(petisco_obj['x'], petisco_obj['y'], petisco.get_width(), petisco.get_height())

        # Verifica colisão entre o gatinho e o petisco
        if gatinho_rect.colliderect(petisco_rect):  # Se o retângulo do gatinho colidir com o petisco
            boca = "aberta"
            # Reinicia a posição do petisco (ele "desaparece" e reaparece em um novo local)
            petisco_obj['y'] = random.randint(-100, -10)  # Reinicia no topo
            petisco_obj['x'] = random.randint(0, largura - petisco.get_width())  # Posição X aleatória
            petisco_obj['direcao_x'] = random.choice([-1, 1]) * random.randint(1, 3)  # Nova direção aleatória

        # Verifica se o petisco atingiu o fundo
        if petisco_obj['y'] > altura:
            petisco_obj['y'] = random.randint(-100, -10)  # Reinicia no topo
            petisco_obj['x'] = random.randint(0, largura - petisco.get_width())  # Posição X aleatória
            petisco_obj['direcao_x'] = random.choice([-1, 1]) * random.randint(1, 3)  # Nova direção aleatória

        # Garante que o petisco não ultrapasse as bordas da tela
        if petisco_obj['x'] < 0:
            petisco_obj['x'] = 0
            petisco_obj['direcao_x'] = abs(petisco_obj['direcao_x'])  # Força a direção para a direita
        elif petisco_obj['x'] > largura - petisco.get_width():
            petisco_obj['x'] = largura - petisco.get_width()
            petisco_obj['direcao_x'] = -abs(petisco_obj['direcao_x'])  # Força a direção para a esquerda

    # Desenha o fundo
    tela.blit(fundo, (0, 0))

    # Desenha o gatinho
    if boca == "aberta":
        tela.blit(gatinhoBocaAberta, (gatinho_rect.x, gatinho_rect.y))
        boca = "fechada"
    else:
        tela.blit(gatinhoBocaFechada, (gatinho_rect.x, gatinho_rect.y))

    # Desenha os petiscos
    for petisco_obj in petiscos:
        tela.blit(petisco, (petisco_obj['x'], petisco_obj['y']))

    # Atualiza a tela
    pygame.display.flip()

    # Controla a velocidade da animação
    pygame.time.delay(30)

# Finaliza o Pygame
pygame.quit()
