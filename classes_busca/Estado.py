#Define a classe Estado, responsável por descrever o estado global de uma partida num dado momento. Usada para explorar
#as possibilidades de jogada com os algoritmos de busca Expectiminimax e Monte-Carlo tree search.

#Escrito por: Luiz Felipe, Vítor Costa, Renato Bastos

import copy

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
            jogador.atualizaPecasJogaveis(mesa, jogador.pecas())
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

    ###########Comentado pois pode ser útil futuramente.############
    #Gera todas as possibilidades de estados/ações dado um nó/estado origem s. Gera as possibilidades de jogadas a partir dessa
    #raizes. As possibilidades de ações/jogadas diferem caso turno == 0 (serão jogadas do jogador max) e caso turno == 1 (serão
    #as possíveis jogadas do jogador min).
    # def gerarEstados(self, mesa, possibilidades):
    #     estadosFilhos = []
    #     for tupla in possibilidades:
    #         peca = copy.deepcopy(tupla[0])
    #         pos = copy.deepcopy(tupla[1])
    #         novaMesa = copy.deepcopy(mesa)
    #         novaMesa.adicionaNaMesa(peca, pos)
    #         estadosFilhos.append(novaMesa)
    #     return estadosFilhos


    #Gera todas as possibilidades de jogada que podem ser executadas por um oponente no dado estado do jogo.
    #Considera que o oponente pode possuir todas as peças que não estão na mão do jogador ou encaixadas na mesa de jogo,
    #i.e. todas as peças em sua mão e todas peças disponíveis para compra.
    #A probabilidade de uma peça existir já está sendo levada em consideração, mas nenhum cálculo mais complexo é executado
    #para obtê-la exceto
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
                possibilidades.append([peca, esq, probabilidade])
                possibilidades.append([peca.viraPeca(), dir, probabilidade])
            else: possibilidades.append([peca, (esq if (peca.ehJogavel(esq)) else dir), probabilidade])
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

    ############Precisa finalizar esta função utilidade().############
    #Calcula o valor de utilidade de um nó. Deve-se diferenciar um nó terminal (i.e. que finaliza a partida) e um nó interno
    # pois o cálculo do valor de utilidade provavelmente será distinto entre eles.
    #Ainda não implementado.
    def utilidade(self): return self.utilidade

