#Define a classe Estado, responsável por descrever o estado global de uma partida num dado momento. Usada para explorar
#as possibilidades de jogada com os algoritmos de busca Expectiminimax e Monte-Carlo tree search.

#Escrito por: Luiz Felipe, Vítor Costa, Renato Bastos

import copy

class Estado():
    # Constantes usadas para indicação do tipo de estado/nó:
    MAX = 1 #Indica que o estado/nó atual é de max.
    CHANCE = 0 #Indica que o estado/nó atual é de chance, i.e. armazena a probabilidade de seus filhos ocorrerem.
    MIN = -1 # " " " " " " " min.
    # Define o construtor de classe, que define seus atributos internos de acordo com o momento de jogo.
    def __init__(self, jogador, oponente, mesa, tipoEstado=0):
        self.jogador = copy.deepcopy(jogador)
        self.oponente = copy.deepcopy(oponente)
        self.mesa = copy.deepcopy(mesa)
        self.__qtdPecasComprar = len(self.mesa.pegaPecasAComprar())
        self.__qtdPecasOponente = len(self.oponente.pecas())
        self.__extremoEsq, self.__extremoDir = self.mesa.extremos()
        self.__acoes = self.gerarEstados(mesa, (jogador.possibilidadesJogaveis() if (tipoEstado == 0)
                                                else (oponente.possibilidadesJogaveis()+
                                                      self.mesa.pegaPecasAComprar())), 0)
        self.utilidade = 0
        #Indica qual é o jogador que executa uma jogada neste estado.
        self.tipo = tipoEstado

    #Gera todas as possibilidades de estados/ações dado um nó/estado origem s. Gera as possibilidades de jogadas a partir dessa
    #raizes. As possibilidades de ações/jogadas diferem caso turno == 0 (serão jogadas do jogador max) e caso turno == 1 (serão
    #as possíveis jogadas do jogador min).
    def gerarEstados(self, mesa, possibilidades):
        estadosFilhos = []
        for tupla in possibilidades:
            peca = copy.deepcopy(tupla[0])
            pos = copy.deepcopy(tupla[1])
            novaMesa = copy.deepcopy(mesa)
            novaMesa.adicionaNaMesa(peca, pos)
            estadosFilhos.append(novaMesa)
        return estadosFilhos

    #Avalia se um dado nó/estado é terminal, i.e. finaliza a partida.
    def ehEstadoTerminal(self): return len(self.__acoes) == 0

    #Alterna o turno de um estado. Usado para alternar entre jogadas de max e min na exploração das possibilidades de ações.
    def alternaTurno(self): self.turno = (0 if (self.tipo == 1) else 1)

    #Indica se o turno atual é do oponente, i.e. se o turno atual é do jogador min.
    def turnoDoOponente(self): return self.tipo == 1

