import pygame
import random
import sys

# Inicializa o Pygame
pygame.init()
pygame.mixer.init()

# Configurações da tela
largura, altura = 600, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Alimente o Gatinho")

# Imagens e sons
fundo = pygame.image.load("fundo.webp")
gatinhoBocaFechada = pygame.transform.scale(pygame.image.load("bocaFechada.png"), (100, 100))
gatinhoBocaAberta = pygame.transform.scale(pygame.image.load("bocaAberta.png"), (100, 100))
petisco = pygame.transform.scale(pygame.image.load("petisco.png"), (80, 80))

som = pygame.mixer.Sound("miado.ogg")
som.set_volume(0.1)
pygame.mixer.music.load("garcom.ogg")

# Fonte e relógio
fonte = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()

def exibir_pontuacao(pontos):
    return fonte.render(f'Pontos: {pontos}', True, (255, 255, 255))

def exibir_tempo_restante(inicio_tempo, tempo_limite):
    tempo_passado = pygame.time.get_ticks() - inicio_tempo
    tempo_restante = max(0, (tempo_limite - tempo_passado) // 1000)
    tempo_texto = fonte.render(f"Falta {tempo_restante} s", True, (255, 255, 255))
    return tempo_restante, tempo_texto

def gerar_petiscos(num_petiscos):
    return [{"x": random.randint(0, largura - petisco.get_width()),  
             "y": random.randint(-100, -10),  
             "velocidade": random.randint(5, 10),
             "direcao_x": random.choice([-1, 1]) * random.randint(1, 3)} 
            for _ in range(num_petiscos)]

def mover_gatinho(gatinho_rect, gatinho_velocidade):
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        gatinho_rect.x -= gatinho_velocidade
    if teclas[pygame.K_RIGHT]:
        gatinho_rect.x += gatinho_velocidade
    gatinho_rect.x = max(0, min(largura - gatinho_rect.width, gatinho_rect.x))
    return gatinho_rect

def atualizar_petiscos(petiscos, gatinho_rect, contador, boca_aberta):
    for petisco_obj in petiscos:
        petisco_obj['y'] += petisco_obj['velocidade']
        petisco_obj['x'] += petisco_obj['direcao_x']
        petisco_rect = pygame.Rect(petisco_obj['x'], petisco_obj['y'], petisco.get_width(), petisco.get_height())

        if gatinho_rect.colliderect(petisco_rect):  
            petisco_obj['y'] = random.randint(-100, -10)
            petisco_obj['x'] = random.randint(0, largura - petisco.get_width())  
            petisco_obj['direcao_x'] = random.choice([-1, 1]) * random.randint(1, 3)
            contador += 1
            som.play()
            boca_aberta = pygame.time.get_ticks()

        if petisco_obj['y'] > altura:
            petisco_obj['y'] = random.randint(-100, -10)
            petisco_obj['x'] = random.randint(0, largura - petisco.get_width())  

        petisco_obj['x'] = max(0, min(largura - petisco.get_width(), petisco_obj['x']))
    return petiscos, contador, boca_aberta

def desenhar_gatinho(tela, gatinho_rect, boca_aberta):
    if boca_aberta and pygame.time.get_ticks() - boca_aberta < 30:
        tela.blit(gatinhoBocaAberta, (gatinho_rect.x, gatinho_rect.y))
    else:
        tela.blit(gatinhoBocaFechada, (gatinho_rect.x, gatinho_rect.y))

# Tela inicial
def tela_inicial():
    while True:
        tela.fill((0, 0, 0))
        tela.blit(fundo, (0, 0))

        titulo_texto = fonte.render("Alimente o Gatinho", True, (255, 255, 255))
        botao_rect = pygame.Rect(largura // 2 - 100, altura // 2, 200, 50)

        # pygame.draw.rect(tela, (0, 255, 0), botao_rect)
        botao_texto = fonte.render("Jogar", True, (255, 255, 255))

        tela.blit(titulo_texto, (largura // 2 - 140, altura // 2 - 60))
        tela.blit(botao_texto, (botao_rect.x + 60, botao_rect.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    return  # Inicia o jogo

# Tela de fim de jogo
def fim_de_jogo(contador):
    pygame.mixer.music.stop()
    while True:
        tela.fill((0, 0, 0))
        tela.blit(fundo, (0, 0))

        game_over_text = fonte.render("Fim do Jogo!", True, (255, 0, 0))
        final_score_text = fonte.render(f'Pontuação Final: {contador}', True, (255, 255, 255))
        botao_rect = pygame.Rect(largura // 2 - 100, altura // 2 + 50, 200, 50)

        # pygame.draw.rect(tela, (255, 255, 255), botao_rect)
        botao_texto = fonte.render("Jogar", True, (255, 255, 255))

        tela.blit(game_over_text, (largura // 2 - 100, altura // 2 - 40))
        tela.blit(final_score_text, (largura // 2 - 120, altura // 2))
        tela.blit(botao_texto, (botao_rect.x + 60, botao_rect.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_rect.collidepoint(evento.pos):
                    return  # Reinicia o jogo

def jogo():
    while True:
        pygame.mixer.music.play(loops=-1)
        gatinho_rect = pygame.Rect(300, 500, gatinhoBocaFechada.get_width(), gatinhoBocaFechada.get_height())
        contador = 0
        tempo_limite = 3000
        inicio_tempo = pygame.time.get_ticks()
        petiscos = gerar_petiscos(10)
        boca_aberta = 0

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            tempo_restante, tempo_texto = exibir_tempo_restante(inicio_tempo, tempo_limite)

            if tempo_restante == 0:
                fim_de_jogo(contador)
                break  

            gatinho_rect = mover_gatinho(gatinho_rect, 7)
            petiscos, contador, boca_aberta = atualizar_petiscos(petiscos, gatinho_rect, contador, boca_aberta)

            tela.fill((0, 0, 0))
            tela.blit(fundo, (0, 0))
            tela.blit(tempo_texto, (10, 10))
            tela.blit(exibir_pontuacao(contador), (largura - 200, 10))
            desenhar_gatinho(tela, gatinho_rect, boca_aberta)

            for petisco_obj in petiscos:
                tela.blit(petisco, (petisco_obj['x'], petisco_obj['y']))

            pygame.display.flip()
            clock.tick(40)

# Executa a tela inicial antes de iniciar o jogo
tela_inicial()
jogo()
