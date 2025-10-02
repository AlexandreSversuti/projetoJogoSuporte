import pygame, random
from pygame.locals import * #importa funções & módulos da biblioteca pygame
from sys import exit

pygame.init()

# CONFIG. DE INICIALIZAÇÃO DA TELA
largura = 1080
altura = 450
tela = pygame.display.set_mode((largura,altura)) #cria a tela do jogo
tempo = pygame.time.Clock() #relógio interno controlador da velocidade do jogo
pygame.display.set_caption('Jump, Bruno! Jump')
fonte = pygame.font.SysFont('img/fonte_game_over3.otf', 25, True, False)
# FIM DA CONFIG. DE INICIALIZAÇÃO DA TELA

# CONFIG. DE INICIALIZAÇÃO DA TRILHA SONORA E DOS EFEITOS SONOROS
# Carregar a trilha de fundo do menu
pygame.mixer.init()
pygame.mixer.music.load('trl/musica1.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)
# Carregar os efeitos sonoros
som_pulo = pygame.mixer.Sound('trl/sompulo.mp3')
som_pulo.set_volume(0.7)
som_grito = pygame.mixer.Sound('trl/somgrito.mp3')
som_grito.set_volume(1.0)
som_choro = pygame.mixer.Sound('trl/somchoro.mp3')
som_choro.set_volume(1.0)
som_emagrecendo = pygame.mixer.Sound('trl/somemagrecendo.mp3')
som_emagrecendo.set_volume(1.0) 
vezes_tocado = 0
# FIM DA CONFIG. DE INICIALIZAÇÃO DA TRILHA SONORA E EFEITOS SONOROS

# CONFIG. DE INICIALIZAÇÃO DOS FUNDOS
fundos = [
    pygame.image.load("img/fundo0.png").convert(), # Fundo que só irá aparecer no inicio
    pygame.image.load("img/fundo1.png").convert(),
    pygame.image.load("img/fundo2.png").convert(),
    pygame.image.load("img/fundo3.png").convert(),
    pygame.image.load("img/fundo4.png").convert()
]
# Inicial: fundo0 e fundo1
fundo1_img = fundos[0]
# Escolhe fundos aleatorios tirando o fundo inicial
fundo2_img = random.choice(fundos[1:]) 
fundo_x1 = 0
fundo_x2 = largura
velocidade_fundo = 5
chao = 345

# Flag para não usar mais o fundo0
fundo0_usado = True
# FIM DA CONFIG. DE INICIALIZAÇÃO DO FUNDO

# CONFIG. DE INICIALIZAÇÃO DO MENU INICIAL
# Upload do nome do jogo
nome_jogo = pygame.image.load('img/nome2.0.png').convert_alpha()
nome_jogo = pygame.transform.scale_by(nome_jogo, 1.2)
fonte_iniciar = pygame.font.SysFont('img/fonte_game_over3.otf', 17, True, True)
iniciar = fonte_iniciar.render('Aperte SETA PARA CIMA ou ESPAÇO para inciar...', True, (248, 248, 248))
posicaox_iniciar = 800
posicaoy_iniciar = 290
# FIM DA CONFIG. DE INICIALIZAÇÃO DO MENU INICIAL

# CONFIG. DE INICIALIZAÇÃO DO BRUNO
bruno_x = 350
bruno_y = 345
bruno_inicial_x = 350
bruno_inicial_y = 345
# Bruno andando
bruno_01 = pygame.image.load('img/bruno_01.png').convert_alpha() #Bruno precisa aparecer com fundo recortado
bruno_02 = pygame.image.load('img/bruno_02.png').convert_alpha() #Bruno precisa aparecer com fundo recortado
# Bruno pulando
bruno_03 = pygame.image.load('img/bruno_03.png').convert_alpha() #Bruno precisa aparecer com fundo recortado

# Config da animação do Bruno
frame_atual_bruno = 0 # Controla se o Bruno mostra bruno_01 ou bruno_02
pulando = False # Inicializa como não pulando
ultimo_tempo_bruno = pygame.time.get_ticks() # Inicializa com o tempo atual
intervalo_frame_bruno = 150 #milissegundos entre cada frame 
# FIM DA CONFIG. DE INICIALIZAÇÃO DO BRUNO 

# CONFIG. DE INICIALIZAÇÃO DA SALADA VOADORA
# Config da salada voadora
salada_spritesheet = pygame.image.load('img/alface_voador.png').convert_alpha()
#-----Converter Spritesheet para 23*64x64 (Cada frame ficará 64x64)-----#
scale_x = 64*23 / salada_spritesheet.get_width()   # 23 frames de 64 px cada
scale_y = 64 / salada_spritesheet.get_height()    # altura de 64 px
salada_spritesheet = pygame.transform.scale(
    salada_spritesheet,
    (int(salada_spritesheet.get_width()*scale_x),
     int(salada_spritesheet.get_height()*scale_y))
)
# Cria uma lista para armazenar os frames da salada voadora
frames_salada = []

# Loop para os frames da salada voadora
# Corta os frames
for salada in range(23):
    frame_2 = salada_spritesheet.subsurface(pygame.Rect(salada*64,0,64,64))
    frames_salada.append(frame_2)

# Variável para a salada começar fora da tela
salada_x = largura + 100 
salada_y = 350

# Variável de controle de animação da salada
salada_frame_index = 0
salada_velocidade_animacao = 0.2
salada_velocidade = 7
# FIM DA CONFIG. DE INICIALIZAÇÃO DA SALADA VOADORA

# CONFIG. DA ANILHA
#-----Converter imagem da anilha para 128x128-----#
imagem = pygame.image.load('img/anilha.png').convert_alpha()
imagem_x  = imagem.get_width()
imagem_y = imagem.get_height()
fator = 2
nova_imagem_x = imagem_x * fator
nova_imagem_y = imagem_y * fator
# Imagem da anilha já convertida e posições iniciais
anilha = pygame.transform.scale(imagem, (nova_imagem_x, nova_imagem_y))
anilha_x = largura + 10
anilha_y = 325
velocidade_anilha = 5
# FIM DA CONFIG. DA ANILHA

# CONFIG. DE INICIALIZAÇÃO DO HAMBURGUER
burguer_x = 880
burguer_y = 350
hamburguer_01 = pygame.image.load('img/hamburguer_01.png').convert_alpha() # Hamburguer precisa aparecer com fundo recortado
hamburguer_02 = pygame.image.load('img/hamburguer_02.png').convert_alpha() # Hamburguer precisa aparecer com fundo recortado

# Config da animação do Hamburguer
frame_atual_hamburguer = 0 # Inicializa como frame 0 (Hamburguer_01)
ultimo_tempo_hamburguer = pygame.time.get_ticks() # Inicializa com o tempo atual
intervalo_frame_hamburguer = 150 # Milissegundos entre cada frame 
# FIM DA CONFIG. DE INICIALIZAÇÃO DO HAMBURGUER

# CONFIG. DE INICIALIZAÇÃO DA GRAVIDADE
# Gravidade Bruno
velocidade_y_bruno = 0 # controla a velocidade vertical do Bruno (pra pular e cair).
G = 0.5 # gravidade
# Gravidade Hamburguer
velocidade_y_burguer = 0
# FIM DA CONFIG. DE INICIALIZAÇÃO DA GRAVIDADE

# CONFIG. DE INICIALIZAÇÃO DA VELOCIDADE
velocidade_bruno_x = 0
V = 5
# FIM DA CONFIG. DE INICIALIZAÇÃO DA VELOCIDADE

# CONFIG. DE INICIALIZAÇÃO DOS PULOS/PONTOS/DIFICULDADE
#Contador de Pulos
pulos = 0
hamburguer_pulou = False

# Pontos & Texto
pontos = 0
cor = (255, 255, 255)
posicaox_texto = 10
posicaoy_texto = 10

# Recorde
recordes = []
maior_recorde = 0

# Controlador da dificuldade do jogo (Aumento de velocidade)
dificuldade = 1.0
ultimo_marco = 0
# FIM DA CONFIG. DE INICIALIZAÇÃO DOS PULOS E DOS PONTOS

# CONFIG. DE INICIALIZAÇÃO DA TELA GAME OVER
# Game over
game_over = fonte.render('GAME OVER!', False, (255, 255, 255))
fonte_game_over = pygame.font.Font('img/fonte_game_over3.otf', 120)
posicaox_gameover = 210
posicaoy_gameover = 120
# Reiniciar
fonte_reiniciar = pygame.font.Font('img/fonte_game_over3.otf', 20)
posicaox_reiniciar = 305
posicaoy_reiniciar = 335
# FIM DA CONFIG. DE INICIALIZAÇÃO DA TELA GAME OVER

# CONFIG "Bruno está emagrecendo!"
bruno_emagrecendo = True
cores_texto = [(255, 0, 0), (0, 255, 0), (0, 150, 255), (255, 255, 0)]
brunox_texto = largura//2
brunoy_texto = 20

# CONFIG. ADICIONAIS DE INICIALIZAÇÃO
# Flag para rodar o jogo 
rodando = True
jogo_iniciado = False
# FIM DAS CONFIG. ADICIONAIS DE INICIALIZAÇÃO

# LOOP PRINCIPAL
while rodando:
    for event in pygame.event.get():
         teclas_pressionadas = pygame.key.get_pressed()
         if event.type == QUIT:
            pygame.quit()
            exit()
         if event.type == KEYDOWN:
             if event.key == K_UP or event.key == K_w or event.key == K_SPACE:
                if not jogo_iniciado:
                   jogo_iniciado = True
                   pygame.mixer.music.load('trl/musica2.mp3')
                   pygame.mixer.music.play(-1)
                pulando = True
                if pulos < 2: # Permite apenas dois pulos
                     som_pulo.play()
                     pulos +=1 # Conta o número de pulos
                     velocidade_y_bruno = -10  # impulso inicial pra cima
                     
    if not jogo_iniciado:
      # Inicia no menu
      tela.fill((0,0,0))
      tela.blit(fundo1_img, (0,0))
      tela.blit(nome_jogo, (620, -170))  
      tela.blit(bruno_01, (bruno_inicial_x, bruno_inicial_y))
      tela.blit(iniciar, (posicaox_iniciar, posicaoy_iniciar))
      
    else:
        # Jogo é iniciado
        # CONFIG. DO FUNDO
        # Preenche a tela com a cor preta
        tela.fill((0,0,0)) 
        # Coloca os fundos iniciais na tela
        tela.blit(fundo1_img, (fundo_x1, 0)) 
        tela.blit(fundo2_img, (fundo_x2, 0)) 

        # Movimenta os fundos
        fundo_x1 -= velocidade_fundo * dificuldade
        fundo_x2 -= velocidade_fundo * dificuldade

        # Loop dos fundos: Se um sair da tela, manda para o fim do outro
        if fundo_x1 <= -largura:
            # Se o fundo inicial já usado ele torna aleatório as escolhas dos fundos 
            if fundo0_usado:
                fundo1_img = random.choice(fundos[1:])
            # Senão ele coloca o fundo inicial 
            else:
                fundo1_img = fundos[0]
                fundo0_usado = True 
            fundo_x1 = fundo_x2 + largura
        
        # Verifica se o fundo já saiu completamente da tela para mandar outro
        if fundo_x2 <= -largura:
            if fundo0_usado:
                fundo2_img = random.choice(fundos[1:])
                fundo_x2 = fundo_x1 + largura
        # FIM DA CONFIG. DO FUNDO

        # CONFIG. RECORDE NA TELA
        recorde_na_tela = fonte.render(f'RECORDE: {int(maior_recorde)}', False, (255,255,255))
        tela.blit(recorde_na_tela, (posicaox_texto, posicaoy_texto + 18))
        if pontos >= maior_recorde:
            maior_recorde = pontos
        # FIM DA CONFIG DO RECORDE NA TELA

        # CONFIG. DA ANILHA
        anilha_x -= velocidade_anilha * dificuldade
        if anilha_x <= -128:
            anilha_x = largura + random.randint(500,600)
        tela.blit(anilha, (anilha_x, anilha_y))

        # CONFIG. DA SALADA VOADORA
        # Armazena a imagem da salada dentro de um variável
        salada_frame_atual = frames_salada[int(salada_frame_index)]
        # Desenha a imagem na tela
        tela.blit(salada_frame_atual,(salada_x, salada_y))

        # Atualiza animação da salada
        salada_frame_index += salada_velocidade_animacao
        if salada_frame_index >= len(frames_salada):
            salada_frame_index = 0
        
        # Movimento da salada
        salada_x -= salada_velocidade * dificuldade

        # Loop da salada
        if salada_x <= -64:
            # Escolhe aleatoriamente onde a salada irá aparecer nos eixos x e y
            salada_x = largura + random.randint(200,600)
            salada_y = random.randint(210,345)
        # FIM DA CONFIG. DA SALADA VOADORA
        
        # CONFIG. DO HAMBURGUER
        # Troca de frames Hamburguer
        tempo_atual_hamburguer = pygame.time.get_ticks() # Sempre atualiza o tempo atual
        if tempo_atual_hamburguer - ultimo_tempo_hamburguer >= intervalo_frame_hamburguer:
            ultimo_tempo_hamburguer = tempo_atual_hamburguer
            frame_atual_hamburguer = 1 - frame_atual_hamburguer # Alterna entre 0 e 1

        # Desenha o Hamburguer
        if frame_atual_hamburguer == 0:
            tela.blit(hamburguer_01, (burguer_x, burguer_y)) # Desenha o Hamburguer andando
        else:
            tela.blit(hamburguer_02, (burguer_x, burguer_y)) # Desenha o Hamburguer andando
        # FIM DA CONFIG. DO HAMBURGUER
        
        # CONFIG. PULO AUTOMÁTICO HAMBURGUER
        # Faz todas as verificações para o Hamburguer não pular sem para (not) ou desnecessário (salada_y > burguer_y - 50)
        if burguer_x < salada_x < burguer_x + 105 * dificuldade and not hamburguer_pulou and burguer_y >= 350 and salada_y > burguer_y - 50:
             velocidade_y_burguer -= 12  # Impulso para cima
             hamburguer_pulou = True # Não pula mais de uma vez

        if burguer_x < anilha_x < burguer_x + 105 * dificuldade and not hamburguer_pulou and burguer_y >= 350 and anilha_y > burguer_y - 50:
             velocidade_y_burguer -= 12 # Impulso para cima
             hamburguer_pulou = True # Não pula mais de uma vez
            
        # Aplica a gravidade
        velocidade_y_burguer += G
        burguer_y += velocidade_y_burguer

        # Impede de atravessar o chão
        if burguer_y > 350:
            burguer_y = 350
            velocidade_y_burguer = 0
            hamburguer_pulou = False
        # FIM DA CONFIG. DO PULO AUTOMÁTICO HAMBURGUER
    
        # CONFIG. DO BRUNO NA TELA
        # Verificações para o Bruno andar na tela apenas depois do jogo iniciar
        # Andar para a direita até o limite permitido
        if teclas_pressionadas[K_RIGHT] or teclas_pressionadas[K_d]:
            if bruno_x < 600:
                bruno_x += 6
        # Andar para a esquerda até o limite permitido
        if teclas_pressionadas[K_LEFT] or teclas_pressionadas[K_a]:
            if bruno_x > 0:
                bruno_x -= 6
        # Cair mais rápido
        if teclas_pressionadas[K_DOWN] or teclas_pressionadas[K_s]:
            velocidade_y_bruno += 2
        # Aplica a sensação de gravidade quando o bruno cai
        velocidade_y_bruno += G 
        bruno_y += velocidade_y_bruno

        # Impede de atravessar a coordenada do "chão"
        if bruno_y > chao:
            bruno_y = chao

        # Reseta a quantidade de pulos limite do Bruno (2) quando está na coordenada do "chão"
        if bruno_y >= chao:
            bruno_y = chao
            velocidade_y_bruno = 0
            pulos = 0

        # Troca de frames Bruno
        # Sempre atualiza a variável do tempo atual
        tempo_atual_bruno = pygame.time.get_ticks() 
        # Verifica o intervalo de tempo com a fórmula do tempo registrado fora do loop menos o tempo que está  sempre atualizando
        if tempo_atual_bruno - ultimo_tempo_bruno >= intervalo_frame_bruno: 
            # Atuazliza o tempo registrado fora do loop
            ultimo_tempo_bruno = tempo_atual_bruno
            # Alterna entre os frames (andando) 0 e 1
            frame_atual_bruno = 1 - frame_atual_bruno 
        
        # Verifica se o Bruno está no chão
        if bruno_y >= chao:
            # Se sim destiva o dele pulando
            pulando = False 

        # Desenha o Bruno
        if pulando:
            tela.blit(bruno_03, (bruno_x, bruno_y)) # Desenha o Bruno pulando
        elif frame_atual_bruno == 0:
            tela.blit(bruno_01, (bruno_x, bruno_y)) # Desenha o Bruno andando
        else:
            tela.blit(bruno_02, (bruno_x, bruno_y)) # Desenha o Bruno andando
        # FIM DA CONFIG. DO BRUNO NA TELA

        # CONFIG. DA COLISÃO DO BRUNO COM OS OBSTÁCULOS
        # Colisão do Bruno e a Salada voadora
        # Cria quadrados invisíveis que são utilizados na colisão para cada frame do bruno e da salada 
        bruno_colisao_anilha = pygame.Rect(bruno_x, bruno_y, bruno_01.get_width()/3.5, bruno_01.get_height()/3.5) 
        bruno_colisao_salada = pygame.Rect(bruno_x, bruno_y, bruno_01.get_width()/2, bruno_01.get_height()/2)
        salada_colisao = pygame.Rect(salada_x, salada_y, 55, 55)
        anilha_colisao = pygame.Rect(anilha_x, anilha_y, 55, 55)

        # Verifica a colisão de qualquer frame(quadrado invisível) do bruno com qualquer frame(quadrado invisível) da salada
        if bruno_colisao_salada.colliderect(salada_colisao) or bruno_colisao_anilha.colliderect(anilha_colisao):
            # Se o Bruno colidir, ele grita e chora
            som_grito.play()
            pygame.time.delay(500) #Espera meio segundo
            som_choro.play()
            # Música de Game over
            pygame.mixer.music.load('trl/musica3.mp3')
            pygame.mixer.music.play(-1)

            # Variável para entrar no loop
            morreu = True
            # Quando ele morrer irá armazenar o maior recorde da lista de recordes
            recordes.append(pontos)
            maior_recorde = max(recordes)

            # Loop na qual cria dois caminhos após a colisão do bruno com a salada: Fechar o jogo ou reiniciar
            while morreu:
                # Mostra a tela game over
                tela.fill((10, 10, 10))
                texto_game_over = fonte_game_over.render('GAME OVER', True, (255, 255, 255))
                tela.blit(texto_game_over, (posicaox_gameover, posicaoy_gameover))
                # Mostra a mensagem de reiniciar 
                texto_reiniciar = fonte_reiniciar.render('Aperta a tecla (r) para começar denovo...', True, (255, 255, 255))
                tela.blit(texto_reiniciar, (posicaox_reiniciar, posicaoy_reiniciar))
                # Atualiza a tela
                pygame.display.flip()
                tempo.tick(60)
                # Inici o Loop de dois caminhos depois do game over: Fechar o programa ou reiniciar
                for event in pygame.event.get():
                    # Verifica se o player quiser fechar o jogo (clicar no x do canto superior direito)
                    if event.type == QUIT:
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN:
                        # Verifica se a tecla r for pressionada, pois esta será a forma  de reiniciar
                        if event.key == K_r:
                            # Reinicia todos os valores do jogo
                            pygame.time.delay(100)
                            pontos = 0
                            vezes_tocado = 0
                            pulos = 0
                            bruno_y = chao
                            bruno_x = 350
                            anilha_x = largura + 10
                            anilha_y = 325
                            salada_x = largura + 100
                            salada_y = 350
                            burguer_x = 880
                            fundo_x1 = 0
                            fundo_x2 = largura
                            dificuldade = 1.0
                            ultimo_marco = 0
                            velocidade_y_bruno = 0
                            frame_atual_bruno = 0
                            frame_atual_hamburguer = 0
                            salada_frame_index = 0
                            fundo1_img = fundos[0]
                            fundo2_img = random.choice(fundos[1:])
                            fundo0_usado = True
                            jogo_iniciado = False
                            morreu = False
                            pygame.mixer.music.load('trl/musica1.mp3')
                            pygame.mixer.music.play(-1)
                            
        # FIM DA CONFIG. DA COLISÃO DO BRUNO COM OS OBSTÁCULOS

        # CONFIG. DA PONTUAÇÃO
        # Aumenta os pontos enquanto o jogo está rodando
        pontos += 0.3 * dificuldade
        # Cria o texto atualizado a cada frame
        texto = fonte.render(f"PONTOS: {int(pontos)}", False, (cor))
        tela.blit(texto,(posicaox_texto,posicaoy_texto))
        # FIM DA CONFIG. DA PONTUAÇÃO

        # CONFIG. "BRUNO ESTÁ EMAGRECENDO!"
        if bruno_emagrecendo:
            fonte2 = pygame.font.SysFont('img/fonte_game_over3.otf', 40, False, False)
            tempo_atual = pygame.time.get_ticks()
            indice_cor = (tempo_atual // 300) % len(cores_texto)
            cor_piscando = cores_texto[indice_cor]
            texto_emagrecendo = fonte2.render(f"BRUNO ESTÁ EMAGRECENDO!", True, cor_piscando)
            tela.blit(texto_emagrecendo, (brunox_texto, brunoy_texto))
        # Lógica para aparecer e desaparecer o texto
        if 3000 < int(pontos) < 3200:
             if vezes_tocado < 1:
                 som_emagrecendo.play()
                 vezes_tocado += 1
             bruno_emagrecendo = True
             
        else:
             bruno_emagrecendo = False
        # FIM DA CONFIG. "BRUNO ESTÁ EMAGRECENDO!"

        # CONFIG. DA DIFICULDADE
        #Aumenta a dificuldade
        if int(pontos) // 200 > ultimo_marco:
            dificuldade += 0.1 #Aumenta dificuldade em 10%
            ultimo_marco = int(pontos) // 200
            dificuldade = min(dificuldade, 4.0) #limite

            print(f"Dificuldade aumentou. Agora é{dificuldade: .1f}")
        # FIM DA CONFIG. DA DIFICULDADE

    # CONFIG. DE ATUALIZAÇÃO DOS FRAMES DO JOGO INTEIRO
    # Atualiza a tela inteira
    pygame.display.flip()
    # Tudo é atualizado neste tempo
    tempo.tick(60) 
    # FIM DA CONFIG. DE ATUALIZAÇÃO DOS FRAMES DO JOGO INTEIRO 
    # FIM DO LOOP PRINCIPAL
    