from classes.Peca import *
from classes.Jogador import *
import random

class Mesa():
    def __init__(self):
        self.__pecasAComprar = []
        self.__tabuleiro = []


    def __str__(self):
        resp = None
        resp = "Mesa: "
        for peca in self.__pecasAComprar: resp += peca
        resp = "\nTabuleiro: "
        for peca in self.__tabuleiro: resp += peca
        print(resp)

    def gerarPecas(self):
        pecas = [] * 28
        for i in range(0, 7):
            for j in range(i, 7):
                pecas.append(Peca(i, j))
        return pecas

    def comprarPeca(self, listaPecas):
        pos = random.randint(0, len(listaPecas)-1)
        peca = listaPecas[pos]
        del listaPecas[pos]
        return peca

    def comecarJogo(self):
        self.__pecasAComprar = self.gerarPecas()
        jogador1 = Jogador()
        jogador2 = Jogador()
        for i in range(0, 7):
            jogador1.adicionaPeca(self.comprarPeca(self.__pecasAComprar))
            jogador2.adicionaPeca(self.comprarPeca(self.__pecasAComprar))
        self.procuraMaiorPeca(jogador1, jogador2)
        return self.__pecasAComprar, jogador1, jogador2

    def procuraMaiorPeca(self, jogador1, jogador2):
        maior1 = None
        maior2 = None
        for i in range(6, 0, -1):
            if (maior1 == None) and (Peca(i, i) in jogador1.pecas()): maior1 = Peca(i, i)
            if (maior2 == None) and (Peca(i, i) in jogador2.pecas()): maior2 = Peca(i, i)
        if (maior1 == None):
            maior1 = jogador1.pecas()[0]
            for i in range(len(jogador1.pecas())):
                if ((jogador1.pecas()[i]).somatorio() > maior1.somatorio()): maior1 = jogador1.pecas()[i]
        if (maior2 == None):
            maior2 = jogador2.pecas()[0]
            for i in range(len(jogador2.pecas())):
                if ((jogador2.pecas()[i]).somatorio() > maior2.somatorio()): maior2 = jogador2.pecas()[i]
        print("Maior peça de jog. 1: " + str(maior1))
        print("Maior peça de jog. 2: " + str(maior2))
        jogador1.setaVez(True) if (maior1.somatorio() > maior2.somatorio()) else jogador2.setaVez(True)
        return