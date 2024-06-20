import pygame
from pygame.locals import *
from pygame import mixer
import random
import math
import os


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.mixer.init()
relogio = pygame.time.Clock()
largura = 600
altura = 700
pontos = 0
velocidade_jogo = 10


# Obtém o diretório atual do script
diretorio_atual = os.path.dirname(__file__)

# Caminho relativo para o arquivo de fonte
caminho_fonte = os.path.join(diretorio_atual, 'img', 'IBMPlexMono-Light.ttf')

# Carrega a fonte usando o caminho relativo
fonte_pontuacao = pygame.font.Font(caminho_fonte, 20)



# definir fontes:
fonte15 = pygame.font.SysFont('constantia', 15)
fonte30 = pygame.font.SysFont('constantia', 30)
fonte40 = pygame.font.SysFont('constantia', 40)
fonte_pontuacao = pygame.font.Font(caminho_fonte, 20)
base_font = pygame.font.Font(None, 32)

nome_usuario = ' '
senha = ''
novo_jogador = False
pontos = 0

# sons

son_jogo = pygame.mixer.Sound(os.path.join(diretorio_atual, 'sons', 'musica_jogo.ogg'))

som_bala = pygame.mixer.Sound(os.path.join(diretorio_atual, 'sons', 'laser.wav'))
son_jogo.set_volume(0.25)
son_jogo.set_volume(0.25)

canal_fundo = pygame.mixer.Channel(0)
canal_balas = pygame.mixer.Channel(1)


# Canal para o som do jogo (contínuo)
canal_jogo = pygame.mixer.Channel(0)


son_explosao = pygame.mixer.Sound(os.path.join(diretorio_atual, 'sons', 'explosion.wav'))
# aumentar volume
son_explosao.set_volume(1)

son_explosao2 = pygame.mixer.Sound(os.path.join(diretorio_atual, 'sons', 'explosion2.wav'))
son_explosao2.set_volume(1)


son_menu = pygame.mixer.Sound(os.path.join(diretorio_atual, 'sons', 'musica_menu.ogg'))
son_menu.set_volume(0.15)  # Define o volume inicial

# Para diminuir ainda mais o volume, você pode fazer:
# Multiplica o volume atual por 0.1 (10% do volume original)
son_menu.set_volume(0.1)
son_jogo = pygame.mixer.Sound(os.path.join(diretorio_atual, 'sons', 'musica_jogo.ogg'))
son_jogo.set_volume(0.10)

# cores
vermelho = (255, 0, 0)
verde = (0, 255, 0)
branco = (255, 255, 255)


# variáveis do jogo
alien_cooldown = 1000
ultimo_tiro_alien = pygame.time.get_ticks()
tempo_proximo_alien = pygame.time.get_ticks()
contagem = 3  # 3 segundos para comecar o jogo
ultima_contagem = pygame.time.get_ticks()
game_over = 0  # 0 jogo nao acabou, 1 = ganhou , -1 perdeu
menu = True
game_pause = False
alien_cooldown = 1000  # Tempo inicial entre aparições de inimigos
tempo_proximo_alien = 0
ultimo_tiro_alien = 0
inimigos_eliminados = 0
# criacao da tela de fundo
# Define a janela do jogo com as dimensões largura e altura
display = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("earth defender")


# Função para desenhar texto na tela
def draw_texto(texto, fonte, cor_texto, x, y):
    # Renderiza o texto com a fonte e a cor especificadas
    img = fonte.render(texto, True, cor_texto)
    display.blit(img, (x, y))  # Desenha o texto na tela nas coordenadas (x, y)


# Carrega a imagem de fundo da tela e redimensiona de acordo com a largura e altura da tela
bg = pygame.image.load(os.path.join(diretorio_atual, 'img', 'bg (1).png'))
bg = pygame.transform.scale(bg, (largura, altura))
bg_altura = bg.get_height()  # Obtém a altura da imagem de fundo
# Calcula o número de vezes que a imagem de fundo cabe na tela verticalmente
tiles = math.ceil(altura / bg_altura) + 1
rolagem = 0  # Inicializa a variável de rolagem do fundo
# botao reset

start_img = pygame.image.load(os.path.join(diretorio_atual, 'img', 'start.png'))
# diminuir tamanho do resetar_img
start_img = pygame.transform.scale(start_img, (80, 50))
exit_img = pygame.image.load(os.path.join(diretorio_atual, 'img', 'botao_sair.png'))
exit_img = pygame.transform.scale(exit_img, (80, 50))
resetar_img = pygame.image.load(os.path.join(diretorio_atual, 'img', 'restart.png'))
resetar_img = pygame.transform.scale(resetar_img, (60, 60))  # dim
pause_img = pygame.image.load(os.path.join(diretorio_atual, 'img', 'pause_button.png'))
voltar_img = pygame.image.load(os.path.join(diretorio_atual, 'img', 'voltar.png'))
voltar_img = pygame.transform.scale(voltar_img, (80, 50))

# deixar esse pause_button pequeno
pause_img = pygame.transform.scale(pause_img, (30, 30))
pause_img2 = pygame.image.load(os.path.join(diretorio_atual, 'img', 'resume_button.png'))
pause_img2 = pygame.transform.scale(pause_img2, (30, 30))


# x e y e dimensoes retangulo
input_rect = pygame.Rect(largura//2, 450, 170, 32)
senha_rect = pygame.Rect(largura//2, 500, 170, 32)
cor_ativa = pygame.Color('lightskyblue')
cor_passadados = pygame.Color('gray15')
cor = cor_passadados
ativa_user = False
ativa_senha = False

digitando = True
