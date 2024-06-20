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

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    display.blit(img,(x,y))


# definir fontes:
fonte15 = pygame.font.SysFont('constantia', 15)
fonte30 = pygame.font.SysFont('constantia', 30)
fonte40 = pygame.font.SysFont('constantia', 40)
fonte_pontuacao = pygame.font.SysFont('Showcard Gothic',20)
base_font = pygame.font.Font(None,32)

nome_usuario = ' '
senha = ''
novo_jogador = False
pontos = 0

# sons
son_explosao = pygame.mixer.Sound('sons/explosion.wav')
# aumentar volume
son_explosao.set_volume(1)

son_explosao2 = pygame.mixer.Sound('img/explosion2.wav')
son_explosao2.set_volume(1)

son_laser = pygame.mixer.Sound('img/laser.wav')
son_laser.set_volume(1)

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

tela_inicio = pygame.display.set_mode((largura, altura))


# Função para desenhar texto na tela
def draw_texto(texto, fonte, cor_texto, x, y):
    img = fonte.render(texto, True, cor_texto)  # Renderiza o texto com a fonte e a cor especificadas
    display.blit(img, (x, y))  # Desenha o texto na tela nas coordenadas (x, y)

# Carrega a imagem de fundo da tela e redimensiona de acordo com a largura e altura da tela
bg = pygame.image.load('img/bg (1).png')
bg = pygame.transform.scale(bg, (largura, altura))
bg_altura = bg.get_height()  # Obtém a altura da imagem de fundo
tiles = math.ceil(altura / bg_altura) + 1  # Calcula o número de vezes que a imagem de fundo cabe na tela verticalmente
rolagem = 0  # Inicializa a variável de rolagem do fundo
#botao reset

start_img = pygame.image.load('img/start_btn (1).png')
start_img = pygame.transform.scale(start_img, (100, 50)) #diminuir tamanho do resetar_img
exit_img = pygame.image.load('img/sair.png')
exit_img = pygame.transform.scale(exit_img, (50, 50)) #diminuir tamanho do exit_img
resetar_img = pygame.image.load('img/restart.png')
resetar_img = pygame.transform.scale(resetar_img, (60, 60)) #dim
pause_img = pygame.image.load('img/pause_button.png')
voltar_img = pygame.image.load('img/voltar.png')
#diminuir tamanho botao sair
voltar_img = pygame.transform.scale(voltar_img, (50, 50))

#deixar esse pause_button pequeno
pause_img = pygame.transform.scale(pause_img, (30, 30))
pause_img2 = pygame.image.load('img/resume_button.png')
pause_img2 = pygame.transform.scale(pause_img2, (30, 30))


input_rect = pygame.Rect(largura//2,450,170,32) # x e y e dimensoes retangulo
senha_rect = pygame.Rect(largura//2,500,170,32)
cor_ativa= pygame.Color('lightskyblue')
cor_passadados = pygame.Color('gray15')
cor = cor_passadados
ativa_user = False
ativa_senha = False

digitando = True

