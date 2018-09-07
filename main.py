from classes.Peca import *
from classes.Jogador import *
from classes.Mesa import *

mesa = Mesa()
jogador1 = Jogador()
jogador2 = Jogador()
listaPecas = mesa.comecarJogo(jogador1, jogador2)

print(jogador1)
print(jogador2)
for i in listaPecas: print(i)