import pygame
import random

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
petisco = pygame.image.load("petisco.png")
petisco = pygame.transform.scale(petisco, (80, 80))

# Posição inicial da imagem petisco
velocidade_max = 5  # Velocidade máxima de queda

# Lista de petiscos
petiscos = []

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

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Fecha a janela
            rodando = False

    # Atualiza a posição de cada petisco
    for petisco_obj in petiscos:
        petisco_obj['y'] += petisco_obj['velocidade']  # Atualiza a posição Y
        petisco_obj['x'] += petisco_obj['direcao_x']  # Atualiza a posição X (movendo para a esquerda ou direita)

        # Cria um retângulo para o petisco
        petisco_rect = pygame.Rect(petisco_obj['x'], petisco_obj['y'], petisco.get_width(), petisco.get_height())

        # Verifica colisão entre o gatinho e o petisco
        if gatinho_rect.colliderect(petisco_rect):  # Se o retângulo do gatinho colidir com o petisco
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
    tela.blit(gatinhoBocaFechada, (300, 450))

    # Desenha os petiscos
    for petisco_obj in petiscos:
        tela.blit(petisco, (petisco_obj['x'], petisco_obj['y']))

    # Atualiza a tela
    pygame.display.flip()

    # Controla a velocidade da animação
    pygame.time.delay(30)

# Finaliza o Pygame
pygame.quit()
