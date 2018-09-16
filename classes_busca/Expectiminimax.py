# Define a classe Expectiminimax, responsável por realizar uma busca por possibilidades de ações para o jogador IA.

# Escrito por: Luiz Felipe, Vítor Costa, Renato Bastos

from classes_busca.Estado import *
from classes_base.Mesa import *
import copy
import math

PROFUNDIDADE = 5  # Valor deve ser modificado, usado por enquanto apenas como placeholder.
PROBABILIDADE = 2

PECA = 0
POSICAO = 1

############Precisa finalizar esta função resultado().############
# Retorna o resultado da execução de uma dada ação (i.e. inserção de peça) num dado estado (i.e. mesa/tabuleiro). Ou
# seja, retorna o estado resultado da ação/jogada tomada.
def resultado(estado, acao):
    novoTipo = 0
    if (estado.tipo == Estado.MAX or estado.tipo == Estado.MIN): novoTipo = Estado.CHANCE
    if (estado.tipo == Estado.CHANCE): novoTipo = (Estado.MAX if (estado.tipoAnterior == Estado.MIN) else Estado.MIN)
    tipoAnterior = estado.tipo
    novaMesa = copy.deepcopy(estado.mesa)
    novoJogador = copy.deepcopy(estado.jogador)
    novoOponente = copy.deepcopy(estado.oponente)
    novaMesa.adicionarNaMesa(acao[PECA], acao[POSICAO])
    novoJogador.setaJogou(True)
    novoJogador.setaVez(False)
    novoOponente.setaVez(True)
    if ((novoJogador.jaGanhou() or novoOponente.jaGanhou()) or
            (not novoJogador.jogouRodada() or not novoOponente.jogouRodada())):
        estado.setaEstadoTerminal(True)
    return Estado(novoJogador, novoOponente, novaMesa, novoTipo, tipoAnterior)


# Inicia o procedimento de busca Expectiminimax.
def expectiminimax(estado, profundidade):
    if (estado.ehEstadoTerminal() or profundidade == 0): return estado.utilidade() #, None
    valor = None
    if (estado.tipo == Estado.MAX):
        valor = -math.inf
        for acao in estado.acoes: valor = max(valor, expectiminimax(resultado(estado, acao), profundidade-1))
    if (estado.tipo == Estado.MIN):
        valor = math.inf
        for acao in estado.acoes: valor = min(valor, expectiminimax(resultado(estado, acao), profundidade-1))
    if (estado.tipo == Estado.CHANCE):
        valor = 0
        for acao in estado.acoes: valor += (acao[PROBABILIDADE] * expectiminimax(resultado(estado, acao), profundidade-1))
    return valor

#Decide a melhor jogada a ser executada num dado estado s do jogo pela instância de Jogador que chama esta função.
#Retorna a Peça que deve ser jogada e a posição em que deve ser colocada.
def escolheJogada(estado):
    acoes = estado.acoes
    melhorAcao = None
    valor = -math.inf
    for acao in acoes:
        novoValor = expectiminimax(estado, PROFUNDIDADE)
        if (novoValor > valor):
            valor = novoValor
            melhorAcao = acao
    return melhorAcao