from classes import Peca as pec
import random

class Mesa():
    def __init__(self): return

    def gerarPecas(self):
        pecas = []
        for i in range(0, 7):
            for j in range(i, 7):
                pecas.append(pec.Peca(i, j))
        return pecas

    def comprarPeca(self, listaPecas):
        pos = random.randint(0, len(listaPecas)-1)
        peca = listaPecas[pos]
        del listaPecas[pos]
        return peca
