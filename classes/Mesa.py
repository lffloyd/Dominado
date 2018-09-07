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
        jogador1 = Jogador(1)
        jogador2 = Jogador(2)
        for i in range(0, 7):
            jogador1.adicionaPeca(self.comprarPeca(self.__pecasAComprar))
            jogador2.adicionaPeca(self.comprarPeca(self.__pecasAComprar))
        maior1, somar1 = self.procuraMaiorPeca(jogador1)
        maior2, somar2 = self.procuraMaiorPeca(jogador2)
        if ((somar1 == True) and (somar2 == True)) or ((somar1 == False) and (somar2 == False)):
            jogador1.setaVez(True) if (maior1.somatorio() > maior2.somatorio()) else jogador2.setaVez(True)
        else:
            jogador1.setaVez(True) if ((somar1 == False) and (somar2 == True)) else jogador2.setaVez(True)
        print("Maior peça de jog. 1: " + str(maior1) + "\tSomar? " + str(somar1))
        print("Maior peça de jog. 2: " + str(maior2) + "\tSomar? " + str(somar2))
        return self.__pecasAComprar, jogador1, jogador2

    def procuraMaiorPeca(self, jogador):
        maior = None
        somar = True
        for i in range(6, 0, -1):
            if ((maior == None) and (somar == True)) and (Peca(i, i) in jogador.pecas()):
                maior = Peca(i, i)
                somar = False
                break
        if (maior == None) and (somar == True):
            maior = jogador.pecas()[0]
            for i in range(1, len(jogador.pecas())):
                if ((jogador.pecas()[i]).somatorio() > maior.somatorio()): maior = jogador.pecas()[i]
        return maior, somar