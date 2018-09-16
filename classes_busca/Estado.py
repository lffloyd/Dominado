import copy

class Estado():
    # Se esse estado é uma vitória, o valor de utilidade é True
    # A mesa fornece a informação de que peças ainda estão disponiveis para a compra
    def __init__(self, jogador, oponente, mesa, turno=0):
        self.jogador = copy.deepcopy(jogador)
        self.oponente = copy.deepcopy(oponente)
        self.mesa = copy.deepcopy(mesa)
        self.__qtdPecasComprar = len(self.mesa.pegaPecasAComprar())
        self.__qtdPecasOponente = len(self.oponente.pecas())
        self.__extremoEsq, self.__extremoDir = self.mesa.extremos()
        self.__acoes = copy.deepcopy(jogador.pegaPecasJogaveis())
        self.utilidade = 0
        #Indica qual é o jogador que executa uma jogada neste estado.
        self.turno = turno

    def ehEstadoTerminal(self): return len(self.__acoes) == 0

    def alternaTurno(self): self.turno = (0 if (self.turno == 1) else 1)

    def turnoDoOponente(self): return self.turno == 1

