import pygame
import random
import time
import sys

# Inicializa o Pygame
pygame.init()

# Inicializar o mixer para áudio
pygame.mixer.init()

# Configurações da tela
largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Alimente o gatinho")

# Imagens e sons
fundo = pygame.image.load("fundo.webp")
gatinhoBocaFechada = pygame.image.load("bocaFechada.png")
gatinhoBocaFechada = pygame.transform.scale(gatinhoBocaFechada, (100, 100))
gatinhoBocaAberta = pygame.image.load("bocaAberta.png")
gatinhoBocaAberta = pygame.transform.scale(gatinhoBocaAberta, (100, 100))
petisco = pygame.image.load("petisco.png")
petisco = pygame.transform.scale(petisco, (80, 80))

som = pygame.mixer.Sound("miado.ogg")
som.set_volume(0.1)
pygame.mixer.music.load("garcom.ogg")
pygame.mixer.music.play(loops=-1)

# Fonte e relógio
fonte = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()

# Função para exibir a pontuação
def exibir_pontuacao(pontos):
    texto_pontuacao = fonte.render(f'Pontos: {pontos}', True, (255, 255, 255))
    return texto_pontuacao

# Função para gerar petiscos
def gerar_petiscos(num_petiscos):
    petiscos = []
    for _ in range(num_petiscos):
        petiscos.append({
            "x": random.randint(0, largura - petisco.get_width()),  
            "y": random.randint(-100, -10),  
            "velocidade": random.randint(1, 5),  
            "direcao_x": random.choice([-1, 1]) * random.randint(1, 3)
        })
    return petiscos

# Função para mover o gatinho
def mover_gatinho(gatinho_rect, gatinho_velocidade):
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        gatinho_rect.x -= gatinho_velocidade
    if teclas[pygame.K_RIGHT]:
        gatinho_rect.x += gatinho_velocidade
    if gatinho_rect.x < 0:
        gatinho_rect.x = 0
    elif gatinho_rect.x > largura - gatinho_rect.width:
        gatinho_rect.x = largura - gatinho_rect.width
    return gatinho_rect

# Função para atualizar a posição dos petiscos
def atualizar_petiscos(petiscos, gatinho_rect, contador):
    for petisco_obj in petiscos:
        petisco_obj['y'] += petisco_obj['velocidade']
        petisco_obj['x'] += petisco_obj['direcao_x']
        
        petisco_rect = pygame.Rect(petisco_obj['x'], petisco_obj['y'], petisco.get_width(), petisco.get_height())

        if gatinho_rect.colliderect(petisco_rect):  
            petisco_obj['y'] = random.randint(-100, -10)
            petisco_obj['x'] = random.randint(0, largura - petisco.get_width())  
            petisco_obj['direcao_x'] = random.choice([-1, 1]) * random.randint(1, 3)
            contador += 1

        if petisco_obj['y'] > altura:
            petisco_obj['y'] = random.randint(-100, -10)
            petisco_obj['x'] = random.randint(0, largura - petisco.get_width())  
            petisco_obj['direcao_x'] = random.choice([-1, 1]) * random.randint(1, 3)

        if petisco_obj['x'] < 0:
            petisco_obj['x'] = 0
            petisco_obj['direcao_x'] = abs(petisco_obj['direcao_x'])  
        elif petisco_obj['x'] > largura - petisco.get_width():
            petisco_obj['x'] = largura - petisco.get_width()
            petisco_obj['direcao_x'] = -abs(petisco_obj['direcao_x'])
    return petiscos, contador

# Função para exibir o tempo restante
def exibir_tempo_restante(inicio_tempo, tempo_limite):
    tempo_passado = pygame.time.get_ticks() - inicio_tempo
    tempo_restante = max(0, (tempo_limite - tempo_passado) // 1000)
    tempo_texto = fonte.render(f"Tempo Restante: {tempo_restante} s", True, (255, 255, 255))
    return tempo_restante, tempo_texto

# Função para desenhar o gatinho
def desenhar_gatinho(tela, gatinho_rect, boca, tempo_boca_aberta):
    if boca == "aberta" and pygame.time.get_ticks() - tempo_boca_aberta < 30:
        tela.blit(gatinhoBocaAberta, (gatinho_rect.x, gatinho_rect.y))
        som.play()
    else:
        tela.blit(gatinhoBocaFechada, (gatinho_rect.x, gatinho_rect.y))

# Função principal
def jogo():
    # Posição inicial do gatinho e outros parâmetros
    gatinho_rect = pygame.Rect(300, 500, gatinhoBocaFechada.get_width(), gatinhoBocaFechada.get_height())
    gatinho_velocidade = 7
    contador = 0
    tempo_boca_aberta = 0
    boca = "fechada"
    
    # Tempo do jogo
    tempo_limite = 30000
    inicio_tempo = pygame.time.get_ticks()

    # Gera os petiscos
    petiscos = gerar_petiscos(10)

    tempo_acabado = False
    rodando = True

    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        if tempo_acabado:
            pygame.mixer.music.stop()
            tela.fill((0, 0, 0))
            tela.blit(fundo, (0, 0))
            game_over_text = fonte.render("Fim do Jogo!", True, (255, 0, 0))
            tela.blit(game_over_text, (largura // 2 - 100, altura // 2 - 20))
            final_score_text = fonte.render(f'Pontuação Final: {contador}', True, (255, 255, 255))
            tela.blit(final_score_text, (largura // 2 - 120, altura // 2 + 30))
            pygame.display.flip()
            continue

        # Atualiza a posição do gatinho
        gatinho_rect = mover_gatinho(gatinho_rect, gatinho_velocidade)

        # Atualiza os petiscos e a pontuação
        petiscos, contador = atualizar_petiscos(petiscos, gatinho_rect, contador)

        # Limpar a tela
        tela.fill((0, 0, 0))
        tela.blit(fundo, (0, 0))

        # Exibir o tempo restante
        tempo_restante, tempo_texto = exibir_tempo_restante(inicio_tempo, tempo_limite)
        tela.blit(tempo_texto, (largura - 260, 10))

        if tempo_restante == 0 and not tempo_acabado:
            tempo_acabado = True

        if not tempo_acabado:
            texto_pontuacao = exibir_pontuacao(contador)
            tela.blit(texto_pontuacao, (10, 10))

        # Desenha o gatinho
        desenhar_gatinho(tela, gatinho_rect, boca, tempo_boca_aberta)

        # Desenha os petiscos
        for petisco_obj in petiscos:
            tela.blit(petisco, (petisco_obj['x'], petisco_obj['y']))

        pygame.display.flip()
        clock.tick(40)

    pygame.quit()
    sys.exit()

# Inicia o jogo
jogo()
