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
velocidade_max = 5  # Reduzindo a velocidade máxima de queda
contador = 0

# Lista de petiscos
petiscos = []
boca = "fechada"
tempo_boca_aberta = 0  # Variável para controlar o tempo que a boca fica aberta

# Tempo do jogo
tempo_limite = 30000  # 15 segundos (em milissegundos)
inicio_tempo = pygame.time.get_ticks()  # Obtém o tempo inicial em milissegundos

som = pygame.mixer.Sound("miado.ogg")
som.set_volume(0.1) 
pygame.mixer.music.load("garcom.ogg")

# Tocar a música em loop (-1 significa loop infinito)
pygame.mixer.music.play(loops=-1)

# Gera 10 petiscos com posições e velocidades aleatórias
for _ in range(10):
    petiscos.append({
        "x": random.randint(0, largura - petisco.get_width()),  # Posição aleatória no eixo X
        "y": random.randint(-100, -10),  # Inicia um pouco acima da tela
        "velocidade": random.randint(1, velocidade_max),  # Velocidade aleatória reduzida
        "direcao_x": random.choice([-1, 1]) * random.randint(1, 3)  # Direção aleatória no eixo X
    })

# Posição do gatinho
gatinho_rect = pygame.Rect(300, 500, gatinhoBocaFechada.get_width(), gatinhoBocaFechada.get_height())  # Cria um retângulo para o gatinho
gatinho_velocidade = 7  # Reduzindo a velocidade do gatinho

# Fonte e relógio
fonte = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()

def exibir_pontuacao(pontos):
    # Definir as cores
    branco = (255, 255, 255)

    # Definir a fonte
    texto_pontuacao = fonte.render(f'Pontos: {pontos}', True, branco)
    
    return texto_pontuacao

# Variável para controle do fim do jogo
tempo_acabado = False  # Variável que controla se o tempo acabou

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:  # Fecha a janela
            rodando = False

    # Se o tempo já acabou, o jogo vai ficar "congelado"
    if tempo_acabado:
        # Parar a música e não tocar mais
        pygame.mixer.music.stop()
        
        # Limpar a tela e exibir apenas o fundo
        tela.fill((0, 0, 0))
        tela.blit(fundo, (0, 0))  # Apenas o fundo após o tempo acabar

        # Exibe a mensagem de fim de jogo e a pontuação
        game_over_text = fonte.render("Fim do Jogo!", True, (255, 0, 0))
        tela.blit(game_over_text, (largura // 2 - 100, altura // 2 - 20))

        final_score_text = fonte.render(f'Pontuação Final: {contador}', True, (255, 255, 255))
        tela.blit(final_score_text, (largura // 2 - 120, altura // 2 + 30))

        pygame.display.flip()
        continue  # Congela o jogo, não faz mais atualizações

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
            tempo_boca_aberta = pygame.time.get_ticks()  # Marca o tempo em que a boca foi aberta
            # Reinicia a posição do petisco (ele "desaparece" e reaparece em um novo local)
            petisco_obj['y'] = random.randint(-100, -10)  # Reinicia no topo
            petisco_obj['x'] = random.randint(0, largura - petisco.get_width())  # Posição X aleatória
            petisco_obj['direcao_x'] = random.choice([-1, 1]) * random.randint(1, 3)  # Nova direção aleatória

            # Incrementa a pontuação
            contador += 1

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

    # Limpar a tela (preencher com o fundo)
    tela.fill((0, 0, 0))
    tela.blit(fundo, (0, 0))

    # Calculando o tempo restante
    tempo_passado = pygame.time.get_ticks() - inicio_tempo  # Tempo que passou desde o início
    tempo_restante = max(0, (tempo_limite - tempo_passado) // 1000)  # Calcula o tempo restante em segundos

    # Exibir o temporizador na tela
    tempo_texto = fonte.render(f"Tempo Restante: {tempo_restante} s", True, (255, 255, 255))
    tela.blit(tempo_texto, (largura - 260, 10))

    # Se o tempo acabou, marca como tempo_acabado
    if tempo_restante == 0 and not tempo_acabado:
        tempo_acabado = True  # Marca que o tempo acabou

    # Exibir a pontuação durante o jogo (só enquanto o tempo não acabou)
    if not tempo_acabado:
        texto_pontuacao = exibir_pontuacao(contador)
        tela.blit(texto_pontuacao, (10, 10))

    # Desenha o gatinho
    if boca == "aberta" and pygame.time.get_ticks() - tempo_boca_aberta < 30:  # A boca ficará aberta por 300 ms
        tela.blit(gatinhoBocaAberta, (gatinho_rect.x, gatinho_rect.y))
        # Reproduzir o som
        som.play()
    else:
        tela.blit(gatinhoBocaFechada, (gatinho_rect.x, gatinho_rect.y))

    # Desenha os petiscos
    for petisco_obj in petiscos:
        tela.blit(petisco, (petisco_obj['x'], petisco_obj['y']))

    # Atualiza a tela
    pygame.display.flip()

    # Controlando os frames por segundo (FPS)
    clock.tick(40)  # Reduziu a taxa de quadros por segundo para diminuir a velocidade do jogo

# Finaliza o Pygame
pygame.quit()
sys.exit()
