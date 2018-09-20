#Define a classe EstadoMCTS, responsável por descrever o estado global de uma partida num dado momento. Usada para explorar
#as possibilidades de jogada com o algoritmo de busca 'Monte-Carlo tree search'. Observar que a classe tem diferenças em
#relação a classe 'Estado'.

#Escrito por: Vítor Costa.

import copy

class EstadoMCTS():
    #Construtor de classe. Define atributos associados ao estado global de uma partida.
    def __init__(self, jogador, oponente, mesa):
        self.jogador = copy.deepcopy(jogador)
        self.oponente = copy.deepcopy(oponente)
        self.mesa = copy.deepcopy(mesa)
        self.qtdPecasComprar = len(self.mesa.pegaPecasAComprar())
        self.qtdPecasOponente = len(self.oponente.pecas())
        self.probabilidade = 0
        self.ultimaPecaJogada = None

    #Indica se um estado terminal foi atingido
    def ehEstadoFinal(self):
        if (self.jogador.jaGanhou() == True or self.oponente.jaGanhou() == True): return True
        else: return False