#Define a classe Estado, responsável por descrever o estado global de uma partida num dado momento. Usada para explorar
#as possibilidades de jogada com os algoritmos de busca Expectiminimax e Monte-Carlo tree search.

#Escrito por: Luiz Felipe, Vítor Costa.

import copy
import math

class Estado():
    # Constantes usadas para indicação do tipo de estado/nó:
    MAX = 2 #Indica que o estado/nó atual é de max.
    CHANCE = 1 #Indica que o estado/nó atual é de chance, i.e. armazena a probabilidade de seus filhos ocorrerem.
    MIN = 0 # " " " " " " " min.
    # Define o construtor de classe, que define seus atributos internos de acordo com o momento de jogo.
    def __init__(self, jogador, oponente, mesa, tipoEstado=0, tipoAnterior=0):
        #Definição de atributos típicos da classe.
        self.jogador = copy.deepcopy(jogador)
        self.oponente = copy.deepcopy(oponente)
        self.mesa = copy.deepcopy(mesa)
        self.__qtdPecasComprar = len(self.mesa.pegaPecasAComprar())
        self.__qtdPecasOponente = len(self.oponente.pecas())
        self.acoes = []
        if (tipoEstado == self.MAX):
            jogador.atualizaPecasJogaveis(mesa)
            self.acoes = copy.deepcopy(jogador.possibilidadesJogaveis(self.mesa))
        if (tipoEstado == self.MIN):
            self.acoes = self.possibilidadesOponente(oponente, mesa)
        #Atributos para valor de utilidade, probabilidade, tipo de estado (max, min ou chance) etc.
        self.valorUtilidade = 0
        self.probabilidade = 0
        self.ultimaPecaJogada = None
        #Indica qual é tipo do estado.
        self.tipo = tipoEstado
        #Indica o tipo de estado anterior ao atual.
        self.tipoAnterior = tipoAnterior

    #Gera todas as possibilidades de jogada que podem ser executadas por um oponente no dado estado do jogo.
    #Considera que o oponente pode possuir todas as peças que não estão na mão do jogador ou encaixadas na mesa de jogo,
    #i.e. todas as peças em sua mão e todas peças disponíveis para compra.
    #A probabilidade de uma peça existir já está sendo levada em consideração, mas nenhum cálculo mais complexo é executado
    #para obtê-la.
    def possibilidadesOponente(self, oponente, mesa):
        pecasMesa = mesa.pegaPecasAComprar()
        possibilidades = []
        probabilidade = 0
        if (len(mesa.pegaTabuleiro()) == 0):
            for peca in pecasMesa:
                possibilidades.append([peca, 0, probabilidade])
        esq, dir = mesa.extremos()
        for peca in pecasMesa:
            if peca.ehJogavel(esq) and peca.ehJogavel(dir):
                possibilidades.append([peca, 0, probabilidade])
                possibilidades.append([peca.viraPeca(), 1, probabilidade])
            else: possibilidades.append([peca, (0 if (peca.ehJogavel(esq)) else 1), probabilidade])
        for jogada in possibilidades: jogada[2] = 1/(len(possibilidades)+len(oponente.possibilidadesJogaveis()))
        possibilidades = copy.deepcopy(oponente.possibilidadesJogaveis()+possibilidades)
        return possibilidades

    #Avalia se um dado nó/estado é terminal, i.e. finaliza a partida.
    def ehEstadoTerminal(self): return len(self.acoes) == 0

    #Seta o estado terminal.
    def setaEstadoTerminal(self, bool):
        if (bool == True): self.acoes = []

    #Alterna o turno de um estado. Usado para alternar entre estados de max, chance e min na exploração das
    # possibilidades de ações.
    def alternaTipo(self, tipoEstado): self.tipo = tipoEstado

    #Métodos para cálculo do valor de um estado/nó terminal ou de nós intermediários (nesse caso, utilizando heurísticas).
    def valorDoEstado(self):
        fat1 = len(self.oponente.pecas()) - len(self.jogador.pecas())
        fat2 = (self.oponente.somatorioPecas() if (fat1 > 0) else self.jogador.somatorioPecas())
        return fat1*fat2

    def heuristica1(self):
        fat1 = len(self.oponente.pecas()) - len(self.jogador.pecas())
        fat2 = None
        if (self.jogador.pecas() != []):
            peca, somar = self.mesa.procuraMaiorPeca(self.jogador)
            fat2 = (peca.esq()*peca.dir() if (peca != None) else fat1)
        else:
            fat2 = len(self.oponente.pecas())
        return (fat1*fat2 if (fat1 != 0) else fat2)

    def heuristica2(self):
        fat1 = len(self.oponente.pecas()) - len(self.jogador.pecas())
        esq, dir = self.mesa.extremos()
        contagemMesaEsq, contagemMesaDir = self.mesa.contarValor(esq), self.mesa.contarValor(dir)
        contagemJogadorEsq, contagemJogadorDir = self.jogador.contarValor(esq), self.jogador.contarValor(dir)
        fat2 = math.sqrt((contagemMesaEsq ** 2) + (contagemMesaDir ** 2))
        fat3 = math.sqrt((contagemJogadorEsq ** 2) + (contagemJogadorDir ** 2))
        return ((fat1 * math.sqrt(fat2 + fat3)) if (fat1 != 0) else ((fat2 + fat3)))

    #Calcula o valor de utilidade de um nó. Deve-se diferenciar um nó terminal (i.e. que finaliza a partida) e um nó interno
    # pois o cálculo do valor de utilidade provavelmente será distinto entre eles.
    #Ainda não implementado.
    def utilidade(self):
        if (self.ehEstadoTerminal()): return self.valorDoEstado()
        else: return self.heuristica1()