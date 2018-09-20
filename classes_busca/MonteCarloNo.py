#Define a classe MonteCarloNo, responsável por descrever o um nó no algoritmo de busca 'Monte-Carlo tree search'.

#Escrito por: Vítor Costa.

#from classes_MCTS import EstadoMCTS
#import numpy as np
#import random
import copy

class MonteCarloNo:
    def __init__(self, estado, pai = None):
        self.estado = estado
        self.pai = pai
        self.filhos = []

    def __str__(self): return "Filhos:" + str(len(self.filhos))

    def expandir(self):
        for peca in self.estado.jogador.pegaPecasJogaveis():
            x = 0
            for i in range(2):
                novoEstado = copy.deepcopy(self.estado)
                adicionou = novoEstado.mesa.adicionarNaMesa(peca, x)
                novoNo = MonteCarloNo(novoEstado, self)
                novoEstado.jogador.setaVez(False)
                if(adicionou):
                    self.filhos.append(novoNo)
                x+=1

    def foiTotalementeExpandido(self):
        if(self.estado.jogador.ehSuaVez() == True):
            return len(self.filhos) == len(self.estado.jogador.pegaPecasJogaveis())
        else:
            return len(self.filhos) == len(self.estado.oponente.pegaPecasJogaveis())



    #TEM QUE FAZER ESSA FUNÇÃO DO ESTADO TERMINAL
    def simular(self, no):
        while(no.estado.ehEstadoTerminal() != True):
            no.expandir()