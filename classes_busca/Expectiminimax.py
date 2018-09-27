# MIT License
#
# Copyright (c) 2018 Luiz Felipe de Melo (lffloyd), Vítor Costa (vitorhardoim), Renato Bastos (RenatoBastos33)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
##############################################################################################################


# Define a classe Expectiminimax, responsável por realizar uma busca por possibilidades de ações para o jogador IA.

# Escrito por: Luiz Felipe.

from classes_busca.Estado import *
import copy
import math

#Constantes:
PROFUNDIDADE = 8 #Constante que define a profundidade de busca do algoritmo. Quando esta profundiade é alcançada, o algoritmo
                 #para retornando o valor de utilidade do nó analisado.
#Constantes para acesso dos campos de uma 'ação'. Uma ação é representada por uma tupla ou vetor contendo a peça a ser encaixada
#ou jogada nesta ação, a posição de encaixe da peça no tabuleiro e a probabilidade de escolha associada a esta peça.
PECA = 0
POSICAO = 1
PROBABILIDADE = 2

# Retorna o resultado da execução de uma dada ação (i.e. inserção de peça) num dado estado (i.e. mesa/tabuleiro). Ou
# seja, retorna o estado resultado da ação/jogada tomada.
def resultado(estado, acao):
    #Determina qual será o tipo (MAX, MIN, CHANCE) do nó/estado a ser criado.
    novoTipo = 0
    if (estado.tipo == Estado.MAX or estado.tipo == Estado.MIN): novoTipo = Estado.CHANCE
    if (estado.tipo == Estado.CHANCE): novoTipo = (Estado.MAX if (estado.tipoAnterior == Estado.MIN) else Estado.MIN)
    tipoAnterior = estado.tipo
    #Executa uma cópia do conteúdo da mesa de jogo e dos jogadores participantes, para que a exploração da árvore de
    #possibilidades seja independente dos dados mesa e jogadores originais.
    novaMesa = copy.deepcopy(estado.mesa)
    novoJogador = copy.deepcopy(estado.jogador)
    novoOponente = copy.deepcopy(estado.oponente)
    novoJogador.atualizaPecasJogaveis(novaMesa)
    #Executa a ação (ou jogada) especificada por parâmetro.
    novaMesa.adicionarNaMesa(acao[PECA], acao[POSICAO])
    novoJogador.removePeca(novaMesa, acao[PECA])
    #Configura as variáveis de controle de quem jogará em seguida.
    novoJogador.setaJogou(True)
    novoJogador.setaVez(False)
    novoOponente.setaVez(True)
    #Executa compras de peças caso necessário.
    novoJogador.compraDaMesa(novaMesa)
    novoOponente.compraDaMesa(novaMesa)
    #Verifica se as condições de vitória foram satisfeitas neste novo estado.
    if ((novoJogador.jaGanhou() or novoOponente.jaGanhou()) or
            (not novoJogador.jogouRodada() or not novoOponente.jogouRodada())):
        estado.setaEstadoTerminal(True)
    #Retorna um estado correspondente àquele gerado pela execução da ação.
    return Estado(novoOponente, novoJogador, novaMesa, novoTipo, tipoAnterior) \
        if (novoTipo == Estado.MIN) else Estado(novoJogador, novoOponente, novaMesa, novoTipo, tipoAnterior)

# Inicia o procedimento de busca Expectiminimax.
# O procedimento Expectiminimax é uma adapatação do algoritmo Minimax para jogos estocásticos (i.e. jogos de chance ou não-
#determinísticos).
def expectiminimax(estado, profundidade):
    #Condição de parada: caso o estado atingido seja terminal deve-se calcular seu valor de utilidade, e caso o limite de
    # profundidade tenha sido alcançado calcula-se o valor heurístico do nó atingido.
    if (estado.ehEstadoTerminal() or profundidade == 0): return estado.utilidade()
    valor = None
    #Caso o nó atual represente uma jogada nossa -- maximiza a nossa jogada a partir de todas as opções disponíveis a
    #partir daqui.
    if (estado.tipo == Estado.MAX):
        valor = -math.inf
        #Varre a lista de ações possíveis procurando aquela que maximiza nossos resultadso.
        for acao in estado.acoes: valor = max(valor, expectiminimax(resultado(estado, acao), profundidade-1))
    #Caso o nó atual represente uma jogada de nosso oponente -- minimiza as nossas possibilidades de jogada a partir deste
    # nó.
    if (estado.tipo == Estado.MIN):
        valor = math.inf
        # Varre a lista de ações possíveis procurando aquela que minimize nossos resultados.
        for acao in estado.acoes: valor = min(valor, expectiminimax(resultado(estado, acao), profundidade-1))
    #Caso o nó atual seja um nó de chance. Nós de chance atuam apenas como acumuladores das probabildiades dos seus
    #nós filhos. Usado pois a escolha de uma jogada no dominó não é determinística e está associada a estas probabilidades
    #de escolha.
    if (estado.tipo == Estado.CHANCE):
        valor = 0
        #Varre a lista de filhos (ou ações) acumulando (somando) as probabilidades de ocorrência de cada uma das ações.
        for acao in estado.acoes: valor +=\
            (acao[PROBABILIDADE] * expectiminimax(resultado(estado, acao), profundidade-1))
    #Retorna o melhor valor encontrado dependendo do tipo do nó/estado analisado.
    return valor

#Decide a melhor jogada a ser executada num dado estado s do jogo pela instância de Jogador que chama esta função.
#Retorna a Peça que deve ser jogada e a posição em que deve ser colocada no tabuleiro.
def escolheJogada(estado):
    #Recupera as ações que podem ser executadas a partir deste estado.
    acoes = estado.acoes
    melhorAcao = None
    valor = -math.inf
    #Para cada ação disponível a partir deste nó/estado:
    for acao in acoes:
        #Calcula o valor de utilidade associado a execução desta ação.
        novoValor = expectiminimax(estado, PROFUNDIDADE)
        #Se o valor calculado é melhor do que o anteriormente obtido substitui-se:
        if (novoValor > valor):
            valor = novoValor
            melhorAcao = acao
    #Retorna a melhor ação que pode ser executada a partir do estado atual.
    return melhorAcao
