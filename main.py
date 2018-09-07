from classes.Peca import *
from classes.Jogador import *
from classes.Mesa import *

def comecarJogo(mesa, jogador1, jogador2):
    listaPecas = mesa.gerarPecas()
    for i in range(0,7):
        jogador1.addPeca(mesa.comprarPeca(listaPecas))
        jogador2.addPeca(mesa.comprarPeca(listaPecas))
    return listaPecas

mesa = Mesa()
jogador1 = Jogador()
jogador2 = Jogador()
listaPecas = comecarJogo(mesa, jogador1, jogador2)


print(jogador1)
print(jogador2)
for i in listaPecas: print(i)