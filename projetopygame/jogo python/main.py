from variaveis import *
from banco_dados import *


def resetar_game():
    global pontos, contagem

    contagem = 3
    pontos = 0
    nave = Nave(int(largura / 2), altura - 100, 3)
    nave_grupo.empty()
    nave_grupo.add(nave)
    navesviloes_grupo.empty()
    planeta = Planeta(5)
    planeta_grupo.empty()
    planeta_grupo.add(planeta)
    alien = Navesviloes(random.randint(
        50, largura - 50), -50)  # Cria um novo vilão
    navesviloes_grupo.add(alien)
    balas_grupo.empty()
    viloes_balas_grupo.empty()

    return pontos, nave, planeta, contagem, alien


class Botao:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()  # cria um retangulo
        self.rect.topleft = (x, y)

    def draw(self):
        acao = False
        # obter posicao do mouse
        pos = pygame.mouse.get_pos()  # retornar coodernada x e y do mouse
        # checar se o mouse esta sobre o botao
        # verifica se o mouse esta sobre o botao
        if self.rect.collidepoint(pos):
            # lista que contem o click esquerdo e o direito  para o botao esquerdo o indice e 0 se el for igual a 1 ele foi clicado
            if pygame.mouse.get_pressed()[0] == 1:
                acao = True

        # desenha botao
        display.blit(self.image, (self.rect.x, self.rect.y))  # desenha o botao
        return acao


# classes
class Nave(pygame.sprite.Sprite):  # Define a classe Nave, que herda da classe pygame.sprite.Sprite
    # Método de inicialização da classe, recebe coordenadas x e y e a saúde da nave
    def __init__(self, x, y, saude):
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)

        # Carrega a imagem da nave com transparência
        self.image = pygame.image.load('img/principal.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (50, 50))  # Redimensiona a imagem da nave
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da nave
        self.rect.centerx = x
        self.rect.centery = y  # Define a posição inicial da nave
        self.mask = pygame.mask.from_surface(self.image)
        self.saude_incial = saude  # Define a saúde inicial da nave
        self.saude_restante = saude  # Define a saúde restante da nave
        # Guarda o tempo do último disparo da nave
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self):  # Método para atualizar a nave
        velocidade = 10  # Define a velocidade de movimento da nave
        game_over = 0  # Inicializa a variável de controle do estado do jogo
        cooldown = 500  # Define o tempo de cooldown para os tiros da nave
        key = pygame.key.get_pressed()  # Obtém as teclas pressionadas

        # Movimentação da nave
        if key[pygame.K_a] and self.rect.left > 0:  # Move a nave para a esquerda
            self.rect.x -= velocidade
        if key[pygame.K_d] and self.rect.right <= largura:  # Move a nave para a direita
            self.rect.x += velocidade
        if key[pygame.K_w] and self.rect.top > 0:  # Move a nave para cima
            self.rect.y -= velocidade
        if key[pygame.K_s] and self.rect.bottom < altura - 60:  # Move a nave para baixo
            self.rect.y += velocidade

        tempo_atual = pygame.time.get_ticks()  # Obtém o tempo atual do jogo

        # Disparo de tiros
        if key[pygame.K_SPACE] and tempo_atual - self.ultimo_tiro > cooldown:  # Dispara um tiro
            son_laser.play()  # Toca o som de disparo de laser
            # Cria um objeto de bala
            balas = Balas(self.rect.centerx, self.rect.top)
            balas_grupo.add(balas)  # Adiciona a bala ao grupo de balas
            self.ultimo_tiro = tempo_atual  # Atualiza o tempo do último disparo

        # Define a máscara de colisão da nave
        self.mask = pygame.mask.from_surface(self.image)

        if pygame.sprite.spritecollide(self, planeta_grupo, False, pygame.sprite.collide_mask):
            if key[pygame.K_s]:
                self.rect.y -= velocidade  # nao pode ir para baixo

        # Verifica se a nave foi destruída
        if self.saude_restante <= 0:
            # Cria uma explosão
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 1)
            # Adiciona a explosão ao grupo de explosões
            explosao_grupo.add(explosao)
            self.kill()  # Remove a nave
            game_over = -1  # Define que o jogo acabou

        if pygame.sprite.spritecollide(self, planeta_grupo, False, pygame.sprite.collide_mask):
            self.rect.center = [self.rect.centerx, self.rect.centery]

        # Verifica colisão com inimigos
        if pygame.sprite.spritecollide(self, navesviloes_grupo, False, pygame.sprite.collide_mask):
            # Cria uma explosão
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 1)
            # Adiciona a explosão ao grupo de explosões
            explosao_grupo.add(explosao)
            self.kill()  # Remove a nave
            nave.kill()
            game_over = -1  # Define que o jogo acabou

        return game_over  # Retorna o estado do jogo

    # Método para desenhar a barra de saúde da nave na tela
    def desenho_barrasaude(self):
        # Desenha a barra de saúde
        # Desenha o fundo vermelho da barra de saúde
        pygame.draw.rect(display, vermelho, (10, altura - 50, 100, 15))
        if self.saude_restante > 0:  # Verifica se a saúde restante é maior que zero
            # Desenha a barra de saúde verde proporcional à saúde restante
            pygame.draw.rect(display, verde, (10, altura - 50,
                             int(100 * (self.saude_restante / self.saude_incial)), 15))
        # Desenha o texto "SAÚDE"
        draw_texto('SAÚDE  NAVE', fonte15, branco, 5, altura - 30)


# Define a classe Balas, que herda da classe pygame.sprite.Sprite
class Planeta(pygame.sprite.Sprite):
    def __init__(self, saude):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        self.image = pygame.image.load(
            'img/planeta.png')  # Carrega a imagem da bala
        self.image = pygame.transform.scale(self.image, (600, 300))
        # self.image = pygame.transform.scale(self.image, (700, 300))
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da bala
        self.rect.x = largura // 2 - self.rect.width // 2  # Centraliza horizontalmente
        self.rect.y = altura - self.rect.height // 3  # Define a posição inicial da bala
        self.planeta_velocidade = 0.01
        self.mask = pygame.mask.from_surface(self.image)
        self.saude_planetainicial = saude
        self.saude_planetrestante = saude
        self.inavdiu = False

    def update(self):
        global pontos
        global game_over
        if pygame.sprite.spritecollide(self, navesviloes_grupo, True, pygame.sprite.collide_mask):
            pontos -= 1

            self.saude_planetrestante -= 1
        if self.saude_planetrestante <= 0:

            game_over = -2  # Define que o jogo acabou

        pygame.draw.rect(display, vermelho, (self.rect.x + 20,
                         (self.rect.top - 570), (self.rect.width - 100)//4,  15))
        if self.saude_planetrestante > 0:  # Verifica se a saúde
            pygame.draw.rect(display, verde, (self.rect.x + 20, (self.rect.top - 570), int(
                (self.rect.width - 100)//4*(self.saude_planetrestante/self.saude_planetainicial)),  15))
        draw_texto('INVASORES', fonte15, branco, 5, altura - 650)

        return game_over


# Define a classe Balas, que herda da classe pygame.sprite.Sprite
class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        self.image = pygame.image.load(
            'img/bullet.png')  # Carrega a imagem da bala
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da bala
        self.rect.center = [x, y]  # Define a posição inicial da bala

    def update(self):  # Método para atualizar a bala
        self.rect.y -= 5  # Move a bala para cima
        if self.rect.bottom < 0:  # Verifica se a bala saiu da tela
            self.kill()  # Remove a bala do jogo
        # Verifica colisão com inimigos
        if pygame.sprite.spritecollide(self, navesviloes_grupo, True):
            self.kill()  # Remove a bala do jogo
            son_explosao.play()  # Toca o som de explosão
            # Cria uma explosão
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 2)
            # Adiciona a explosão ao grupo de explosões
            explosao_grupo.add(explosao)
            global pontos
            pontos += 1  # Incrementa a pontuação

        def resetar_bala(self):
            self.bala = None


# Define a classe Navesviloes, que herda da classe pygame.sprite.Sprite
class Navesviloes(pygame.sprite.Sprite):
    def __init__(self, x, y):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        # Carrega uma imagem aleatória do vilão e atribui à variável image
        self.image = pygame.image.load(
            'img/vilao' + str(random.randint(1, 5)) + '.png')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem do vilão
        self.rect.center = [x, y]  # Define a posição inicial do vilão
        # Define a máscara de colisão do vilão
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):  # Método para atualizar o vilão
        self.rect.y += 2  # Move o vilão para baixo
        if self.rect.top > altura:  # Verifica se o vilão saiu da tela
            self.kill()  # Remove o vilão do jogo


# Define a classe Naves_viloes_balas, que herda da classe pygame.sprite.Sprite
class Naves_viloes_balas(pygame.sprite.Sprite):
    def __init__(self, x, y):  # Método de inicialização da classe, recebe coordenadas x e y
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        # Carrega a imagem do projétil do inimigo
        self.image = pygame.image.load('img/alien_bullet.png')
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem do projétil
        self.rect.center = [x, y]  # Define a posição inicial do projétil

    def update(self):  # Método para atualizar o projétil do inimigo
        self.rect.y += 5  # Move o projétil para baixo
        if self.rect.top > altura:  # Verifica se o projétil saiu da tela
            self.kill()  # Remove o projétil do jogo
            son_explosao2.play()  # Toca o som de explosão
        # Verifica colisão com a nave do jogador
        if pygame.sprite.spritecollide(self, nave_grupo, False, pygame.sprite.collide_mask):
            self.kill()  # Remove o projétil do jogo
            nave.saude_restante -= 1  # Reduz a saúde da nave do jogador
            # Cria uma explosão
            explosao = Explosoes(self.rect.centerx, self.rect.centery, 1)
            # Adiciona a explosão ao grupo de explosões
            explosao_grupo.add(explosao)


# Define a classe Explosoes, que herda da classe pygame.sprite.Sprite
class Explosoes(pygame.sprite.Sprite):
    # Método de inicialização da classe, recebe coordenadas x e y, e tamanho da explosão
    def __init__(self, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)  # Inicializa a classe pai (Sprite)
        self.images = []  # Lista para armazenar as imagens da explosão
        for num in range(1, 6):  # Loop para carregar as cinco imagens de explosão
            # Carrega a imagem de explosão correspondente
            img = pygame.image.load(f'img/exp{num}.png')
            if tamanho == 1:  # Verifica o tamanho da explosão
                # Redimensiona a imagem para 20x20 pixels
                img = pygame.transform.scale(img, (20, 20))
            if tamanho == 2:  # Verifica o tamanho da explosão
                # Redimensiona a imagem para 40x40 pixels
                img = pygame.transform.scale(img, (40, 40))
            if tamanho == 3:  # Verifica o tamanho da explosão
                # Redimensiona a imagem para 160x160 pixels
                img = pygame.transform.scale(img, (160, 160))
            self.images.append(img)  # Adiciona a imagem à lista de imagens
        self.index = 0  # Índice atual da imagem da explosão
        # Define a imagem atual da explosão
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()  # Obtém o retângulo da imagem da explosão
        self.rect.center = [x, y]  # Define a posição inicial da explosão
        self.contador = 0  # Contador para controlar a troca de imagens da explosão

    def update(self):  # Método para atualizar a explosão
        velocidade_explosao = 3  # Velocidade de troca de imagens da explosão
        self.contador += 1  # Incrementa o contador
        # Verifica se é hora de trocar para a próxima imagem e se ainda há imagens para mostrar
        if self.contador >= velocidade_explosao and self.index < len(self.images) - 1:
            self.contador = 0  # Reinicia o contador
            self.index += 1  # Avança para a próxima imagem da explosão
            # Define a próxima imagem da explosão
            self.image = self.images[self.index]

        # Verifica se todas as imagens da explosão foram mostradas e remove a explosão do jogo
        if self.index >= len(self.images) - 1 and self.contador >= velocidade_explosao:
            self.kill()  # Remove a explosão do jogo


# Cria grupos para armazenar diferentes tipos de sprites
nave_grupo = pygame.sprite.Group()  # Grupo para a nave do jogador
balas_grupo = pygame.sprite.Group()  # Grupo para as balas do jogador
navesviloes_grupo = pygame.sprite.Group()  # Grupo para os vilões
viloes_balas_grupo = pygame.sprite.Group()  # Grupo para as balas dos vilões
explosao_grupo = pygame.sprite.Group()  # Grupo para as explosões
planeta = Planeta(5)  # 5 aliens podem entrar
planeta_grupo = pygame.sprite.Group()
planeta_grupo.add(planeta)
botao_resetar = Botao(largura//2 - 200, altura//2 + 200, resetar_img)
botao_start = Botao(largura - 398, altura - 100, start_img)
botao_sair = Botao(largura//2 + 100, altura//2 + 200, exit_img)
botao_pause = Botao(largura//2 + 100, altura - 670, pause_img)
botao_pause2 = Botao(largura//2 + 170, altura - 670, pause_img2)
botao_voltar = Botao(largura//2 + 100, altura//2 + 200, voltar_img)
# Cria a nave do jogador e a adiciona ao grupo da nave
# Cria uma instância da classe Nave
nave = Nave(int(largura / 2), altura - 100, 5)
nave_grupo.add(nave)  # Adiciona a nave ao grupo de naves do jogador

run = True  # Variável de controle do loop principal do jogo
# retangulo caixa texto
while run:  # Loop principal do jogo
    # Desenha o fundo em loop, deslocando-o verticalmente
    for i in range(0, tiles):
        display.blit(bg, (0, i * bg_altura + rolagem))

    # Rola o fundo para cima
    rolagem -= 5
    # Reseta a rolagem se ultrapassar a altura do fundo
    if abs(rolagem) > bg_altura:
        rolagem = 0

    if menu == True:
        draw_texto("Top 3 jogadores:", fonte30, branco, 180, 250)
        for idx, jogador in enumerate(melhores_jogadores):
            draw_texto(f"{idx+1}. {jogador['nome']} - {jogador['pontos']
                                                       } pontos", fonte15, branco, 200, 300 + 40 * idx)
        draw_texto("Usuario : ", fonte30, branco, 175, 455)  # aqui
        draw_texto("Senha : ", fonte30, branco, 197, 505)  # aqui
        pygame.draw.rect(display, cor, senha_rect, 2)
        text_surface2 = base_font.render(senha, True, (255, 255, 255))
        display.blit(text_surface2, (senha_rect.x + 5, senha_rect.y + 5))
        senha_rect.w = max(100, text_surface2.get_width() + 10)

        text_surface = base_font.render(nome_usuario, True, (255, 255, 255))
        pygame.draw.rect(display, cor, input_rect, 2)
        display.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        if botao_sair.draw():
            run = False
        if botao_start.draw():
            if len(nome_usuario) > 1:
                if verificar_usuario(nome_usuario, dados_existentes):
                    print("Usuário existe na lista. Verificando senha...")
                    for jogador in dados_existentes["jogadores"]:
                        if isinstance(jogador, dict) and jogador.get("nome") == nome_usuario:
                            if "senha" in jogador and jogador["senha"] == senha:
                                print("Senha correta. Iniciando o jogo.")
                                menu = False
                                novo_jogador = False
                                pontos = jogador["pontos"]
                            else:
                                draw_texto(
                                    "Senha incorreta. Tente novamente.", fonte15, vermelho, 180, 400)
                                break
                else:
                    print(
                        f"Usuário {nome_usuario} não existe na lista. Adicionando como novo jogador.")
                    novo_jogador = True
                    menu = False
            else:
                draw_texto("Digite um nome de usuário válido.",
                           fonte15, vermelho, 180, 400)

    else:

        if game_pause == False:
            if botao_pause.draw():
                game_pause = True

        if game_pause == True:
            if botao_pause2.draw():
                game_pause = False

        else:

            # Verifica se a contagem regaressiva acabou
            if contagem == 0:
                tempo_atual = pygame.time.get_ticks()

                # Ajusta a dificuldade com base nos inimigos eliminados
                if inimigos_eliminados > 5:
                    alien_cooldown = 1500  # Reduz o tempo entre aparições dos inimigos
                if inimigos_eliminados > 10:
                    alien_cooldown = 800
                if inimigos_eliminados > 15:
                    alien_cooldown = 700
                if inimigos_eliminados > 20:
                    alien_cooldown = 600

                # Adiciona um novo vilão em intervalos regulares
                # Adiciona um novo vilão em intervalos regulares
                if tempo_atual - tempo_proximo_alien > alien_cooldown:
                    alien_image_width = 50
                    x = random.randint(alien_image_width,
                                       largura - alien_image_width)

                    # Verifica se o novo vilão não está muito próximo de um vilão existente
                    novo_alien = Navesviloes(x, -50)
                    if pygame.sprite.spritecollideany(novo_alien, navesviloes_grupo):
                        # Se houver colisão, não adiciona o novo vilão neste momento
                        pass
                    else:
                        navesviloes_grupo.add(novo_alien)
                        tempo_proximo_alien = tempo_atual

                # Adiciona tiros dos vilões
                if tempo_atual - ultimo_tiro_alien > alien_cooldown and len(viloes_balas_grupo) < 5 and len(navesviloes_grupo) > 0:
                    ataque_alien = random.choice(navesviloes_grupo.sprites())
                    alien_bala = Naves_viloes_balas(
                        ataque_alien.rect.centerx, ataque_alien.rect.bottom)
                    viloes_balas_grupo.add(alien_bala)
                    ultimo_tiro_alien = tempo_atual

                # Atualiza o estado do jogo se ainda não acabou
                if game_over == 0:
                    game_over = nave.update()  # Atualiza a nave do jogador
                    balas_grupo.update()  # Atualiza as balas do jogador
                    navesviloes_grupo.update()  # Atualiza os vilões
                    viloes_balas_grupo.update()  # Atualiza os tiros dos vilões
                    planeta_grupo.update()

                if game_over == - 1:  # Se o jogador perdeu
                    posicao_ranking = obter_posicao_ranking(
                        nome_usuario, jogadores_ordenados)

            # Atualizar dados do jogador

            # Salvar os dados do jogador

                    draw_texto('GAME OVER : NAVE DESTRUIDA!', fonte15, branco, int(
                        # Exibe a mensagem de "GAME OVER!"
                        largura / 2 - 100), int(altura / 2 - 50))
                    draw_texto(f'SUA POSIÇÃO NO RANKING: {posicao_ranking}', fonte15, (255, 255, 255), int(
                        largura / 2 - 100), int(altura / 2))
                    if botao_resetar.draw():
                        game_over = 0
                        pontos_atuais = pontos  # Salva os pontos atuais
                        pontos, nave, planeta, contagem, alien = resetar_game()
                        pontos += pontos_atuais  # Adiciona os pontos atuais aos pontos reiniciados

                    if botao_voltar.draw():
                        menu = True

                        # Se você tiver outras variáveis para resetar, adicione aqui

                if game_over == - 2:  # Se o jogador perdeu

                    posicao_ranking = obter_posicao_ranking(
                        nome_usuario, jogadores_ordenados)

                    draw_texto('GAME OVER: TERRA INVADIDA!', fonte15, (255, 255, 255), int(
                        largura / 2 - 100), int(altura / 2 - 50))
                    draw_texto(f'SUA POSIÇÃO NO RANKING  : {
                               posicao_ranking}', fonte15, (255, 255, 255), int(largura / 2 - 100), int(altura / 2))
                    if botao_resetar.draw():
                        # Acumula pontos ao reiniciar o jogo
                        game_over = 0
                        pontos_atuais = pontos  # Salva os pontos atuais
                        pontos, nave, planeta, contagem, alien = resetar_game()
                        pontos += pontos_atuais  # Adiciona os pontos atuais aos pontos reiniciados

                    if botao_voltar.draw():
                        run = True
                        menu = True

                        # Resetar variáveis relevantes para encerrar a sessão

                        # Se você tiver outras variáveis para resetar, adicione aqui
                        # Por exemplo, resetar nome de usuário, senha, pontos, etc.

            # Se ainda há contagem regressiva
            if contagem > 0:
                draw_texto('GET READY!', fonte40, branco, int(
                    # Exibe a mensagem "GET READY!"
                    largura / 2 - 110), int(altura / 2 + 50))
                draw_texto(str(contagem), fonte40, branco, int(
                    # Exibe a contagem regressiva
                    largura / 2 - 10), int(altura / 2 + 100))

                # Atualiza a contagem regressiva
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - ultima_contagem >= 1000:
                    contagem -= 1  # Decrementa a contagem regressiva
                    ultima_contagem = tempo_atual  # Atualiza o tempo da última contagem regressiva

        # Atualiza o grupo de explosões
        explosao_grupo.update()

        # Desenha as sprites na tela
        nave_grupo.draw(display)  # Desenha a nave do jogador
        balas_grupo.draw(display)  # Desenha as balas do jogador
        navesviloes_grupo.draw(display)  # Desenha os vilões
        viloes_balas_grupo.draw(display)  # Desenha as balas do vilao
        planeta_grupo.draw(display)

        explosao_grupo.draw(display)

        # desenha barra de saúde
        nave.desenho_barrasaude()

        pontos_texto = fonte_pontuacao.render(
            f'Pontos: {pontos}', True, (255, 255, 255))
        text_rect = pontos_texto.get_rect(
            center=(largura // 2, altura // 16))  # Centraliza o texto na tela
        display.blit(pontos_texto, text_rect)

    # eventos do pygame
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos) and not ativa_senha:
                ativa_user = True
            else:
                ativa_user = False

        if event.type == pygame.KEYDOWN:
            if ativa_user and not ativa_senha:
                if event.key == pygame.K_BACKSPACE:
                    nome_usuario = nome_usuario[:-1]
                else:
                    nome_usuario += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if senha_rect.collidepoint(event.pos) and not ativa_user:
                ativa_senha = True
            else:
                ativa_senha = False

        if event.type == pygame.KEYDOWN:
            if ativa_senha and not ativa_user:
                if event.key == pygame.K_BACKSPACE:
                    senha = senha[:-1]
                else:
                    senha += event.unicode

    cor = cor_ativa if ativa_senha or ativa_user else cor_passadados

    pygame.display.update()

    # fecha o pygame
pygame.quit()
