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

    def gerarEstados(self, mesa, mao, possibilidades, turno):
        estadosFilhos = []
        for tupla in possibilidades:
            peca = tupla[0]
            pos = tupla[1]
            novaMesa = copy.deepcopy(mesa)
            novaMesa.adicionaNaMesa(peca, pos)
            estadosFilhos.append(novaMesa)

        # estados = []
        # jogadasPossiveis = jogadasPossiveis(mesa, mao) // retornar as peças
        # que
        # sao
        # possiveis
        # de
        # ser
        # jogadas
        # for peca in jogadasPossiveis:
        #     novaMesa = mesa.copy
        #     if pecaDoisLados:
        #         novaMesa = jogar(novaMesa, peca, 2)
        #         estado = Estado(novaMesa, mesa.qtdpecasoponente - -, mesa.qtdpecascomprar)
        #         estados.append(estado)
        #     novaMesa = jogar(novaMesa, peca)
        #     estado = Estado(novaMesa, mesa.qtdpecasoponente - -, mesa.qtdpecascomprar)
        #     estados.append(estado)
        # if size(jogadasPossiveis) < mesa.pecasAComprar
        #     estado = Estado(novaMesa, mesa.qtdpecasoponente, mesa.qtdpecascomprar - -)
        #     estados.append(estado)
        # return estados

    def ehEstadoTerminal(self): return len(self.__acoes) == 0

    def alternaTurno(self): self.turno = (0 if (self.turno == 1) else 1)

    def turnoDoOponente(self): return self.turno == 1

