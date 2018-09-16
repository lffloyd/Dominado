import copy

class Estado():
    # Se esse estado é uma vitória, o valor de utilidade é True
    # A mesa fornece a informação de que peças ainda estão disponiveis para a compra
    def __init__(self, jogador, oponente, mesa):
        self.jogador = copy.deepcopy(jogador)
        self.oponente = copy.deepcopy(oponente)
        self.mesa = copy.deepcopy(mesa)
        self.__qtdPecasComprar = len(self.mesa.pegaPecasAComprar())
        self.__qtdPecasOponente = len(self.oponente.pecas())
        self.__extremoEsq, self.__extremoDir = mesa.extremos()
        self.__acoes = []
        self.utilidade = 0

    def ehEstadoTerminal(self): return len(self.__acoes) == 0

