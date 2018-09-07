import random
from classes import Peca as pec

def gerarPecas():
    pecas = []*28
    for i in range(0,7):
        for j in range(i,7):
                pecas.append(pec.Peca(i,j))
    return pecas

def comprarPeca(listaPecas):
    pos = random.randint(0, len(listaPecas))
    peca = listaPecas[pos]
    del listaPecas[pos]
    return peca

listaPecas = gerarPecas()

print(comprarPeca(listaPecas),"\n\n\n")

for i in listaPecas: print(i)