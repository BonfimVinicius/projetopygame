
from variaveis import *
import json


nome_arquivo = "dados_jogo.json"

# Tenta carregar os dados existentes do arquivo, se houver
try:
    with open(nome_arquivo, "r") as file:
        dados_existentes = json.load(file)
except FileNotFoundError:
    dados_existentes = {"jogadores": []}

# Função para verificar se o nome de usuário existe na lista de jogadores
def verificar_usuario(nome_usuario, dados_existentes):
    for jogador in dados_existentes["jogadores"]:
        if isinstance(jogador, dict) and jogador.get("nome") == nome_usuario:
            return True
    return False

# Verifica se todos os itens em dados_existentes["jogadores"] são dicionários com a chave "pontos"
jogadores_validos = [jogador for jogador in dados_existentes["jogadores"] if isinstance(jogador, dict) and "pontos" in jogador]

# Ordena os jogadores válidos por pontos em ordem decrescente
jogadores_ordenados = sorted(jogadores_validos, key=lambda x: x["pontos"], reverse=True)

# Seleciona os 3 melhores jogadores
melhores_jogadores = jogadores_ordenados[:3]


def obter_posicao_ranking(nome_usuario, jogadores_ordenados):
    for idx, jogador in enumerate(jogadores_ordenados):
        if jogador["nome"] == nome_usuario:
            return idx + 1
    return None

