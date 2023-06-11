import pygame
import random
from collections import deque

# Inicialização do Pygame
pygame.init()
# Definição de cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Dimensões da janela do jogo
largura_tela = 800
altura_tela = 600

# Criação da janela do jogo
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo de Coletar Moedas")

# Classe para representar um nó no labirinto
class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbors = []
        self.visited = False
        

# Classe para representar o personagem
class Personagem(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.center = (largura_tela // 2, altura_tela // 2)
        self.velocidade = 5
        self.moedas_coletadas = 0

    def update(self):
        # Movimentação do personagem
        teclas_pressionadas = pygame.key.get_pressed()
        if teclas_pressionadas[pygame.K_LEFT]:
            self.rect.x -= self.velocidade
        if teclas_pressionadas[pygame.K_RIGHT]:
            self.rect.x += self.velocidade
        if teclas_pressionadas[pygame.K_UP]:
            self.rect.y -= self.velocidade
        if teclas_pressionadas[pygame.K_DOWN]:
            self.rect.y += self.velocidade
            
        # Tecla 'b' para executar a busca em largura
        if teclas_pressionadas[pygame.K_b]:
            # Encontrar uma moeda não visitada usando a busca em largura
                moedas_nao_visitadas = [moeda for moeda in moedas if not moeda.visited]
                if moedas_nao_visitadas:
                    objetivo = random.choice(moedas_nao_visitadas)
                    objetivo_node = labirinto[int(objetivo.rect.x / 50)][int(objetivo.rect.y / 50)]
                    resultado_largura = busca_largura(personagem_node, objetivo_node)
                    if resultado_largura:
                        print("Busca em Largura: Moeda encontrada!")
                        # Movimentar o personagem até a moeda
                        personagem.rect.x = objetivo.rect.x
                        personagem.rect.y = objetivo.rect.y                     

        # Tecla 'u' para executar a busca uniforme
        if teclas_pressionadas[pygame.K_u]:
            # Encontrar uma moeda não visitada usando a busca uniforme
            moedas_nao_visitadas = [moeda for moeda in moedas if not moeda.visited]
            if moedas_nao_visitadas:
                objetivo = random.choice(moedas_nao_visitadas)
                objetivo_node = labirinto[int(objetivo.rect.x / 50)][int(objetivo.rect.y / 50)]
                resultado_uniforme = busca_uniforme(personagem_node, objetivo_node)
                if resultado_uniforme:
                    print("Busca Uniforme: Moeda encontrada!")
                    # Movimentar o personagem até a moeda
                    personagem.rect.x = objetivo.rect.x
                    personagem.rect.y = objetivo.rect.y
                    
         # Tecla 'd' para executar a busca em profundidade
        if teclas_pressionadas[pygame.K_d]:
            # Encontrar uma moeda não visitada usando a busca em profundidade
            moedas_nao_visitadas = [moeda for moeda in moedas if not moeda.visited]
            if moedas_nao_visitadas:
                objetivo = random.choice(moedas_nao_visitadas)
                objetivo_node = labirinto[int(objetivo.rect.x / 50)][int(objetivo.rect.y / 50)]
                resultado_profundidade = busca_profundidade(personagem_node, objetivo_node)
                if resultado_profundidade:
                    print("Busca em Profundidade: Moeda encontrada!")
                    # Movimentar o personagem até a moeda
                    personagem.rect.x = objetivo.rect.x
                    personagem.rect.y = objetivo.rect.y

        # Tecla 'a' para executar o algoritmo A*
        if teclas_pressionadas[pygame.K_a]:
            # Encontrar uma moeda não visitada usando o algoritmo A*
            moedas_nao_visitadas = [moeda for moeda in moedas if not moeda.visited]
            if moedas_nao_visitadas:
                objetivo = random.choice(moedas_nao_visitadas)
                objetivo_node = labirinto[int(objetivo.rect.x / 50)][int(objetivo.rect.y / 50)]
                resultado_aestrela = a_estrela(personagem_node, objetivo_node)
                if resultado_aestrela:
                    print("Algoritmo A*: Moeda encontrada!")
                    # Movimentar o personagem até a moeda
                    personagem.rect.x = objetivo.rect.x
                    personagem.rect.y = objetivo.rect.y
                    
        # Verifica se o personagem colidiu com alguma moeda
        colisoes = pygame.sprite.spritecollide(self, moedas, True)
        for moeda in colisoes:
            # Aqui você pode adicionar a lógica de pontuação ou qualquer outra ação ao coletar uma moeda
            self.moedas_coletadas += 1
            print("Moeda coletada!")

# Classe para representar as moedas
class Moeda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(BRANCO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(largura_tela - self.rect.width)
        self.rect.y = random.randrange(altura_tela - self.rect.height)
        self.visited = False


# Criação dos grupos de sprites
todos_sprites = pygame.sprite.Group()
moedas = pygame.sprite.Group()

# Criação do personagem
personagem = Personagem()
todos_sprites.add(personagem)

# Criação das moedas
for _ in range(9):
    moeda = Moeda()
    todos_sprites.add(moeda)
    moedas.add(moeda)

def busca_largura(inicio, objetivo):
    fila = deque()
    fila.append(inicio)

    while fila:
        atual = fila.popleft()

        if atual == objetivo:
            return True

        for vizinho in atual.neighbors:
            if not vizinho.visited:
                fila.append(vizinho)
                vizinho.visited = True

                # Marcar o vizinho como visitado antes de avançar para o próximo nível
                vizinho.visited = True

    return False

# Função para realizar a busca em profundidade
def busca_profundidade(atual, objetivo):
    if atual == objetivo:
        return True

    atual.visited = True

    for vizinho in atual.neighbors:
        if not vizinho.visited:
            if busca_profundidade(vizinho, objetivo):
                return True

    return False

# Função para realizar a busca uniforme
def busca_uniforme(inicio, objetivo):
    fila_prioridade = []
    fila_prioridade.append((0, inicio))

    while fila_prioridade:
        custo, atual = min(fila_prioridade, key=lambda x: x[0])  # Usar o custo como chave de comparação

        if atual == objetivo:
            return True

        for vizinho in atual.neighbors:
            if not vizinho.visited:
                custo = 1  # Custo fixo de 1 para todos os vizinhos no exemplo
                fila_prioridade.append((custo, vizinho))
                vizinho.visited = True

        # Verificar se o elemento está presente na lista antes de removê-lo
        if (custo, atual) in fila_prioridade:
            fila_prioridade.remove((custo, atual))

    return False

# Função para calcular a heurística (distância de Manhattan) entre dois nós
def calcular_heuristica(node_atual, node_destino):
    return abs(node_destino.x - node_atual.x) + abs(node_destino.y - node_atual.y)

# Função para realizar o algoritmo A*
def a_estrela(inicio, objetivo):
    fila_prioridade = []
    fila_prioridade.append((0, inicio))

    while fila_prioridade:
        _, atual = min(fila_prioridade, key=lambda x: x[0])  # Usar o custo como chave de comparação

        if atual == objetivo:
            return True

        for vizinho in atual.neighbors:
            if not vizinho.visited:
                custo = 1  # Custo fixo de 1 para todos os vizinhos no exemplo
                heuristica = calcular_heuristica(vizinho, objetivo)
                custo_total = custo + heuristica
                fila_prioridade.append((custo_total, vizinho))
                vizinho.visited = True

        # Verificar se o elemento está presente na lista antes de removê-lo
        if (_, atual) in fila_prioridade:
            fila_prioridade.remove((_, atual))

    return False

# Criação do labirinto e definição dos nós e vizinhos
labirinto = []
for i in range(largura_tela // 50):
    linha = []
    for j in range(altura_tela // 50):
        node = Node(i, j)
        linha.append(node)
    labirinto.append(linha)

for i in range(largura_tela // 50):
    for j in range(altura_tela // 50):
        node = labirinto[i][j]
        if i > 0:
            node.neighbors.append(labirinto[i-1][j])  # Vizinho acima
        if i < largura_tela // 50 - 1:
            node.neighbors.append(labirinto[i+1][j])  # Vizinho abaixo
        if j > 0:
            node.neighbors.append(labirinto[i][j-1])  # Vizinho à esquerda
        if j < altura_tela // 50 - 1:
            node.neighbors.append(labirinto[i][j+1])  # Vizinho à direita

# Loop principal do jogo
jogo_ativo = True
clock = pygame.time.Clock()

while jogo_ativo:
    # Eventos do jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            jogo_ativo = False

    # Verificar se o personagem está em um nó do labirinto
    personagem_node = labirinto[int(personagem.rect.x / 50)][int(personagem.rect.y / 50)]

    # Condição de encerramento do jogo
    if personagem.moedas_coletadas == 9:
        print("Fim do jogo. Você coletou 10 moedas!")
        jogo_ativo = False

    # Atualização dos sprites
    todos_sprites.update()

    # Renderização
    tela.fill(PRETO)
    todos_sprites.draw(tela)

    # Atualização da tela
    pygame.display.flip()
    clock.tick(60)

# Encerramento do Pygame
pygame.quit()