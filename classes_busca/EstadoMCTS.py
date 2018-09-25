#Define a classe EstadoMCTS, responsável por descrever o estado global de uma partida num dado momento. Usada para explorar
#as possibilidades de jogada com o algoritmo de busca 'Monte-Carlo tree search'. Observar que a classe tem diferenças em
#relação a classe 'Estado'.

#Escrito por: Vítor Costa, Renato Bastos.

import copy

class EstadoMCTS():
    #Construtor de classe. Define atributos associados ao estado global de uma partida.
    def __init__(self, jogador, oponente, mesa):
        self.jogador = jogador
        self.oponente = oponente
        self.mesa = mesa
        self.qtdPecasComprar = len(self.mesa.pegaPecasAComprar())
        self.qtdPecasOponente = len(self.oponente.pecas())
        self.probabilidade = 0
        self.ultimaPecaJogada = None

    def __str__(self):
        print(self.jogador)
        print(self.oponente)
        print(self.mesa)

    def comparar(self,estado2):
        for peca in self.jogador.pecas():
            achou=False
            for peca2 in estado2.jogador.pecas():
                if peca.igual(peca2):
                    achou=True
                    break
            if achou==False: return False

        for peca in self.oponente.pecas():
            igual=False
            for peca2 in estado2.oponente.pecas():
                if peca.igual(peca2):
                    igual=True
                    break
            if igual==False: return False
        onde=0
        for pecaTab in self.mesa.pegaTabuleiro():
            pecaTab2=estado2.mesa.pegaTabuleiro()[onde]
            if not pecaTab.igual(pecaTab2): return False
            onde+=1
        return True

    #Indica se um estado terminal foi atingido
    def ehEstadoFinal(self): return not self.mesa.fechada