from classes import Peca as pec
import random

class Mesa():
    def __init__(self):
        self.__pecas = []

    def gerarPecas(self):
        pecas = [] * 28
        for i in range(0, 7):
            for j in range(i, 7):
                pecas.append(pec.Peca(i, j))
        return pecas

    def comprarPeca(self, listaPecas):
        pos = random.randint(0, len(listaPecas)-1)
        peca = listaPecas[pos]
        del listaPecas[pos]
        return peca

    def comecarJogo(self, jogador1, jogador2):
        listaPecas = self.gerarPecas()
        for i in range(0, 7):
            jogador1.addPeca(self.comprarPeca(listaPecas))
            jogador2.addPeca(self.comprarPeca(listaPecas))
        return listaPecas